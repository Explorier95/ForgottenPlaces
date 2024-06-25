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

class Geocoding:

    #initialise the class and load the key from the json (to pretect the key)
    def __init__(self):
       self.api_key = None

    def load_api_key(self):
        if not self.api_key:
            try:
                with open('token.json') as f:
                    data = json.load(f)
                    self.api_key = data.get('api_key')
                    if not self.api_key:
                        raise ValueError("API key not found in the token.json file.")
            except FileNotFoundError:
                print("token.json file not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

    #function for returning coordinates
    def get_coordinates(self, region_name):
        url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{region_name}.json'
        params = {
            'access_token': self.api_key,
            'limit': 1
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'features' in data and len(data['features']) > 0:
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates
        else:
            return None


def get_coordinates(region_name):
    geolocator = Nominatim(user_agent="my-application-custom")
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


geolocator = Nominatim(user_agent="my-application-custom")


"""function to get latitude and 
longitude from city names"""


def region_to_city(region_name):
    #region and capitals in germany
    region_capitals = {
        'Baden-Württemberg': 'Stuttgart',
        'Bayern': 'München',
        'Berlin': 'Berlin',
        'Brandenburg': 'Potsdam',
        'Bremen': 'Bremen',
        'Hamburg': 'Hamburg',
        'Hessen': 'Wiesbaden',
        'Mecklenburg-Vorpommern': 'Schwerin',
        'Niedersachsen': 'Hannover',
        'Nordrhein-Westfalen': 'Düsseldorf',
        'Rheinland-Pfalz': 'Mainz',
        'Sachsen': 'Dresden',
        'Sachsen-Anhalt': 'Magdeburg',
        'Schleswig-Holstein': 'Kiel',
        'Saarland': 'Saarbrücken',
        'Thüringen': 'Erfurt',
    }

    if region_name in region_capitals:
        capital_city = region_capitals[region_name]
        try:
            location = geolocator.geocode(capital_city)
            if location:
                return location.latitude, location.longitude
            else:
                print("Keine Koordinaten gefunden - bitte Bundesland in D angeben")
                return None, None
        except Exception as e:
            print(f'Fehler beim geocoding: {e}')
            return None, None


def update_coordinates_for_all_places():
    places = Places.objects.all()
    for place in places:
        if place.location_map and (not place.latitude or not place.longitude):
            location = geolocator.geocode(place.location_map)
            if location:
                place.latitude = location.latitude
                place.longitude = location.longitude
                place.save()
                print(f"Updated: {place.name} -> {place.latitude}, {place.longitude}")
            else:
                print(f"Koordinaten nicht gefunden: {place.location_map}")


update_coordinates_for_all_places()


def calculate_and_save_coordinates(places):
    places_with_coordinates = []

    for place in places:
        if place.location_map:
            lat, lon = get_coordinates(place.location_map)
            if lat and lon:
                place.latitude = lat
                place.longitude = lon
                place.save()
                places_with_coordinates.append({
                    'id': place.id,
                    'name': place.name,
                    'latitude': lat,
                    'longitude': lon
                })
            else:
                print(f"Koordinaten nicht gefunden für: {place.location_map}")

    with open('places_coordinates.json', 'w') as f:
        json.dump(places_with_coordinates, f, indent=4)
