import streamlit as st;
from streamlit_geolocation import streamlit_geolocation;
import streamlit.components.v1 as components;

# -----------------------------------------------------------------------------
# Title & Description
# -----------------------------------------------------------------------------
st.title("Destination AQI")
st.write("Planning a trip? Use this Destination AQI to check for the real-time AQI at your preferred location!")

# -----------------------------------------------------------------------------
# HTML Code for Geocoding Interface
# -----------------------------------------------------------------------------
# This HTML string contains:
# - The necessary <head> section with CSS and JS includes for the MapTiler Geocoding Control.
# - Custom CSS to style the search and results areas.
# - JavaScript that initializes the geocoding control using the provided API key,
#   and event listeners that display geocoding results.
# Note: Double curly braces {{ }} are used to escape curly braces inside an f-string.
html_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Geocoding How to Search Places</title>
  <!-- Include the MapTiler Geocoding Control JS and CSS -->
  <script src="https://cdn.maptiler.com/maptiler-geocoding-control/v2.1.4/vanilla.umd.js"></script>
  <link href="https://cdn.maptiler.com/maptiler-geocoding-control/v2.1.4/style.css" rel="stylesheet">
  <style>
    /* Styling for the results panel */
    #results {{
      position: absolute;
      top: 48px;
      bottom: 0;
      left: 8px;
      right: 8px;
      overflow: auto;
      background: #E4ECFF;
      font-size: 0.85em;
      border-radius: 6px;
      box-shadow: 0px 15px 68px rgba(51, 51, 89, 0.15);
      padding: 8px;
    }}
    /* Styling for the search container */
    #search-container {{
      position: left;
    }}
  </style>
</head>
<body>
  <!-- Container where the geocoding search control will be attached -->
  <div id="search-container"></div>
  <!-- Container to display geocoding results -->
  <pre id="results"></pre>
  <script type="module">
    // Set the API key from the Streamlit text input
    const apiKey = "{api_key}";

    // Initialize the MapTiler Geocoding Control with the API key and attach it to the 'search-container' div
    const geocodingControl = new maptilerGeocoder.GeocodingControl({{
      apiKey,
      target: document.getElementById("search-container")
    }});

    // Event listener for when the geocoding control sends a response.
    // It displays the full response in the 'results' container.
    geocodingControl.addEventListener("response", (e) => {{
      document.getElementById("results").innerHTML =
        e.detail ? JSON.stringify(e.detail, null, 2) : "";
    }});

    // Event listener for when the user picks one of the suggestions.
    // It displays the details of the picked location.
    geocodingControl.addEventListener("pick", (e) => {{
      document.getElementById("results").innerHTML =
        e.detail ? JSON.stringify(e.detail, null, 2) : "";
    }});
  </script>
</body>
</html>
"""

# -----------------------------------------------------------------------------
# Render the HTML Component in Streamlit
# -----------------------------------------------------------------------------
# This embeds the HTML code into the Streamlit app.
# Adjust the height as needed so that the full component is visible.
components.html(html_code, height=600)