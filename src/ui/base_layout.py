import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                :root {
                    --bg-main: #0E1117;
                    --bg-surface: rgba(18, 22, 32, 0.72);
                    --bg-surface-strong: rgba(12, 16, 24, 0.92);
                    --border-cyan: rgba(0, 242, 255, 0.22);
                    --accent-cyan: #00F2FF;
                    --text-primary: #EAFBFF;
                    --text-secondary: rgba(234, 251, 255, 0.72);
                }

                .stApp {
                    background:
                        radial-gradient(circle at top left, rgba(0, 242, 255, 0.14), transparent 28%),
                        radial-gradient(circle at bottom right, rgba(0, 242, 255, 0.08), transparent 22%),
                        linear-gradient(180deg, #11151d 0%, #0E1117 48%, #090c11 100%) !important;
                    color: var(--text-primary) !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background: rgba(255, 255, 255, 0.02) !important;
                    border: 1px solid rgba(0, 242, 255, 0.12) !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    padding:2.5rem !important;
                    border-radius: 1.75rem !important;
                    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.35) !important;
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                :root {
                    --bg-main: #0E1117;
                    --bg-surface: rgba(18, 22, 32, 0.72);
                    --bg-surface-strong: rgba(12, 16, 24, 0.92);
                    --border-cyan: rgba(0, 242, 255, 0.22);
                    --accent-cyan: #00F2FF;
                    --text-primary: #EAFBFF;
                    --text-secondary: rgba(234, 251, 255, 0.72);
                }

                .stApp {
                    background:
                        radial-gradient(circle at top left, rgba(0, 242, 255, 0.14), transparent 28%),
                        radial-gradient(circle at bottom right, rgba(0, 242, 255, 0.08), transparent 22%),
                        linear-gradient(180deg, #11151d 0%, #0E1117 48%, #090c11 100%) !important;
                    color: var(--text-primary) !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap');

                
         /* Hide Top Bar of streamlit */
                
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top:1.5rem !important;
                max-width: 1180px;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(0, 242, 255, 0.14), transparent 28%),
                    radial-gradient(circle at bottom right, rgba(0, 242, 255, 0.08), transparent 22%),
                    linear-gradient(180deg, #11151d 0%, #0E1117 48%, #090c11 100%) !important;
                color: #EAFBFF !important;
            }

            body {
                color: #EAFBFF !important;
                font-family: 'Montserrat', sans-serif !important;
            }

            h1 {
                font-family: 'Montserrat', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 !important;
                margin-bottom:0rem !important;
                letter-spacing: 0.02em;
                color: #F3FEFF !important;
                text-shadow: 0 0 18px rgba(0, 242, 255, 0.18);
            }
                

            h2 {
                font-family: 'Montserrat', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
                color: #D7FCFF !important;
                text-shadow: 0 0 16px rgba(0, 242, 255, 0.14);
            }
                
            h3, h4, p, label, span, div {
                font-family: 'Montserrat', sans-serif;
            }

            h3, h4 {
                color: #EAFBFF !important;
            }

            p, label, .stMarkdown, .stCaption {
                color: rgba(234, 251, 255, 0.76) !important;
            }
                

            div[data-testid="stButton"] > button{
                border-radius: 1.1rem !important;
                background: linear-gradient(135deg, rgba(0, 242, 255, 0.18), rgba(0, 242, 255, 0.06)) !important;
                color: #F4FEFF !important;
                padding: 10px 20px !important;
                border: 1px solid rgba(0, 242, 255, 0.48) !important;
                box-shadow: 0 0 18px rgba(0, 242, 255, 0.14), inset 0 1px 0 rgba(255,255,255,0.08) !important;
                transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease !important;
                font-family: 'Montserrat', sans-serif !important;
                letter-spacing: 0.02em !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                }

            div[data-testid="stButton"] > button[kind="secondary"],
            div[data-testid="stButton"] > button[kind="tertiary"]{
                border-radius: 1.1rem !important;
                background: rgba(255, 255, 255, 0.03) !important;
                color: #EAFBFF !important;
                padding: 10px 20px !important;
                border: 1px solid rgba(0, 242, 255, 0.18) !important;
                box-shadow: 0 0 12px rgba(0, 242, 255, 0.08) !important;
                transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease !important;
                font-family: 'Montserrat', sans-serif !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                }

            div[data-testid="stButton"] > button:hover{
                transform: translateY(-1px) scale(1.01) !important;
                border-color: rgba(0, 242, 255, 0.85) !important;
                box-shadow: 0 0 22px rgba(0, 242, 255, 0.28) !important;
                }

            div[data-testid="stButton"] > button:focus-visible{
                outline: none !important;
                box-shadow: 0 0 0 2px rgba(0, 242, 255, 0.22), 0 0 28px rgba(0, 242, 255, 0.3) !important;
            }

            div[data-testid="stTextInput"] input,
            div[data-testid="stTextArea"] textarea,
            div[data-testid="stSelectbox"] div,
            div[data-testid="stFileUploaderDropzone"],
            div[data-testid="stCameraInput"] {
                background: rgba(255, 255, 255, 0.035) !important;
                color: #EAFBFF !important;
                border: 1px solid rgba(0, 242, 255, 0.16) !important;
                border-radius: 1rem !important;
                box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 0 16px rgba(0, 242, 255, 0.06) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
            }

            div[data-testid="stCameraInput"] {
                position: relative !important;
                overflow: hidden !important;
                border-color: rgba(0, 242, 255, 0.32) !important;
            }

            div[data-testid="stCameraInput"]::before {
                content: '';
                position: absolute;
                inset: 0;
                pointer-events: none;
                background:
                    linear-gradient(rgba(0, 242, 255, 0.16) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0, 242, 255, 0.16) 1px, transparent 1px),
                    radial-gradient(circle at center, transparent 0 42%, rgba(0, 242, 255, 0.08) 100%);
                background-size: 28px 28px, 28px 28px, 100% 100%;
                mix-blend-mode: screen;
                opacity: 0.9;
                z-index: 2;
            }

            div[data-testid="stCameraInput"]::after {
                content: '';
                position: absolute;
                left: 0;
                right: 0;
                top: 0;
                height: 4px;
                background: linear-gradient(90deg, transparent, rgba(0, 242, 255, 0.95), transparent);
                box-shadow: 0 0 18px rgba(0, 242, 255, 0.7);
                animation: gaze-scan 2.8s linear infinite;
                z-index: 3;
            }

            @keyframes gaze-scan {
                0% { transform: translateY(0); opacity: 0.2; }
                10% { opacity: 1; }
                50% { opacity: 0.95; }
                100% { transform: translateY(100%); opacity: 0.2; }
            }

            div[data-testid="stDataFrame"] {
                background: rgba(255,255,255,0.03) !important;
                border: 1px solid rgba(0, 242, 255, 0.12) !important;
                border-radius: 1rem !important;
                overflow: hidden !important;
            }
        </style>  

                """
            ,unsafe_allow_html=True)