from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse
from Forgotten.models import *
from Forgotten.forms import *


# Create your views here.

def get_place_list(request):
    places = Places.objects.all().order_by('name')

    return render(request, 'Forgotten/place_list.html', {'page_title': 'Meine Orte',
                                                         'Places': places, })

#geht noch nicht steht im Konflikt zu places_details es fehlt noch eine Abfrage...
def place_delete(request, pk=None):
    place = Places.objects.get(pk=pk)
    place.delete()
    return HttpResponseRedirect(reverse('place_list'))


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

    return render(request, 'Forgotten/place_details.html', {'page_title': 'Orte hinzufügen',
                                                            'form': form})
