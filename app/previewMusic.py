
#SPOTIPY environment variable CLIENT_ID en CLIENT_SECRET staan in .env file
#worden automatisch gelden bij starten pipenv shell

import spotipy
import sys
import os
# from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

from datetime import date, datetime
from app.album import Album

def haalNewReleases(sp, land):

    regels = []
    offset = 0
    nieuw = sp.new_releases(limit=50, offset=offset, country=land) 
    newlijst = nieuw['albums']['items']
    teller = 0
    while len(newlijst) > 0:

        for el in newlijst[0:10]:
        
            teller += 1
            album = Album()

            album.reldate = el['release_date']
            if (date.today() - datetime.strptime(album.reldate, '%Y-%m-%d').date()).days < 8:

                album.volgnr = teller
                album_id = el['id']
                album.artist = el['artists'][0]['name']
                album.title = el['name']
                album.image = el['images'][0]['url']

                artist = sp.artist(el['artists'][0]['id'])
                album.artist_popularity = artist['popularity']

                genre = ""
                for idx, g in enumerate(artist['genres']):
                    if idx < 4:
                        genre = genre + " " + g

                album.artist_genres = genre

                tracks = sp.album_tracks(album_id=album_id, limit=50, offset=0, market=None)
                album.tracks = []
                album.prev = []
                for l in tracks['items']:
                    if l['preview_url'] != None:
                        album.tracks.append(l['name'])
                        album.prev.append(l['preview_url'])
                regels.append(album)

        offset += 50
        nieuw = sp.new_releases(country="NL", limit=50, offset=offset)
        newlijst = nieuw['albums']['items']


    regels = sorted(regels, key=lambda x: x.reldate, reverse=True)

    return regels

def haalAlbums(land):

    #Geeft een redirect op localhost:5000 om token te accepteren
    # username = os.getenv('SPOTIFY_USER')
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    scope = 'user-library-read'


    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
 
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, username=username))

    return haalNewReleases(sp, land)

if __name__ == "__main__ ":
    haalAlbums()