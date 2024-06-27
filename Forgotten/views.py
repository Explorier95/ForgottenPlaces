from django.shortcuts import render
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect, FileResponse, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from Forgotten.models import *
from Forgotten.forms import *
from ForgottenPlaces import settings
from .geocoding import Geocoding
from .models import Places
import json
import requests
from geopy.geocoders import Nominatim

# Willkommensbildschirm wenn man den Root aufruft
def get_first_view(request):
    return render(request, 'Forgotten/welcome_screen.html', {'page_title': 'Forgotten Places'})

# gibt die List-Elemente aus
@login_required()
def get_place_list(request):
    places = Places.objects.all().order_by('name')

    return render(request, 'Forgotten/place_list.html', {'page_title': ' Forgotten Places',

                                                         'Places': places, })
#gibt die Profildaten
@login_required()
def get_profile(request):
    return render(request, 'Forgotten/profile.html', {'page_title': 'Profildaten'})

#logout funktionalität
def logout_view(request):
    logout(request)
    messages.success(request, 'Abgemeldet')
    return HttpResponseRedirect(reverse_lazy('login'))

#Funktion für das erstellen und bearbeiten von Orten
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


# Theoretisch unsicher sollte man die PK,s
# wissen nach alternativlösung suchen damit @login_required() eingesetzt werden kann (Classbased)
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


# Klasse für die Map
class MapView(TemplateView):
    template_name = 'Forgotten/map.html'

    # Funktion um die Karte im browser anzuzeigen
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_KEY
        context['places'] = Places.objects.all()
        return context


def map_view(request):
    places = Places.objects.all()
    return render(request, 'Forgotten/map.html', {'places': places})


def get_mapbox_token(request):
    """
    :param request:
    :return:
    method to hand the key to the javascript
    """
    token = settings.MAPBOX_KEY
    return JsonResponse({'token': token})
