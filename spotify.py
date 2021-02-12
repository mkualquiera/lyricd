import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

def reload_spotify():
    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                scope="user-read-playback-state"
                ))
                
reload_spotify()

def get_playback():
    try:
        playback_response = sp.current_playback()
    except:
        reload_spotify()
        return get_playback()
    try:
        author = playback_response["item"]["artists"][0]["name"]
        song = playback_response["item"]["name"]
        progress = playback_response["progress_ms"]/1000
        return (author, song, progress)
    except:
        return (None, None, None)

if __name__ == "__main__":
    print(get_playback())