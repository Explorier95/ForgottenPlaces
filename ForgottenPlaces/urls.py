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
from Forgotten.views import get_place_list, get_profile, place_details, PlaceDelete, get_first_view, logout_view, \
    register_user, get_mapbox_token  # place_delete
from Forgotten.forms import UserLoginForm
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from django.conf.urls import include
from Forgotten.views import MapView

urlpatterns = [
                  path('', get_first_view, name='welcome'),
                  path('admin/', admin.site.urls),
                  # path('members/', include('members.urls')),
                  # path('members/', include('django.contrib.auth.urls')),
                  path('places/', get_place_list, name='place_list'),
                  path('profile/', get_profile, name='profile'),
                  path('places/add/', place_details, name='add_places'),
                  path('places/edit/<int:pk>', place_details, name='edit_place'),
                  path('place/delete/<int:pk>/', PlaceDelete.as_view(), name='place-delete'),
                  # Für eigenes Login mit Bootstrap template etc...
                  path(
                      'login/',
                      views.LoginView.as_view(
                          template_name="Forgotten/login.html",
                          authentication_form=UserLoginForm
                      ),
                      name='login'),
                  path('logout/', logout_view, name='logout'),
                  path('regist/', register_user, name='register'),

                  path('map/', MapView.as_view(), name='map'),
                  path('api/mapbox-token/', get_mapbox_token, name='get_mapbox_token')
                  # Wenn Update benötigt wird ...
                  # path('place/update/<int:pk>/', PlaceUpdate.as_view(), name='place-update'),
                  # URL zum direkten löschen
                  # -> path('places/place_delete/<int:pk>', place_delete, name='place_delete'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
