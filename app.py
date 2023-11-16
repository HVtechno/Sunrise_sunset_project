from flask import Flask, render_template, request, jsonify, send_file
import requests
from urllib.parse import quote
import pytz
from datetime import datetime, timedelta
from opencage.geocoder import OpenCageGeocode
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

#call environment variables
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')
Google_api_key = os.getenv('Google_api_key')

# Initialize the geocoder
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

@app.route('/countries.json')
def get_countries_json():
    return send_file('countries.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

def convert_to_local_time(utc_time, country):
    # Get the time zone for the selected country using the OpenCage API
    geocoding_url = f'https://api.opencagedata.com/geocode/v1/json?q={quote(country)}&key={OPENCAGE_API_KEY}'
    print(geocoding_url)
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()
    print(geocoding_data)
    
    if 'results' in geocoding_data and len(geocoding_data['results']) > 0:
        country_timezone = geocoding_data['results'][0]['annotations']['timezone']['name']
        local_timezone = pytz.timezone(country_timezone)
        utc_time = datetime.strptime(utc_time, '%I:%M:%S %p')
        print(utc_time)
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
        print(local_time)
        return local_time.strftime('%I:%M %p')
    else:
        return "Timezone information not available for the selected country"
    

def get_latitude_longitude(country):
    geocoding_url = f'https://api.opencagedata.com/geocode/v1/json?q={quote(country)}&key={OPENCAGE_API_KEY}'
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if 'results' in geocoding_data and len(geocoding_data['results']) > 0:
        latitude = geocoding_data['results'][0]['geometry']['lat']
        longitude = geocoding_data['results'][0]['geometry']['lng']
        return latitude, longitude
    else:
        return None, None

def get_city_state_from_lat_lng(lat, lng, Google_api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": Google_api_key,
    }

    city = ""
    state = ""

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            # Extract city and state from the result
            for result in data["results"]:
                for component in result["address_components"]:
                    if "locality" in component["types"]:
                        city = component["long_name"]
                    if "administrative_area_level_1" in component["types"]:
                        state = component["short_name"]
                return city, state
        else:
            print("Geocoding request failed with status:", data["status"])
            return None, None

    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        return None, None
    
@app.route('/get_sunrise_sunset', methods=['POST'])
def get_sunrise_sunset():
    date = request.form.get('date')
    country = quote(request.form.get('country'))

    # Get the latitude and longitude for the selected country
    latitude, longitude = get_latitude_longitude(country)

    print(latitude)
    print(longitude)

    if latitude is None or longitude is None:
        return jsonify({'error': 'Unable to geocode the selected country'})

    # Use the retrieved latitude and longitude to get sunrise and sunset times
    url = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date}'
    response = requests.get(url)

    data = response.json()
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']

    country_city, country_state = get_city_state_from_lat_lng(latitude, longitude, Google_api_key) 

    # Convert UTC times to the local time zone
    sunrise_local = convert_to_local_time(sunrise, country)
    sunset_local = convert_to_local_time(sunset, country)

    # Create a list to hold the parts of the sunrise and sunset
    sunrise_parts = [sunrise_local]
    sunset_parts = [sunset_local]

    # Check if city and state information is available
    if country_city and country_state:
        sunrise_parts.extend([country_city, country_state])
        sunset_parts.extend([country_city, country_state])

    # Join the parts with a comma, but only if they exist
    sunrise_result = ', '.join(part for part in sunrise_parts if part)
    sunset_result = ', '.join(part for part in sunset_parts if part)

    return jsonify({
        'sunrise': sunrise_result,
        'sunset': sunset_result
    })

if __name__ == '__main__':
    app.run(debug=True)