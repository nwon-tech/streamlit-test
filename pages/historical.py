import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Historical AQI Page", 
    layout="wide", 
    initial_sidebar_state="collapsed"
                   )

# Background styling for the app
page_by_image = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    opacity: 1;
    background-size: cover;
    background-image: url("https://images.unsplash.com/photo-1534083708493-62fff9d96ecc?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
}

[data-testid="stHeader"] {
    background-color: transparent;
}

[data-testid="stMarkdownContainer"]{
    color: white;
    padding: 10px;
    border-radius: 10px;
}

[data-testid="stBaseButton-headerNoPadding"]{
    color: rgba(0, 0, 0, 0.5);
}

[data-testid="stHeadingWithActionElements"]>h1{
    text-align: center
}

[data-testid="stCaptionContainer"]{
    text-align: center
    
}
</style>
"""


# Acts as a navigation bar for the app
# aligns the links to the horizontally
col1, col2, col3 = st.columns([1, 2, 3])
with col1:
    st.page_link("app.py", label="Homepage", icon="🏠")
with col2:
    st.page_link("pages/location.py", label="AQI By Destination Page", icon="📍")
with col3:
    st.page_link("pages/historical.py", label="AQI Historical Data Page", icon="📜")

# Main app interface
st.title("PolluCheck")
st.caption("_Stay Informed, Stay Healthy._")
st.divider()

# Embed an iframe for additional historical data visualisation
st.header("Air Quality Historical Data Visualised")
st.write("Use the available filters to explore historical air quality data. Data sourced from Looker Studio.")
components.iframe("https://lookerstudio.google.com/embed/u/0/reporting/1e01b8fc-0baa-4219-81bd-258967fc09b0/page/f7gAF", height=3500)


