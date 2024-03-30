import googlemaps
import time
import pandas as pd

def get_taco_bell_coords(api_key: str='AIzaSyBVmTDCW8zxGKB41JwUj8PIxxwRSxfjiPQ', location: tuple=(40.7831, -73.9712), radius: int=24140):
    gmaps = googlemaps.Client(key=api_key)

    def fetch_places_nearby(client, location, radius, page_token=None):
        return client.places_nearby(location=location, radius=radius, keyword="Taco Bell", page_token=page_token)

    all_results = []

    results = fetch_places_nearby(gmaps, location, radius)
    all_results.extend(results['results'])

    while 'next_page_token' in results:
        time.sleep(2) 
        results = fetch_places_nearby(gmaps, location, radius, results['next_page_token'])
        all_results.extend(results['results'])
    

    return pd.DataFrame([(place['geometry']['location']['lat'], place['geometry']['location']['lng'], place['vicinity']) for place in all_results],columns=["lat", "long", "address"])

print(get_taco_bell_coords())