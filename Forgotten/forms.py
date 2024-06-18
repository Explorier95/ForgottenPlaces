from django.forms import *
from Forgotten.models import *


class PlacesForm(ModelForm):
    class Meta:
        model = Places
        exclude = ()
        labels = {'story_field': 'Zum Ort',
                  'upload_picture': 'Bild hinzufügen',
                  'location_map': 'Geo-Daten für die Karte hinzufügen',
                  'place_delete': 'Ja,Löschen!'}
