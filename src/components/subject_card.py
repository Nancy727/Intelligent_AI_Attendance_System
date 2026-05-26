import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    with st.container(border=True):
        st.markdown(f"### {name}")
        st.caption(f"Section {section}")
        st.write(f"**Code:** {code}")

        if stats:
            stat_cols = st.columns(len(stats))
            for stat_col, (icon, label, value) in zip(stat_cols, stats):
                with stat_col:
                    st.metric(f"{icon} {label}", value)

    if footer_callback:
        footer_callback()
