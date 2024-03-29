import googlemaps
import time

def get_taco_bell_coords(api_key: str='AIzaSyBVmTDCW8zxGKB41JwUj8PIxxwRSxfjiPQ', location: tuple=(40.7831, -73.9712), radius: int=24140):
    # Default is NYC, within 15 miles (reached out to Newark and the ass crack of Long Island or so)
    gmaps = googlemaps.Client(key=api_key)

    def fetch_places_nearby(client, location, radius, page_token=None):
        # Perform a nearby search for "Taco Bell" locations within the radius
        return client.places_nearby(location=location, radius=radius, keyword="Taco Bell", page_token=page_token)

    all_results = []

    results = fetch_places_nearby(gmaps, location, radius)
    all_results.extend(results['results'])

    while 'next_page_token' in results:
        time.sleep(2)  # Wait for the next_page_token to become valid
        results = fetch_places_nearby(gmaps, location, radius, results['next_page_token'])
        all_results.extend(results['results'])

    return [(place['geometry']['location']['lat'], place['geometry']['location']['lng']) for place in all_results]

get_taco_bell_coords(location=(39.5, -98.35), radius=100000)