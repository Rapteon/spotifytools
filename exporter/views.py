from django.http import HttpResponse
from django.shortcuts import render
from spotify.views import getPlaylists
import json


class Card:
    def __init__(self, title: str, url: str):
        self.title = title
        self.url = url


# Create your views here.
def index(request):
    cards = [Card("Playlists", "playlists")]
    return render(request, "exporter/index.html", {"cards": cards})


def playlists(request):
    playlists, num_total_tracks = getPlaylists()

    return render(
        request,
        "exporter/playlists.html",
        {
            "playlists": playlists,
            "num_total_tracks": num_total_tracks,
            "playlists_json": json.dumps(playlists),
        },
    )
