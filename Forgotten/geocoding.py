from ForgottenPlaces import settings
from .models import Places
import json
import requests
from geopy.geocoders import Nominatim


class Geocoding:
    """
    Klasse für das Laden der Mapbox sowie das Geocoding
    um Orte in Koordinaten zu berechnen
    """

    def __init__(self):
        # Initialisierung der Klasse
        self.api_key = settings.MAPBOX_KEY

    def load_api_key(self):
        # Laden des API-Schlüssels
        if not self.api_key:
            try:
                self.api_key = settings.MAPBOX_KEY
                if not self.api_key:
                    raise ValueError("API key not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def get_coordinates(self, region_name):
        """
        Diese Funktion verwendet die Mapbox Geocoding APi
        um Längen- und Breitengrade für Orte abzurufen
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


"""
def get_coordinates(region_name):
    Diese Funktion berechnet ebenfalls die Koordinaten sie nutzt dafür
    aber die Nominatim Open Source und nicht mapbox
    (eventuell für spätere Implementierungen angedacht)
    
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
"""


def update_coordinates():
    """
    Diese Funktion speichert die Location und updated die Orte
    mit den zuvor berechneten Daten
    """
    geocoder = Geocoding()
    places = Places.objects.all()
    for place in places:
        if place.location_map and (not place.latitude or not place.longitude):
            coordinates_mapbox = geocoder.get_coordinates(place.location_map)
            if coordinates_mapbox:
                place.latitude = coordinates_mapbox[1]
                place.longitude = coordinates_mapbox[0]
                place.save()
                print(f"Updated: {place.name} -> {place.latitude}, {place.longitude}")
            else:
                print(f"Koordinaten nicht gefunden: {place.location_map}")


update_coordinates()
