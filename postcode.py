import requests

def get_city_state_from_lat_lng(lat, lng, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "latlng": f"{lat},{lng}",
        "key": api_key,
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

# Replace with your API key and latitude and longitude coordinates
api_key = "AIzaSyBJB4ak00J7cFuah6TfTnks7wkyDi61OBw"
latitude = -24.7761086  # Replace with the desired latitude
longitude =  134.755 # Replace with the desired longitude

city, state = get_city_state_from_lat_lng(latitude, longitude, api_key)
if city and state:
    print(f"City: {city}, State: {state}")
else:
    print("Unable to retrieve city and state information.")