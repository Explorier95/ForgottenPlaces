from django.forms import *
from Forgotten.models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms


class PlacesForm(ModelForm):
    class Meta:
        model = Places
        exclude = ()
        labels = {'story_field': 'Zum Ort',
                  'upload_picture': 'Bild hinzufügen',
                  'location_map': 'Geo-Daten für die Karte hinzufügen'}


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    error_messages = {
        'invalid_login': ("Es ist ein fehler aufgetreten, bitte versuchen Sie es erneut."),
        'inactive': ("Dieser Benutzer wurde gesperrt."),
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
