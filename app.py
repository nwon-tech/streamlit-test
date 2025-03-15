import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import streamlit.components.v1 as components
import requests

# Set the page title and icon (must be called first)
st.set_page_config(
    page_title="PolluCheck",
    page_icon="💨",
)

# Background styling for the app
page_by_image = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    opacity: 1;
    background-size: cover;
    background-image: url("https://images.unsplash.com/photo-1599148401012-60bd30ff1967?q=80&w=1527&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
}

[data-testid="stHeader"] {
    background-color: transparent;
}

[data-testid="stSidebarContent"]{
    background: rgba(51, 170, 51, 1);
}
</style>
"""

# Inject the CSS styling into the app
st.markdown(page_by_image, unsafe_allow_html=True)

def aqi_rating(aqi):
    """
    Converts the AQI value to a qualitative rating.
    """
    if aqi >= 0 and aqi <= 50:
        return "Good"
    elif aqi >= 51 and aqi <= 100:
        return "Moderate"
    elif aqi >= 101 and aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi >= 151 and aqi <= 200:
        return "Unhealthy"
    elif aqi >= 201 and aqi <= 300:
        return "Very Unhealthy"
    elif aqi >= 301:
        return "Hazardous"
    else:
        return "Unknown"
    
def display_and_fetch_data(location):
    """
    Extracts latitude and longitude from the geolocation data,
    then fetches air quality data using a GET request.
    """
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    
    # Ensure valid latitude and longitude are provided
    if latitude is None or longitude is None:
        st.error("Latitude or Longitude is missing from the location data.")
        return

    # Build API URL with the given coordinates
    api_url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token=261ee3243494eb7a36e0edd4deabfcc92eee9880"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")

def display_centered_metric(aqi,city,air_quality):
    """
    Creates a custom HTML block to display the Air Quality Index (AQI)
    in a centered layout, then embeds it in the Streamlit app.
    """
    # HTML code using inline CSS for centering and styling
    html_code = f"""
    <div style="display: flex; align-items: center; justify-content: center; height: 600px;">
        <div style="background: transparent; padding: 20px; text-align: center; color: white; font-family: Sans-Serif; font-weight: bold; border-radius: 10px; background: rgba(0, 0, 0, 0.5);">
            <h2 style="margin: 0;">{city}</h2>
            <h2 style="color: white;">Current Air Quality</h2>
            <p style="font-size: 48px; margin: 10px 0;">{aqi}</p>
            <h3 style="color: white;">{air_quality}</h3>
        </div>
    </div>
    """
    # Use Streamlit's components.html to render the custom HTML component.
    # The height parameter ensures proper layout in the app.
    components.html(html_code, height=180)

def current_air_quality(payload):
    """
    Extracts and displays the city name and AQI from the API response.
    It uses the custom HTML component to display the AQI in a centered manner.
    """
    if payload is None:
        aqi = payload.get("data", {}).get("aqi")
        city = payload.get("data", {}).get("city", {}).get("name")
    
    aqi = payload.get("data", {}).get("aqi")
    city = payload.get("data", {}).get("city", {}).get("name")
    
    if aqi is None or city is None:
        st.error("AQI or City name is missing from the payload data.")
        return
    
    air_quality = aqi_rating(aqi)
    
    # custom function to display centered AQI
    display_centered_metric(aqi,city,air_quality)

# Main app interface
st.title("Check the Air Quality Index in your area")
st.write("Click The Icon Below to Begin!")

# Fetch geolocation and air quality data
location = streamlit_geolocation()
data = display_and_fetch_data(location)
current_air_quality(data)

# Embed an iframe for additional historical data visualisation
st.header("Air Quality Historical Data Visualised")
components.iframe("https://lookerstudio.google.com/embed/u/0/reporting/1e01b8fc-0baa-4219-81bd-258967fc09b0/page/f7gAF", height=500)
