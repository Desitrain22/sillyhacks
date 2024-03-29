import googlemaps
from datetime import datetime

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyBVmTDCW8zxGKB41JwUj8PIxxwRSxfjiPQ')

# Define a location and radius (in meters)
location = (40.7831, 73.9712)  # Example: Los Angeles, CA
radius = 100  # Search within this radius
# Perform a text search for "Taco Bell" locations within the radius
results = gmaps.places(query="Taco Bell", location=location, radius=radius)

# Extract and print the names and locations
for place in results['results']:
    name = place['name']
    lat = place['geometry']['location']['lat']
    lng = place['geometry']['location']['lng']
    print(f"{name} at Latitude: {lat}, Longitude: {lng}")

coords = [(place['geometry']['location']['lat'], place['geometry']['location']['lng']) for place in results['results']]

for i in coords:
    print(i)

