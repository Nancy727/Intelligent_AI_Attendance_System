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
                --academic-surface: rgba(255, 255, 255, 0.74);
                --academic-surface-strong: rgba(255, 255, 255, 0.96);
                --academic-surface-soft: rgba(255, 255, 255, 0.58);
                --academic-border: rgba(148, 163, 184, 0.24);
                --academic-text: #0f172a;
                --academic-muted: #475569;
                --academic-radius: 18px;
                --academic-radius-sm: 14px;
                --academic-shadow: 0 18px 40px rgba(15, 23, 42, 0.09);
                --academic-shadow-hover: 0 24px 52px rgba(15, 23, 42, 0.14);
                --academic-glow: 0 0 0 1px rgba(255, 255, 255, 0.52) inset;
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
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.90), rgba(255, 255, 255, 0.72)) !important;
                border: 1px solid var(--academic-border) !important;
                box-shadow: var(--academic-shadow) !important;
                padding: 1.25rem 1.25rem !important;
                backdrop-filter: blur(18px);
                -webkit-backdrop-filter: blur(18px);
                transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease !important;
                overflow: hidden;
                position: relative;
            }

            .academic-card::before,
            div[data-testid="stVerticalBlockBorderWrapper"]::before {
                content: '';
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg, rgba(30, 64, 175, 0.08), rgba(14, 165, 233, 0.02) 42%, transparent 72%);
                pointer-events: none;
                opacity: 0.65;
            }

            .academic-card:hover,
            div[data-testid="stVerticalBlockBorderWrapper"]:hover {
                transform: translateY(-3px);
                box-shadow: var(--academic-shadow-hover) !important;
                border-color: rgba(30, 64, 175, 0.22) !important;
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
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.72));
                border: 1px solid var(--academic-border);
                border-radius: var(--academic-radius);
                padding: 1rem 1.05rem;
                box-shadow: var(--academic-shadow);
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
            }

            div[data-testid="stButton"] > button {
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 0.45rem !important;
                min-height: 2.8rem !important;
                border-radius: var(--academic-radius-sm) !important;
                border: 1px solid transparent !important;
                padding: 0.8rem 1rem !important;
                font-weight: 700 !important;
                line-height: 1.2 !important;
                white-space: normal !important;
                text-align: center !important;
                overflow-wrap: anywhere !important;
                box-sizing: border-box !important;
                transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease, border-color 0.18s ease, opacity 0.18s ease !important;
                box-shadow: var(--academic-glow);
            }

            div[data-testid="stButton"] {
                margin-bottom: 0.25rem;
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
                transform: translateY(-2px);
                box-shadow: 0 18px 30px rgba(15, 23, 42, 0.12);
            }

            div[data-testid="stButton"] > button:active {
                transform: translateY(0);
                box-shadow: 0 10px 18px rgba(15, 23, 42, 0.10);
            }

            div[data-testid="stButton"] > button:focus-visible {
                outline: 3px solid rgba(14, 165, 233, 0.26) !important;
                outline-offset: 2px;
            }

            div[data-testid="stButton"] > button:disabled {
                opacity: 0.58 !important;
                transform: none !important;
                box-shadow: none !important;
            }

            div[data-testid="stButton"] > button[kind="secondary"]:hover {
                background: rgba(255, 255, 255, 0.92) !important;
                border-color: rgba(30, 64, 175, 0.20) !important;
            }

            div[data-testid="stButton"] > button[kind="tertiary"]:hover {
                background: rgba(15, 23, 42, 0.08) !important;
                border-color: rgba(15, 23, 42, 0.12) !important;
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

            .ui-skeleton {
                position: relative;
                overflow: hidden;
                background: rgba(148, 163, 184, 0.16);
                border-radius: 999px;
            }

            .ui-skeleton::after {
                content: '';
                position: absolute;
                inset: 0;
                transform: translateX(-100%);
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.72), transparent);
                animation: skeleton-shimmer 1.4s infinite;
            }

            .ui-skeleton-block {
                border-radius: 16px;
            }

            .ui-skeleton-line {
                height: 0.9rem;
            }

            .ui-skeleton-chip {
                height: 1.4rem;
                width: 5.5rem;
            }

            @keyframes skeleton-shimmer {
                100% {
                    transform: translateX(100%);
                }
            }
        </style>  

                """
            ,unsafe_allow_html=True)