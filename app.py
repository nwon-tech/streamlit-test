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
    background: rgb(128, 0, 0);
}
</style>
"""

# pg = st.navigation([st.Page("app.py", icon="🏠"), st.Page("pages/location.py", icon="📚")])

# check_current_aqi = st.Page("app.py", title="Check Your Current AQI | Pollc", icon=":material/home:")
# check_destination_aqi = st.Page("location.py", title="Check Your Destination AQI", icon=":material/gps_fixed:")

# pg = st.navigation([check_current_aqi, check_destination_aqi])
# st.set_page_config(page_title="Home ", page_icon=":material/edit:")
# pg.run()

# Inject the CSS styling into the app
st.markdown(page_by_image, unsafe_allow_html=True)

# Display a notification at the top of the page to notify user that data is sourced from open source
st.info(
    "All data is sourced from The World Air Quality Index Project. "
    "Please note that while the data is openly sourced, users should still take necessary precautions.",icon="ℹ️"
)

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
    else:
        return "Unknown"

def aqi_recommendation(rating):
    """
    Provides recommendations based on the AQI value.
    """
    if rating == "Good":
        return "Air quality is considered satisfactory, and air pollution poses little or no risk."
    
    
def display_and_fetch_data(location):
    """
    Extracts latitude and longitude from the geolocation data,
    then fetches air quality data using a GET request.
    """
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    
    # Ensure valid latitude and longitude are provided
    if latitude is None or longitude is None:
        st.error("Kindly select the location button to check the air quality.")
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

def placeholder_display_and_fetch_data(location):
    """
    Extracts latitude and longitude from the geolocation data,
    then fetches air quality data using a GET request.
    """
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    
    # Ensure valid latitude and longitude are provided
    if latitude is None or longitude is None:
        st.error("Kindly select the location button to check the air quality.")
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
    <div style="display: flex; align-items: center; justify-content: center; height: 200px;">
        <div style="background: transparent; padding: 20px; text-align: center; color: white; font-family: Sans-Serif; font-weight: bold; border-radius: 10px; background: rgba(0, 0, 0, 0.5);">
            <h3 style="margin: 0;">{city}</h3>
            <h4 style="color: white;">Current Air Quality</h4>
            <p style="font-size: 48px; margin: 10px 0;">{aqi}</p>
            <h3 style="color: white;">{air_quality}</h3>
        </div>
    </div>
    """
    # Use Streamlit's components.html to render the custom HTML component.
    # The height parameter ensures proper layout in the app.
    components.html(html_code, height=220)

def current_air_quality(payload):
    """
    Extracts and displays the city name and AQI from the API response.
    It uses the custom HTML component to display the AQI in a centered manner.
    """
    # if payload is None:
    #     aqi = payload.get("data", {}).get("aqi")
    #     city = payload.get("data", {}).get("city", {}).get("name")
    
    aqi = payload.get("data", {}).get("aqi")
    city = payload.get("data", {}).get("city", {}).get("name")
    
    if aqi is None or city is None:
        return
    
    air_quality = aqi_rating(aqi)
    
    # custom function to display centered AQI
    display_centered_metric(aqi,city,air_quality)

# Main app interface
# st.title("Check the Air Quality Index in your area")
st.write("Click The Icon Below to Begin!")

# Fetch geolocation and air quality data
location = streamlit_geolocation()
data = display_and_fetch_data(location)

if data is not None:
    # Display the current air quality data
    # if data is not None:
    #     current_air_quality(data)
    # else:
    #     st.error("Failed to retrieve data.")
    current_air_quality(data)
else:
    data = {
        "latitude": 3.139,
        "longitude": 101.6841
    }
    current_air_quality(data)

# Embed an iframe for additional historical data visualisation
# st.header("Air Quality Historical Data Visualised")
# components.iframe("https://lookerstudio.google.com/embed/u/0/reporting/1e01b8fc-0baa-4219-81bd-258967fc09b0/page/f7gAF", height=500)
