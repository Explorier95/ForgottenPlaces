from .models import Places
import json
import requests
from geopy.geocoders import Nominatim

"""
class for geocoding 
the main function of this class is to return latitude and longitude from city names
it uses the mapbox geocoding api 
"""

#TODO: security key noch in den token.json --> sichrheit !!! wichtig dann methode noch so dass es funktioniert
# TODO: viewonmap button, marker müssen noch funzen, grüner button bei location, farben css
#TODO: bei map noch oben menü aktivieren

class Geocoding:
    #initialise the class and load the key from the json (to pretect the key)
    def __init__(self):
        with open('token.json') as f:
            data = json.load(f)
            self.api_key = data['api_key']

    #function for returning coordinates
    def get_coordinates(self, region_name):
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{region_name}.json'
        params = {
            'access_token': self.api_key,
            'limit': 1
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'features' in data and len(data['features'])> 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates
        else:
            return None


def get_coordinates(region_name):
    geolocator = Nominatim(user_agent="my-application")
    region_name = Places.name
    try:
        location = geolocator.geocode(region_name)
        if location:
            lat = location.latitude
            lon = location.longitude
            return lat, lon
        else:
            return None, None
    except Exception as e:
        print(f'Fehler beim geocoding: {e}')
        return None, None

