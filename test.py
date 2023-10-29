from opencage.geocoder import OpenCageGeocode

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '5ba3f78b608b430d9627a7660928f0d1'

# Initialize the geocoder
geocoder = OpenCageGeocode(api_key)

# Latitude and longitude coordinates
lat = 49.7439047
lng = 15.3381061

# Perform the geocoding
results = geocoder.reverse_geocode(lat, lng)

if results:
    # Extract location information
    location = results[0]['components']
    print(location)

    # Print the location details
    print("Country:", location.get('country'))
    print("City:", location.get('city'))
    print("State:", location.get('state'))
    print("Postal Code:", location.get('postcode'))
else:
    print("Location not found")