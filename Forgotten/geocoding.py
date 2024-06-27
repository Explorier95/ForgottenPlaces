from ForgottenPlaces import settings
from .models import Places
import json
import requests
from geopy.geocoders import Nominatim

"""
class for geocoding 
the main function of this class is to return latitude and longitude from city names
it uses the mapbox geocoding api 
"""


class Geocoding:

    #initialise the class and load the key from the json (to protect the key)
    def __init__(self):
       self.api_key = settings.MAPBOX_KEY

    def load_api_key(self):
        if not self.api_key:
            try:
                self.api_key = settings.MAPBOX_KEY
                if not self.api_key:
                    raise ValueError("API key not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

    #function for returning coordinates
    def get_coordinates(self, region_name):
        """
        This function is using the mapbox geocoding api to get latitude and longitude
        from the places
        :param region_name:
        :return:
        """
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
