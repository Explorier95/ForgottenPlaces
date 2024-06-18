from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from Forgotten.forms import *


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'Willkommen')
            login(request, user)
            return redirect('place_list')
        else:
            messages.error(request, "Es ist ein fehler aufgetreten, bitte versuchen Sie es erneut.")
            return redirect('login')

    else:
        messages.error(request, "Es ist ein fehler aufgetreten, bitte versuchen Sie es erneut.")
        return render(request, 'registration/login.html', {})
