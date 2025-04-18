import streamlit as st
from streamlit_geolocation import streamlit_geolocation
import streamlit.components.v1 as components
import requests

# Set the page title and icon (must be called first)
st.set_page_config(
    page_title="PolluCheck",
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
    text-align: center;
}

[data-testid="stCaptionContainer"]{
    text-align: center;
    color: white;
}

[data-testid="stImageContainer"]{
    margin: auto;
}

[data-testid="stAlert"]{
    opacity: 1;
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

    if (air_quality == "Good"):
        html_code = f"""
    <div style="display: flex; align-items: center; justify-content: center; height: 200px;">
        <div style="background: transparent; padding: 20px; text-align: center; color: white; font-family: Sans-Serif; font-weight: bold; border-radius: 10px; background: rgba(143,185,53,0.5);">
            <h3 style="margin: 0;">{city}</h3>
            <h4 style="color: white;">Current Air Quality</h4>
            <p style="font-size: 48px; margin: 10px 0;">{aqi}</p>
            <h3 style="color: white;">{air_quality}</h3>
        </div>
    </div>
    """
    elif (air_quality == "Moderate"):
        html_code = f"""
    <div style="display: flex; align-items: center; justify-content: center; height: 200px;">
        <div style="background: transparent; padding: 20px; text-align: center; color: white; font-family: Sans-Serif; font-weight: bold; border-radius: 10px; background: rgba(230,226,46,0.5);">
            <h3 style="margin: 0;">{city}</h3>
            <h4 style="color: white;">Current Air Quality</h4>
            <p style="font-size: 48px; margin: 10px 0;">{aqi}</p>
            <h3 style="color: white;">{air_quality}</h3>
        </div>
    </div>
    """
    elif (air_quality == "Unhealthy for Sensitive Groups"):
        html_code = f"""
    <div style="display: flex; align-items: center; justify-content: center; height: 200px;">
        <div style="background: transparent; padding: 20px; text-align: center; color: white; font-family: Sans-Serif; font-weight: bold; border-radius: 10px; background: rgba(224,156,59,0.5);">
            <h3 style="margin: 0;">{city}</h3>
            <h4 style="color: white;">Current Air Quality</h4>
            <p style="font-size: 48px; margin: 10px 0;">{aqi}</p>
            <h3 style="color: white;">{air_quality}</h3>
        </div>
    </div>
    """
    else:
        html_code = f"""
    <div style="display: flex; align-items: center; justify-content: center; height: 200px;">
        <div style="background: transparent; padding: 20px; text-align: center; color: white; font-family: Sans-Serif; font-weight: bold; border-radius: 10px; background: rgba	(230,71,71,0.5);">
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
        "Good": "Recommendation: Encourage children to enjoy outdoor sports. Maintain good living habits and avoid contact with allergens. Keep indoor air circulation to let children breathe fresh air. Pay attention to weather changes and avoid long-term exposure to strong sunlight.",
        "Moderate": "Recommendation: Pay attention to children’s health. Sensitive children should avoid strenuous exercise. If children need to go out, it is recommend to wear a protective mask. Open windows appropriately for ventilation and keep the air flowing. Use an air purifier to reduce pollutants in the air.",
        "Unhealthy for Sensitive Groups": "Recommendation: Limit long outdoor activities and avoid strenuous exercise. If children need to go out, try to choose a time with better air quality (early morning or evening), and it is recommended to wear a mask with a higher protection level. Reduce the time of opening windows for ventilation. Monitor the health of your child. If unwell, take a rest as soon as possible and consider seeking medical attention as appropriate. Drinking plenty of water can help keep the respiratory tract moist.",
        "Unhealthy": "Recommendation: Avoid all outdoor activities, and carry out low-intensity indoor activities appropriately. Close doors and windows, and use air purifiers. If children must go out, it is recommended to wear N95 or KN95 level protective masks. Rehydrate and use saline to clean the nasal cavity. Pay close attention to whether your child has the following symptoms: persistent cough, sore throat; shortness of breath, chest tightness; red and swollen eyes or discomfort; dizziness, fatigue. If the symptoms worsen, please seek medical attention in time, especially for children with asthma, who need to carry an inhaler with them.",
        "Unknown": "Recommendation: Air quality is considered satisfactory, and air pollution poses little or no risk."
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

def current_air_quality(payload):

    # keep for debugging
    #     aqi = payload.get("data", {}).get("aqi")
    #     city = payload.get("data", {}).get("city", {}).get("name")
    
    aqi = payload.get("data", {}).get("aqi")
    city = payload.get("data", {}).get("city", {}).get("name")
    
    if aqi is None or city is None:
        return
    
    air_quality = aqi_rating(aqi)
    
    # custom function to display centered AQI
    display_centered_metric(aqi,city,air_quality)

    # display recomemndation based on AQI
    aqi_recommendation(air_quality)

# Main app interface
st.title("PolluCheck")
st.caption("_Stay Informed, Stay Healthy._")
st.divider()

# Display a notification at the top of the page to notify user that data is sourced from open source
st.info(
    "All data is sourced from The World Air Quality Index Project. "
    "Please note that while the data is openly sourced, users should still take necessary precautions.",icon="ℹ️"
)

st.header("Check the Air Quality Index in your Area")
st.write("Click The Icon ⌖ Below to Begin!")

# Fetch geolocation and air quality data
location = streamlit_geolocation()
data = display_and_fetch_data(location)

if data is not None:
    current_air_quality(data)
else:
    data = {
        "latitude": 3.139,
        "longitude": 101.6841
    }
    current_air_quality(data)

st.subheader("What does the recommendation mean?")
st.image("air-quality-recomm.jpg")