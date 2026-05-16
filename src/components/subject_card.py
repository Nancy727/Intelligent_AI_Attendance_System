import streamlit as st
def subject_card(name, code, section, stats=None):
    html = f"""
        <div style="background:rgba(18, 22, 32, 0.72); border-left: 8px solid #00F2FF; padding:25px; border-radius: 20px; border: 1px solid rgba(0, 242, 255, 0.18); margin-bottom:20px; box-shadow:0 0 30px rgba(0, 242, 255, 0.06); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px);">
        <h3 style="margin:0; color: #F4FEFF; font-size: 1.5rem; letter-spacing:0.02em; ">{name}</h3>
        <p style="color:rgba(234,251,255,0.7); margin:10px 0;">Code : <span style="background:rgba(0,242,255,0.12); color:#00F2FF; padding:2px 8px; border-radius:5px; border:1px solid rgba(0,242,255,0.22);">{code} </span> | Section : {section}</p>
        
        """
    
    if stats:
        html+= """
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
        """
        for icon, label, value in stats:
            html+= f'<div style="background: rgba(0, 242, 255, 0.08); color:#EAFBFF; border:1px solid rgba(0,242,255,0.14); padding:5px 12px; border-radius:12px; font-size:0.9rem; box-shadow:0 0 12px rgba(0,242,255,0.06);">{icon} <b>{value}</b> {label} </div>'
        
        html+= "</div>"

    st.markdown(html, unsafe_allow_html=True)
