import streamlit as st


def header_home():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:18px; padding:1.5rem 2rem; border:1px solid rgba(0,242,255,0.18); border-radius:1.6rem; background:rgba(255,255,255,0.03); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); box-shadow:0 0 28px rgba(0,242,255,0.08);">
            <img src='{logo_url}' style='height:96px; filter: drop-shadow(0 0 18px rgba(0,242,255,0.22));' />
            <h1 style='text-align:center; color:#EAFBFF; letter-spacing:0.22rem; text-shadow:0 0 20px rgba(0,242,255,0.18); margin-top:0.2rem;'>GAZE<br/>HUM</h1>
        </div>   
                
                """, unsafe_allow_html=True)


def header_dashboard():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:12px; padding:1rem 1.25rem; border:1px solid rgba(0,242,255,0.18); border-radius:1.35rem; background:rgba(255,255,255,0.03); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px); box-shadow:0 0 26px rgba(0,242,255,0.06);">
            <img src='{logo_url}' style='height:82px; filter: drop-shadow(0 0 18px rgba(0,242,255,0.2));' />
            <h2 style='text-align:left; color:#00F2FF; letter-spacing:0.18rem; text-shadow:0 0 16px rgba(0,242,255,0.28);'>GAZE<br/>HUM</h1>
        </div>   
                
                """, unsafe_allow_html=True)
