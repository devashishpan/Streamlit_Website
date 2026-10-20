import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
    "Get Help": "https://google.com",
    "Report a Bug": "mailto:dk1998rpl@gmail.com",
    "About": "This is a sample Streamlit app.",
    }
)

# Navigation Settings
profile_page = st.Page("pages/Profile.py", title="Profile", icon="🏠")
portfolio_page = st.Page("pages/Portfolio.py", title="Portfolio", icon="📊")
pg = st.navigation([profile_page, portfolio_page], position="top")
pg.run()
