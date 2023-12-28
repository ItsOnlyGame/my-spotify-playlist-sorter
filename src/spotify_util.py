import os
import spotipy

spotify = None

def get_spotify() -> spotipy.Spotify:
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
    return spotipy.Spotify(auth=token['access_token'])


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


def get_playlist_items(sp: spotipy.Spotify, playlist_url) -> list:
    track_items = []

    playlist = sp.playlist(playlist_url)
    total_tracks = playlist['tracks']['total']

    playlist_page_offset = 0
    while playlist_page_offset < total_tracks:
        results = sp.playlist_items(playlist_url, limit=100, offset=playlist_page_offset)
        track_items += results['items']
        playlist_page_offset += len(results['items'])


    return track_items