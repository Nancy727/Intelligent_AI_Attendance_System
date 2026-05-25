import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div class="academic-card" style="margin-bottom: 1rem;">
        <div class="academic-pill" style="margin-bottom: 0.8rem;">Section {section}</div>
        <h3 style="margin:0; color:#0f172a; font-size:1.25rem;">{name}</h3>
        <p style="color:#475569; margin:0.45rem 0 0.9rem 0;">Code: <span style="background:rgba(30,64,175,0.08); color:#1e40af; padding:0.2rem 0.55rem; border-radius:999px; font-weight:700;">{code}</span></p>
        
        """
    
    if stats:
        html+= """
        <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.9rem;">
        """
        for icon, label, value in stats:
            html+= f'<div style="background:rgba(14,165,233,0.08); color:#0f172a; padding:0.45rem 0.75rem; border-radius:12px; font-size:0.92rem;">{icon} <b>{value}</b> {label}</div>'
        
        html+= "</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
