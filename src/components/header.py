import streamlit as st
from pathlib import Path


LOGO_PATH = Path(__file__).resolve().parents[2] / "assets" / "Screenshot 2026-05-15 152619.png"


def _render_brand(title, subtitle, compact=False):
    image_width = 88 if compact else 112
    title_tag = "h2" if compact else "h1"

    with st.container(border=True):
        left, right = st.columns([1, 4], vertical_alignment="center", gap="medium")

        with left:
            if LOGO_PATH.exists():
                st.image(str(LOGO_PATH), width=image_width)
            else:
                st.markdown("<div class='academic-pill'>AI Attendance</div>", unsafe_allow_html=True)

        with right:
            st.markdown("<div class='academic-pill'>Modern Academic Portal</div>", unsafe_allow_html=True)
            st.markdown(
                f"<{title_tag} style='margin:0.35rem 0 0.15rem 0; color:#0f172a;'>{title}</{title_tag}>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='academic-muted' style='margin:0;'>{subtitle}</p>",
                unsafe_allow_html=True,
            )


def header_home():
    _render_brand(
        "Intelligent AI Attendance",
        "A student-friendly, academic dashboard for face, voice, and subject-based attendance.",
        compact=False,
    )


def header_dashboard():
    _render_brand(
        "Intelligent AI Attendance",
        "Manage classes, review attendance, and keep student flows organized from one clean portal.",
        compact=True,
    )
