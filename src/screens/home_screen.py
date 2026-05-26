import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
def home_screen():


    header_home()
    style_background_home()
    style_base_layout()

    st.markdown(
        """
        <style>
            div[data-testid="stVerticalBlock"]:has(.home-card-anchor-student),
            div[data-testid="stVerticalBlock"]:has(.home-card-anchor-teacher) {
                will-change: transform;
                transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
            }

            div[data-testid="stVerticalBlock"]:has(.home-card-anchor-student):hover,
            div[data-testid="stVerticalBlock"]:has(.home-card-anchor-teacher):hover {
                transform: translateY(-6px) scale(1.01);
                box-shadow: 0 28px 60px rgba(15, 23, 42, 0.14) !important;
                border-color: rgba(30, 64, 175, 0.22) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class='academic-muted' style='text-align:center; margin-top:0.5rem;'>Choose the portal that matches your role. The experience is optimized for focus, clarity, and fast access on laptops and tablets.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.25rem;'></div>", unsafe_allow_html=True)


    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("<div class='home-card-anchor-student'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<div class='academic-pill'>Student Portal</div>", unsafe_allow_html=True)
            st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=120)
            st.subheader("I'm a Student")
            st.write("Check your attendance, enroll in subjects, and use face or voice login in a streamlined flow.")
            st.markdown("<ul class='academic-muted' style='padding-left: 1.1rem; margin-top: 0.75rem;'><li>Fast FaceID access</li><li>Subject enrollment in seconds</li><li>Attendance summaries at a glance</li></ul>", unsafe_allow_html=True)
            if st.button('Open Student Portal', type='primary', width='stretch'):
                st.session_state['login_type']='student'
                st.rerun()

    with col2:
        st.markdown("<div class='home-card-anchor-teacher'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<div class='academic-pill'>Teacher Portal</div>", unsafe_allow_html=True)
            st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)
            st.subheader("I'm a Teacher")
            st.write("Create subjects, manage attendance, and review records from a clean classroom dashboard.")
            st.markdown("<ul class='academic-muted' style='padding-left: 1.1rem; margin-top: 0.75rem;'><li>Face and voice attendance workflows</li><li>Subject and enrollment management</li><li>Attendance records in one place</li></ul>", unsafe_allow_html=True)
            if st.button('Open Teacher Portal', type='primary', width='stretch'):
                st.session_state['login_type']='teacher'
                st.rerun()

    footer_home()