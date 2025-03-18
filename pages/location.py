import streamlit as st
import requests
import urllib.parse
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Destination AQI", layout="wide", initial_sidebar_state="collapsed")

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

[data-testid="stElementContainer" > data-testid="stFullScreenFrame"]{
    color: white;
    padding: 10px;
    border-radius: 10px;
}

[data-testid="stBaseButton-headerNoPadding"]{
    color: rgba(0, 0, 0, 0.5);
}

</style>
"""
# Acts as a navigation bar for the app
# aligns the links to the horizontally
col1, col2 = st.columns([1, 2])
with col1:
    st.page_link("app.py", label="Homepage", icon="🏠")
with col2:
    st.page_link("pages/location.py", label="AQI By Destination Page", icon="📍")

# Inject the CSS styling into the app
st.markdown(page_by_image, unsafe_allow_html=True)

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

def get_map(lon, lat):

    st.write("Location Map")
    
    if lon is None or lat is None:
        st.error("Latitude or Longitude is missing from the location data.")
        return
    
    try:
        # Display loading animation
        with st.spinner("Loading map...", show_time=True):
            time.sleep(7)
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
    
    # Call API URL with the latitude and longitude.
    api_url = f"https://api.waqi.info/feed/geo:{latitude};{longitude}/?token=261ee3243494eb7a36e0edd4deabfcc92eee9880"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
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
    
    # Check if have valid AQI and city name
    if aqi is None or city is None:
        st.error("AQI or City name is missing from the payload data.")
        return
    
    searched_city = st.success(city)
    time.sleep(3)
    searched_city.empty()

    air_quality = aqi_rating(aqi)

    # custom function to display centered AQI
    display_centered_metric(aqi,city,air_quality)

    # display recomemndation based on AQI
    aqi_recommendation(air_quality)

    # for debugging city and aqi
    # st.write("**City:**", city)
    # st.write("**AQI:**", aqi)

def find_location(query):
    # URL encode the query to ensure it is safe for use in a URL
    encoded_query = urllib.parse.quote(query)
    
    # call MapTiler Geocoding API to return location payload
    url = f"https://api.maptiler.com/geocoding/{encoded_query}.json"
    
    params = {
        "key": map_tiler_api_key,
    }
    
    # call GET
    response = requests.get(url, params=params)
    
    # Display the HTTP status code for debugging purposes
    # st.write("Search Location:", response.status_code)
    
    if response.status_code == 200:
        data = response.json()  # Parse the JSON data from the response
        return data
    else:
        st.error("Error fetching data from MapTiler API. Please check your API key or query parameters.")

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
    
def display_centered_metric(aqi,city,air_quality):

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
    components.html(html_code, height=220)

def aqi_recommendation(air_quality):
    """
    Provides recommendations based on the AQI value.
    """
    recommendations = {
        "Good": "Encourage children to enjoy outdoor sports. Maintain good living habits and avoid contact with allergens. Keep indoor air circulation to let children breathe fresh air. Pay attention to weather changes and avoid long-term exposure to strong sunlight.",
        "Moderate": "Pay attention to children’s health. Sensitive children should avoid strenuous exercise. If children need to go out, it is recommend to wear a protective mask. Open windows appropriately for ventilation and keep the air flowing. Use an air purifier to reduce pollutants in the air.",
        "Unhealthy for Sensitive Groups": "Limit long outdoor activities and avoid strenuous exercise. If children need to go out, try to choose a time with better air quality (early morning or evening), and it is recommended to wear a mask with a higher protection level. Reduce the time of opening windows for ventilation. Monitor the health of your child. If unwell, take a rest as soon as possible and consider seeking medical attention as appropriate. Drinking plenty of water can help keep the respiratory tract moist.",
        "Unhealthy": "Avoid all outdoor activities, and carry out low-intensity indoor activities appropriately. Close doors and windows, and use air purifiers. If children must go out, it is recommended to wear N95 or KN95 level protective masks. Rehydrate and use saline to clean the nasal cavity. Pay close attention to whether your child has the following symptoms: persistent cough, sore throat; shortness of breath, chest tightness; red and swollen eyes or discomfort; dizziness, fatigue. If the symptoms worsen, please seek medical attention in time, especially for children with asthma, who need to carry an inhaler with them.",
        "Unknown": "Air quality is considered satisfactory, and air pollution poses little or no risk."
    }

    if air_quality == "Good":
        st.success(recommendations.get("Good"))
    elif air_quality == "Moderate":
        st.warning(recommendations.get("Moderate"))
    elif air_quality == "Unhealthy for Sensitive Groups":
        st.error(recommendations.get("Unhealthy for Sensitive Groups"))
    elif air_quality == "Unhealthy":
        st.error(recommendations.get("Unhealthy"))
    else:
        st.error(recommendations.get("Unknown"))

st.title("Destination AQI")
st.write(
    """
    Planning a trip? Use this Destination AQI to check for the real-time AQI at your preferred location!
    """
)

map_tiler_api_key = "URNI3k74PFnNil4zQ5WJ"
weather_aqi_api_key = "261ee3243494eb7a36e0edd4deabfcc92eee9880"
geoApify_api_key = "6f655e8fd34b405e89d8657aa0a12d41"

query = st.text_input("Enter location to search. Click the Search button to check the AQI at your destination.", value="Kuala Lumpur")

if st.button("Search"):
    destination_aqi(query)
    st.caption("Powered by MapTiler, Waqi.info, and GeoApify")

st.header("Forecasted Air Quality")
st.write("Use the available filters to explore search the forecasted air quality. Data sourced from Looker Studio.")
components.iframe("https://lookerstudio.google.com/embed/reporting/32539d04-bab9-4b72-9014-345f50b5db98/page/lNzCF", height=750)




