import os

import spotipy


def get_user_token() -> spotipy.Spotify:
    scopes = [
        "playlist-modify-private",
        "playlist-modify-public",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-read",
        "user-library-modify"
    ]
    scope_string = ','.join(scopes)

    auth_manager = spotipy.SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        scope=scope_string,
        redirect_uri='http://localhost:8080'
    )
    token = auth_manager.get_access_token()
    sp = spotipy.Spotify(auth=token['access_token'])

    return sp


def get_all_user_playlists(sp: spotipy.Spotify):
    all_playlists = []

    while True:
        playlist = sp.current_user_playlists(limit=50, offset=0)

        all_playlists += playlist['items']

        if playlist['next'] is None:
            break

    return all_playlists


def get_playlist(sp: spotipy.Spotify, url: str):
    playlist = sp.playlist(url)
    return playlist
