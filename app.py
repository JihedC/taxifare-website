import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static

st.markdown('# Plan your Taxifare trip!')

# Get user inputs, for now numeric for location lat and lon
pickup_date = st.sidebar.date_input('Choose your pickup date')
pickup_time = st.sidebar.time_input('Choose your pickup time') # This is only hh:mm, need to send hh:mm:ss
pickup_longitude = st.sidebar.number_input('Choose your pickup longitude', value=40.7614327, step=0.000001, key=1)
pickup_latitude = st.sidebar.number_input('Choose your pickup latitude', value=-73.9798156, step=0.000001, key=2)
dropoff_longitude = st.sidebar.number_input('Choose your dropoff longitude', value=40.6513111, step=0.000001, key=3)
dropoff_latitude = st.sidebar.number_input('Choose your dropoff latitude', value=-73.8803331, step=0.000001, key=4)
passenger_count = st.sidebar.slider('Choose the number of passengers,', min_value=1, max_value=6, step=1, key=5)

if st.sidebar.button("Get fare"):
    try:
        # Generate request based on input
        url = 'https://taxifare.lewagon.ai/predict'

        params = {'pickup_datetime': f"{pickup_date} {pickup_time.strftime('%H:%M:%S')}",
                  'pickup_longitude': pickup_longitude,
                  'pickup_latitude': pickup_latitude,
                  'dropoff_longitude': dropoff_longitude,
                  'dropoff_latitude': dropoff_latitude,
                  'passenger_count': passenger_count}

        response = requests.get(url, params=params)
        response.raise_for_status() # Raises an error if the response is not ok

        # Display the predicted fare amount
        st.success(f"Predicted fare amount: {response.json()['fare']:.2f}$")
    except requests.exceptions.RequestException as e:
        st.error("Failed to retrieve fare. Please check your input and try again.")
    except (KeyError, ValueError):
        st.error("Failed to parse API response. Please try again later.")

# Create a map centered on the pickup location
m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=13)

# Add markers for pickup and dropoff locations
folium.Marker([pickup_latitude, pickup_longitude], popup='Pickup location').add_to(m)
folium.Marker([dropoff_latitude, dropoff_longitude], popup='Dropoff location').add_to(m)

# Add a line between the pickup and dropoff locations
folium.PolyLine([[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]], color='red').add_to(m)

# Display the map
folium_static(m)
