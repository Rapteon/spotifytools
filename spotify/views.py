from django.http import HttpResponse
from .models import Credential, SpotifyUser, Token
from django.utils import timezone

import urllib.request
import urllib.parse
import sys
import json

# Create your views here.

# Encoding for requests/responses
ENCODING = "utf-8"


def sendRequest(urllib_req):
    resp = urllib.request.urlopen(urllib_req)

    if resp.code != 200:
        print(f"{resp.code}: {resp.msg}", file=sys.stderr)
        return None

    return resp


def getDictResponse(response):
    try:
        return json.load(response)
    except json.JSONDecodeError:
        print(f"Could not parse data into JSON: {response}", file=sys.stderr)
        return {}


def getOrCreateToken(credential: Credential) -> Token:
    token = Token.objects.first()
    if token is None:
        print("Token does not exist. Creating...")
        return createToken(credential)

    elif token.expiry_time < timezone.now():
        print("Token has expired")
        # TODO delete all tokens in DB
        all_tokens = Token.objects.all()
        all_tokens.delete()

        return createToken(credential)
    else:
        return token


def createToken(credential: Credential):
    API_URL = "https://accounts.spotify.com/api/token"
    HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
    METHOD = "POST"

    data = f"grant_type=client_credentials&client_id={credential.client_id}&client_secret={credential.client_secret}"
    req = urllib.request.Request(
        API_URL, data=bytes(data, ENCODING), headers=HEADERS, method=METHOD
    )

    resp = sendRequest(req)
    resp = getDictResponse(resp)

    # Calculate expiry time for token.
    expiry_time = timezone.now() + timezone.timedelta(
        days=0, seconds=resp["expires_in"]
    )
    token = Token(
        access_token=resp["access_token"],
        token_type=resp["token_type"],
        expiry_time=expiry_time,
    )
    token.save()

    return token


def getURLEncodedParams(params):
    return urllib.parse.urlencode(params, safe="(),")


def getPlaylists():
    # Get first credential row from table. Only consider the first credential.
    credential = Credential.objects.get(id=1)
    token = getOrCreateToken(credential=credential)
    spotify_user = SpotifyUser.objects.first()

    HEADERS = {
        "Authorization": f"{token.token_type} {token.access_token}",
        "Content": "application/json",
    }
    METHOD = "GET"

    # Get specific fields from API
    params = {
        "fields": "items(name, tracks(total, href))",
    }
    query_string = getURLEncodedParams(params)
    api_url = (
        f"https://api.spotify.com/v1/users/{spotify_user.id}/playlists?{query_string}"
    )

    req = urllib.request.Request(
        api_url,
        headers=HEADERS,
        method=METHOD,
    )

    resp = sendRequest(req)

    dict = getDictResponse(resp)
    all_playlists = []
    num_tracks_total = 0

    for playlist in dict["items"]:
        pl = {"name": playlist["name"]}
        pl["track_count"] = playlist["tracks"]["total"]
        tracks = getPlaylistTracks(token, playlist["tracks"]["href"])
        pl["tracks"] = tracks
        pl["tracks_json"] = json.dumps(tracks)
        num_tracks_total += pl["track_count"]
        all_playlists.append(pl)

    return all_playlists, num_tracks_total


def getPlaylistTracks(token, tracks_api_url):
    # Get specific fields from API
    params = {
        "fields": "items(track(name, artists, duration_ms, album(images, release_date))), next"
    }
    query_string = getURLEncodedParams(params)
    tracks_api_url = f"{tracks_api_url}?{query_string}"

    HEADERS = {
        "Authorization": f"{token.token_type} {token.access_token}",
        "Content": "application/json",
    }
    METHOD = "GET"

    req = urllib.request.Request(tracks_api_url, headers=HEADERS, method=METHOD)

    resp = sendRequest(req)

    dict = getDictResponse(resp)

    tracks = []

    for item in dict["items"]:
        tr = {
            "name": item["track"]["name"],
            "artists": [{"name": art["name"]} for art in item["track"]["artists"]],
            "duration_ms": item["track"]["duration_ms"],
            "images": item["track"]["album"]["images"],
            "release_date": item["track"]["album"]["release_date"],
        }
        tracks.append(tr)

    # API returns paginated results, so next field should be checked for the next URL
    # and results should be fetched.
    if dict["next"]:
        next_tracks = getPlaylistTracks(token, dict["next"])
        for tr in next_tracks:
            tracks.append(tr)

    return tracks
