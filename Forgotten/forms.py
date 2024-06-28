from django.forms import *
from Forgotten.models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class PlacesForm(ModelForm):
    class Meta:
        """ Diese Klasse verknüpft das Formular mit dem Modell Places"""
        model = Places
        exclude = ()
        labels = {'story_field': 'Zum Ort',
                  'upload_picture': 'Bild hinzufügen',
                  'location_map': 'Geo-Daten für die Karte hinzufügen'}


class UserLoginForm(AuthenticationForm):
    """ Diese Klasse passt das AuthenticationForm für die Benutzeranmeldung an """
    def __init__(self, *args, **kwargs):
        """ Initialisierungscode der Basisklasse wird aufgerufen"""
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    error_messages = {
        'invalid_login': "Es ist ein fehler aufgetreten, bitte versuchen Sie es erneut.",
        'inactive': "Dieser Benutzer wurde gesperrt.",
    }
    success_messages = {

    }
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        },

    ))
