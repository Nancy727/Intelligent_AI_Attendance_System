import streamlit as st


HOME_BACKGROUND = "linear-gradient(180deg, #f6f8ff 0%, #eef4ff 42%, #f9fbff 100%)"
DASHBOARD_BACKGROUND = "radial-gradient(circle at top left, rgba(30, 64, 175, 0.10), transparent 34%), linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%)"


def style_background_home():

    st.markdown("""
        <style>
                .stApp {
                    background: %s !important;
                }
        </style>  

                """
            % HOME_BACKGROUND, unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: %s !important;
                }

        </style>  

                """
            % DASHBOARD_BACKGROUND, unsafe_allow_html=True)
    

    

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

            :root {
                --academic-primary: #1e40af;
                --academic-secondary: #0ea5e9;
                --academic-accent: #d97706;
                --academic-surface: rgba(255, 255, 255, 0.92);
                --academic-surface-strong: #ffffff;
                --academic-border: rgba(148, 163, 184, 0.28);
                --academic-text: #0f172a;
                --academic-muted: #475569;
                --academic-radius: 12px;
                --academic-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
            }

            #MainMenu, footer, header {
                visibility: hidden;
            }

            html, body, .stApp {
                color: var(--academic-text) !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                max-width: 1200px !important;
            }

            h1, h2, h3, h4, h5, h6, p, span, label, button, input, textarea, li, div {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            h1, h2, h3 {
                letter-spacing: -0.03em;
            }

            .academic-card,
            div[data-testid="stVerticalBlockBorderWrapper"],
            div[data-testid="stForm"],
            div[data-testid="stExpander"],
            div[data-testid="stDialog"] > div {
                border-radius: var(--academic-radius) !important;
            }

            .academic-card,
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--academic-surface) !important;
                border: 1px solid var(--academic-border) !important;
                box-shadow: var(--academic-shadow) !important;
                padding: 1.15rem 1.2rem !important;
            }

            .academic-hero {
                background: linear-gradient(135deg, rgba(30, 64, 175, 0.10), rgba(14, 165, 233, 0.08)) !important;
                border: 1px solid rgba(30, 64, 175, 0.14) !important;
            }

            .academic-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.35rem 0.75rem;
                border-radius: 999px;
                background: rgba(30, 64, 175, 0.08);
                color: var(--academic-primary);
                font-size: 0.8rem;
                font-weight: 700;
                letter-spacing: 0.01em;
            }

            .academic-muted {
                color: var(--academic-muted);
            }

            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.90);
                border: 1px solid var(--academic-border);
                border-radius: var(--academic-radius);
                padding: 1rem;
                box-shadow: var(--academic-shadow);
            }

            div[data-testid="stButton"] > button {
                border-radius: var(--academic-radius) !important;
                border: 1px solid transparent !important;
                padding: 0.8rem 1rem !important;
                font-weight: 700 !important;
                transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease !important;
            }

            div[data-testid="stButton"] > button[kind="primary"] {
                background: linear-gradient(135deg, var(--academic-primary), var(--academic-secondary)) !important;
                color: #ffffff !important;
                box-shadow: 0 12px 24px rgba(30, 64, 175, 0.22);
            }

            div[data-testid="stButton"] > button[kind="secondary"] {
                background: rgba(255, 255, 255, 0.78) !important;
                color: var(--academic-text) !important;
                border-color: var(--academic-border) !important;
            }

            div[data-testid="stButton"] > button[kind="tertiary"] {
                background: rgba(15, 23, 42, 0.06) !important;
                color: var(--academic-text) !important;
                border-color: rgba(15, 23, 42, 0.08) !important;
            }

            div[data-testid="stButton"] > button:hover {
                transform: translateY(-1px);
            }

            div[data-baseweb="input"],
            div[data-baseweb="select"],
            div[data-baseweb="textarea"] {
                border-radius: var(--academic-radius) !important;
            }

            div[data-baseweb="input"] > div,
            div[data-baseweb="select"] > div,
            div[data-baseweb="textarea"] > div {
                border-radius: var(--academic-radius) !important;
                background: rgba(255, 255, 255, 0.96) !important;
                border-color: var(--academic-border) !important;
            }

            div[data-testid="stDataFrame"] {
                border-radius: var(--academic-radius);
                overflow: hidden;
                box-shadow: var(--academic-shadow);
            }
        </style>  

                """
            ,unsafe_allow_html=True)