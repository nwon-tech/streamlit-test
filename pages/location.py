import streamlit as st
import requests
import urllib.parse
import time

st.set_page_config(page_title="Destination AQI", layout="wide")

def destination_aqi(search_query):
    # Call the find_location function to get the long and lat
    dest_payload = find_location(search_query)

    lat = dest_payload.get("features")[0].get("geometry").get("coordinates")[1]
    lon = dest_payload.get("features")[0].get("geometry").get("coordinates")[0]

    # Pass it to the get_aqi function to get the AQI
    dest_aqi = get_aqi(lon, lat)
    current_air_quality(dest_aqi)

    # Generate Geo Map
    get_map(lon, lat)


def get_map(lon, lat):
    
    if lon is None or lat is None:
        st.error("Latitude or Longitude is missing from the location data.")
        return
    
    try:
        # Display loading animation
        with st.spinner("Loading map...", show_time=True):
            time.sleep(5)
            # Display the map using GeoApify Static Maps API
            st.image(f"https://maps.geoapify.com/v1/staticmap?style=osm-bright-smooth&width=600&height=400&center=lonlat:{lon},{lat}&zoom=12&marker=lonlat:{lat},{lon};color:%23ff0000;size:medium&apiKey=6f655e8fd34b405e89d8657aa0a12d41")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve data: {e}")

def get_aqi(lon, lat):
    # Extract latitude and longitude
    latitude = lat
    longitude = lon
    
    # Check if we have valid latitude and longitude
    if latitude is None or longitude is None:
        st.error("Latitude or Longitude is missing from the location data.")
        return

    # Display the latitude and longitude on the page
    # st.write("**Latitude:**", latitude)
    # st.write("**Longitude:**", longitude)

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

def find_location(query):
    # URL encode the query to ensure it is safe for use in a URL
    encoded_query = urllib.parse.quote(query)
    
    # call MapTiler Geocoding API to return location payload
    url = f"https://api.maptiler.com/geocoding/{encoded_query}.json"
    
    params = {
        "key": map_tiler_api_key,
    }
    
    # ---------------------------
    # Make the GET request to the MapTiler Geocoding API
    # ---------------------------
    response = requests.get(url, params=params)
    
    # Display the HTTP status code for debugging purposes
    st.write("Search Location:", response.status_code)
    
    # ---------------------------
    # Check if the request was successful and display the JSON response
    # ---------------------------
    if response.status_code == 200:
        data = response.json()  # Parse the JSON data from the response
        return data
    else:
        st.error("Error fetching data from MapTiler API. Please check your API key or query parameters.")

# ---------------------------
# App title and description
# ---------------------------
st.title("Destination AQI")
st.write(
    """
    Planning a trip? Use this Destination AQI to check for the real-time AQI at your preferred location!
    """
)

map_tiler_api_key = "URNI3k74PFnNil4zQ5WJ"
weather_aqi_api_key = "261ee3243494eb7a36e0edd4deabfcc92eee9880"
geoApify_api_key = "6f655e8fd34b405e89d8657aa0a12d41"

query = st.text_input("Enter location to search:", value="Kuala Lumpur")

if st.button("Search"):
    destination_aqi(query)
    # # URL encode the query to ensure it is safe for use in a URL
    # encoded_query = urllib.parse.quote(query)
    
    # # call MapTiler Geocoding API to return location payload
    # url = f"https://api.maptiler.com/geocoding/{encoded_query}.json"
    
    # params = {
    #     "key": map_tiler_api_key,
    # }
    
    # # ---------------------------
    # # Make the GET request to the MapTiler Geocoding API
    # # ---------------------------
    # response = requests.get(url, params=params)
    
    # # Display the HTTP status code for debugging purposes
    # st.write("Search Location:", response.status_code)
    
    # # ---------------------------
    # # Check if the request was successful and display the JSON response
    # # ---------------------------
    # if response.status_code == 200:
    #     data = response.json()  # Parse the JSON data from the response
    #     return data
    # else:
    #     st.error("Error fetching data from MapTiler API. Please check your API key or query parameters.")

    # st.write(data.get("features")[0].get("geometry").get("coordinates"))



