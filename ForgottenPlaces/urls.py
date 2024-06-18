"""ForgottenPlaces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Forgotten.views import get_place_list, place_details, place_delete

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('places/', get_place_list, name='place_list'),
                  path('places/add/', place_details, name='add_places'),
                  path('places/edit/<int:pk>', place_details, name='edit_place'),
                  path('places/place_delete/<int:pk>', place_delete, name='place_delete'),
                  # path('place_delete/<int:pk>', place_delete, name="place-delete"),
                  # path('place_delete/<int:id>/', place_delete, name='place_delete'),
                  # path('places/edit/<int:pk>', place_delete, name='place-delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
