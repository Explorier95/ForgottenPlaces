from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect, FileResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from Forgotten.models import *
from Forgotten.forms import *
from .models import Places
import json
import requests
from geopy.geocoders import Nominatim

# gibt die List-Elemente aus
@login_required()
def get_place_list(request):
    places = Places.objects.all().order_by('name')

    return render(request, 'Forgotten/place_list.html', {'page_title': ' Forgotten Places',
                                                         'Places': places, })


def logout_view(request):
    logout(request)
    messages.success(request, 'Abgemeldet')
    return HttpResponseRedirect(reverse_lazy('login'))


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Erfolgreich angemeldet')
            return HttpResponseRedirect(reverse_lazy('place_list'))
        else:
            form = UserCreationForm()
    return render(request, 'Forgotten/register_user.html', {'form': form})


# Willkommensbildschirm wenn man den Root aufruft
def get_first_view(request):
    return render(request, 'Forgotten/welcome_screen.html', {'page_title': 'Forgotten Places'})


# Funktion zum direkten Löschen von List-Elementen
# def place_delete(request, pk=None):
#     place = Places.objects.get(pk=pk)
#     place.delete()
#     return HttpResponseRedirect(reverse('place_list'))

# Funktion zum Speichern von neuen List-Elementen
@login_required()
def place_details(request, pk=None):
    if pk:
        places = Places.objects.get(pk=pk)
    else:
        places = Places()

    if request.method == 'POST':
        form = PlacesForm(request.POST, files=request.FILES, instance=places)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ort gespeichert.')
            return HttpResponseRedirect(reverse_lazy('place_list'))
        else:
            messages.error(request, 'Fehler bei der verarbeitung.')
    else:
        form = PlacesForm(instance=places)

    return render(request, 'Forgotten/place_details.html', {'page_title': 'Hinzufügen und Bearbeiten',
                                                            'form': form})


# Theoretisch unsicher sollte man die PK,s
# wissen nach alternativlösung suchen damit @login_required() eingesetzt werden kann
class PlaceDelete(DeleteView):
    model = Places
    context_object_name = 'place'
    success_url = reverse_lazy('place_list')

    def form_valid(self, form):
        messages.success(self.request, "Der Ort wurde erfolgreich gelöscht.")
        return super(PlaceDelete, self).form_valid(form)

    # Wenn Update benötigt wird ...
    # class PlaceUpdate(UpdateView):
    #     model = Places
    #     fields = ['name', 'story_field', 'upload_picture', 'location_map']
    #     success_url = reverse_lazy('place_list')
    #
    #     def form_valid(self, form):
    #         messages.success(self.request, "Der Ort wurde erfolgreich aktualisiert.")
    #         return super(PlaceUpdate, self).form_valid(form)


# Class for the Map view
class MapView(TemplateView):
    template_name = 'Forgotten/map.html'

    # function to show the map in the browser
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = 'pk.my_mapbox_access_token'
        return context

    def map_view(request):
        places = Places.objects.all()
        return render(request, 'map.html')
                   #   {'places:' places})

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

