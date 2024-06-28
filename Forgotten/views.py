from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect, FileResponse, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from Forgotten.forms import *
from ForgottenPlaces import settings
from .geocoding import Geocoding
from .models import Places
import json
import requests


def get_first_view(request):
    """ Willkommensbildschirm wenn man den Root aufruft """
    return render(request, 'Forgotten/welcome_screen.html', {'page_title': 'Forgotten Places'})


@login_required()
def get_place_list(request):
    """ Gibt die List-Elemente aus"""
    places = Places.objects.all().order_by('name')

    return render(request, 'Forgotten/place_list.html',
                  {'page_title': ' Forgotten Places', 'Places': places, })

@login_required()
def get_profile(request):
    """ gibt die Profildaten aus """
    return render(request, 'Forgotten/profile.html', {'page_title': 'Profildaten'})


def logout_view(request):
    """ logout funktionalität """
    logout(request)
    messages.success(request, 'Abgemeldet')
    return HttpResponseRedirect(reverse_lazy('login'))


def register_user(request):
    """ Funktion für das erstellen und bearbeiten von Orten """
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


@login_required()
def place_details(request, pk=None):
    """ Funktion zum Speichern von neuen List-Elementen """
    if pk:
        places = Places.objects.get(pk=pk)
    else:
        places = Places()

    if request.method == 'POST':
        form = PlacesForm(request.POST, files=request.FILES, instance=places)
        if form.is_valid():
            place = form.save(commit=False)

            geocoder = Geocoding()
            coordinates = geocoder.get_coordinates(place.location_map)
            if coordinates:
                place.longitude, place.latitude = coordinates

            place.save()
            messages.success(request, 'Ort gespeichert.')
            return HttpResponseRedirect(reverse_lazy('place_list'))
        else:
            messages.error(request, 'Fehler bei der verarbeitung.')
    else:
        form = PlacesForm(instance=places)

    return render(request, 'Forgotten/place_details.html', {'page_title': 'Hinzufügen und Bearbeiten',
                                                            'form': form})


class PlaceDelete(DeleteView):
    """ Klasse um Orte wieder löschen zu können. """
    model = Places
    context_object_name = 'place'
    success_url = reverse_lazy('place_list')

    def form_valid(self, form):
        """ Erfolgsnachricht falls es geklappt hat"""
        messages.success(self.request, "Der Ort wurde erfolgreich gelöscht.")
        return super(PlaceDelete, self).form_valid(form)


class MapView(TemplateView):
    """ Klasse für das Anzeigen der Karte """
    template_name = 'Forgotten/map.html'

    def get_context_data(self, **kwargs):
        """ Methode um die Karte im Browser anzuzeigen """
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_KEY
        context['places'] = Places.objects.all()
        # Hinzufügen der Längen & Breitengrade, notwendig für Zoomen später
        context['lon'] = self.request.GET.get('lon', None)
        context['lat'] = self.request.GET.get('lat', None)
        return context


def map_view(request):
    """ Funktion zur Anzeige der Karte im Browser """
    places = Places.objects.all()
    return render(request, 'Forgotten/map.html', {'places': places})


def get_mapbox_token(request):
    """
    Funktion die den Mapbox Key als Json zurück gibt damit er in
    der JS Controller genutzt werden kann
    """
    token = settings.MAPBOX_KEY
    return JsonResponse({'token': token})
