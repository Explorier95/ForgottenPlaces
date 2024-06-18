from django.shortcuts import render
from django.contrib import messages
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse_lazy
from django.urls import reverse
from Forgotten.models import *
from Forgotten.forms import *
from .models import Places


# Create your views here.


# gibt die List-Elemente aus
def get_place_list(request):
    places = Places.objects.all().order_by('name')

    return render(request, 'Forgotten/place_list.html', {'page_title': 'Meine Orte',
                                                         'Places': places, })


# Funktion zum direkten Löschen von List-Elementen
# def place_delete(request, pk=None):
#     place = Places.objects.get(pk=pk)
#     place.delete()
#     return HttpResponseRedirect(reverse('place_list'))

# Funktion zum Speichern von neuen List-Elementen
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
