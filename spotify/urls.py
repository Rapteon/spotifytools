from django.urls import path
from . import views

urlpatterns = [path("playlists/", views.getPlaylists, name="playlists")]
