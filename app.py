import streamlit as st;
from streamlit_geolocation import streamlit_geolocation;
import streamlit.components.v1 as components
import requests;

st.set_page_config(
    page_title="PolluCheck",
    page_icon="💨",
)

def main(start):
    current_air_quality(display_and_fetch_data(location))

# Displays the latitude and longitude from the location dictionary,
# and uses them to perform a GET request.

# Parameters:
# - location: dict containing geolocation info with keys "latitude" and "longitude"

def display_and_fetch_data(location):
    
    # Extract latitude and longitude
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    
    # Check if we have valid latitude and longitude
    if latitude is None or longitude is None:
        st.error("Latitude or Longitude is missing from the location data.")
        return

    # Display the latitude and longitude on the page
    st.write("**Latitude:**", latitude)
    st.write("**Longitude:**", longitude)

    # Call API URL with the latitude and longitude.
    api_url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token=261ee3243494eb7a36e0edd4deabfcc92eee9880"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        st.success("Data fetched successfully!")
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")

def current_air_quality(payload):
    # Check if payload is None
    if payload is None:
        return st.error("Payload is missing.")
    
    # Extract AQI and city name
    aqi = payload.get("data", {}).get("aqi")
    city = payload.get("data", {}).get("city", {}).get("name")
    
    # Check if we have valid AQI and city name
    if aqi is None or city is None:
        st.error("AQI or City name is missing from the payload data.")
        return

    # Display the city name and AQI on the page
    st.write("**City:**", city)
    st.write("**AQI:**", aqi)

st.title("Check the Air Quality Index in your area");
st.write("Click The Icon Belo to Begin!")
location = streamlit_geolocation()
main(location)


st.header("Air Quality Historical Data Visualised")
components.iframe("https://lookerstudio.google.com/embed/u/0/reporting/1e01b8fc-0baa-4219-81bd-258967fc09b0/page/f7gAF", height=500)