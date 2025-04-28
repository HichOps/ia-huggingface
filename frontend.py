import os
import base64
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

# Empêcher Streamlit de surveiller le module torch qui cause l'erreur
if os.environ.get("PYTHONPATH") is None:
    os.environ["PYTHONPATH"] = ""

# ————— UTILITAIRES —————

def load_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def inject_global_styles(font_path: str, bg_path: str):
    if not os.path.isfile(font_path):
        st.error(f"Police introuvable : {font_path}")
        return
    if not os.path.isfile(bg_path):
        st.error(f"Image de fond introuvable : {bg_path}")
        return
    font_b64 = load_base64(font_path)
    bg_b64   = load_base64(bg_path)
    css = f"""
    <style>
      @font-face {{
        font-family: 'BreakingBad';
        src: url(data:font/otf;base64,{font_b64}) format('opentype');
      }}
      
      /* Police globale et texte en blanc par défaut */
      html, body, [class*="st-"], [data-testid="stAppViewContainer"] *,
      .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div, 
      [data-testid="stHeader"], [data-testid="baseButton-secondary"],
      .stRadio label, .stCheckbox label, .stSelectbox label {{
        font-family: 'BreakingBad', sans-serif !important;
        color: white !important;
      }}
      
      /* Image de fond */
      [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{bg_b64}") no-repeat center center fixed;
        background-size: cover;
      }}
      
      /* Couleur de fond des widgets */
      .stButton button, .stSelectbox, .css-1inwz65 {{
        background-color: rgba(50, 50, 50, 0.7) !important;
        color: white !important;
        border-color: #444 !important;
      }}
      
      /* Champs de saisie en noir */
      [data-testid="stTextInput"] input,
      [data-testid="stTextArea"] textarea {{
        font-family: sans-serif !important;
        color: black !important;
        background-color: white !important;
      }}
      
      /* Options déroulantes */
      .stSelectbox option {{
        color: black !important;
        background-color: white !important;
      }}
      
      /* Couleur des boutons et sélections */
      .stButton button:hover {{
        border-color: white !important;
      }}
      
      /* Classe pour les résultats formatés */
      .user-standard-font {{
        font-family: sans-serif !important;
        color: white !important;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
      }}
      
      /* Ajuster les couleurs du graphique matplotlib */
      .stPlotlyChart, .stPlot {{
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 5px;
        padding: 10px;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ————— FONCTIONS MÉTIER —————

def sentiment_analysis(text: str) -> str:
    if not text.strip():
        return "<div class='user-standard-font'>Veuillez entrer un texte.</div>"
    
    # Importer pipeline seulement quand nécessaire (lazy loading)
    from transformers import pipeline
    
    clf = pipeline(
        "sentiment-analysis",
        model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"
    )
    res = clf(text)[0]
    return (
        f"<div class='user-standard-font'>💬 <strong>Sentiment :</strong> {res['label']}  "
        f"|  <strong>Score :</strong> {res['score']:.2f}</div>"
    )

def plot_forex(pair: str):
    pair = pair.upper()
    ticker = f"{pair[:3]}{pair[3:]}=X"
    data = yf.download(ticker, period="1mo")
    
    # Configuration spécifique pour un thème sombre
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data['Close'], color='#33ff33', linewidth=2)
    
    # Personnalisation des axes et titres en blanc
    ax.set_title(f"Cours {pair}", color='white', fontsize=16)
    ax.set_xlabel("Date", color='white')
    ax.set_ylabel("Prix", color='white')
    
    # Personnalisation des grilles
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Couleur des axes
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    
    # Personnalisation des graduations
    ax.tick_params(axis='both', colors='white')
    
    # Fond transparent
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    
    st.pyplot(fig)

def tradingview_widget(pair: str):
    html = f"""
    <div class="tradingview-widget-container" style="margin: 10px 0; padding: 10px; background-color: rgba(0, 0, 0, 0.5); border-radius: 5px;">
      <div id="tradingview_chart"></div>
      <script src="https://s3.tradingview.com/tv.js"></script>
      <script>
      new TradingView.widget({{
        "width": 800,
        "height": 500,
        "symbol": "FX:{pair}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "fr",
        "toolbar_bg": "#1E222D",
        "enable_publishing": false,
        "hide_top_toolbar": false,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    st.components.v1.html(html, height=550)

# ————— APPLICATION —————

def main():
    BASE      = os.path.dirname(__file__)
    FONT      = os.path.join(BASE, "breakingbad-font.otf")
    BG        = os.path.join(BASE, "breakingbad-wallpaper.jpg")
    LOGO      = os.path.join(BASE, "heisenberg.png")

    inject_global_styles(FONT, BG)
    
    # En-tête
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(LOGO, width=180)

    st.markdown("<h1 style='text-align:center; font-size:50px'>💰 Analyse de Sentiment Financier</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:22px; color: white;'>Cette application analyse le sentiment de vos textes financiers.</p>",
        unsafe_allow_html=True
    )

    # — Sentiment —
    st.markdown("<h3 style='color: white;'>Analyse de Sentiment</h3>", unsafe_allow_html=True)
    
    text = st.text_area("Entrez votre texte ici", "")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💬 Analyser le sentiment"):
            st.markdown(sentiment_analysis(text), unsafe_allow_html=True)

    st.markdown("<hr style='border-color: white; margin: 30px 0;'>", unsafe_allow_html=True)

    # — Forex —
    st.markdown("<h3 style='color: white;'>Analyse Forex</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pair = st.text_input("Paire Forex (ex. EURUSD, GBPJPY)", "EURUSD")
    with col2:
        method = st.selectbox("Source des données", ["yfinance", "TradingView widget"])
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📈 Afficher le graphique"):
            if method == "yfinance":
                plot_forex(pair)
            else:
                tradingview_widget(pair)

if __name__ == "__main__":
    main()