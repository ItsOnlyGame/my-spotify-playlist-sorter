import os
from typing import Any
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
        redirect_uri='http://localhost:8080',
        open_browser=False
    )
    token: Any = auth_manager.get_access_token()
    return spotipy.Spotify(auth=token['access_token'])


def get_all_user_playlists(sp: spotipy.Spotify):
    all_playlists = []

    while True:
        playlist: Any = sp.current_user_playlists(limit=50, offset=0)

        all_playlists += playlist['items']

        if playlist['next'] is None:
            break

    return all_playlists


def get_playlist(sp: spotipy.Spotify, url: str):
    playlist = sp.playlist(url)
    return playlist


def get_playlist_items(sp: spotipy.Spotify, playlist_url) -> list:
    track_items = []

    playlist: Any = sp.playlist(playlist_url)
    total_tracks = playlist['tracks']['total']

    playlist_page_offset = 0
    while playlist_page_offset < total_tracks:
        results: Any = sp.playlist_items(playlist_url, limit=100, offset=playlist_page_offset)
        track_items += results['items']
        playlist_page_offset += len(results['items'])

    track_list = []

    for index, track in enumerate(track_items):
        if track['track'] is None:
            track['track'] = {
                "is_local": False,
                "album": {
                    "album_type": "album",
                    "name": "invalid",
                    "release_date": "1970-01-01",
                    "artists": [
                        { "name": "invalid" }
                    ],
                },
                "artists": [
                    { "name": "invalid" }
                ],
                "uri": f"invalid-{index}",
                "name": "invalid"
            }
            
        track_list.append(track['track'])

    return [track['track'] for track in track_items]


def get_album_tracks(sp: spotipy.Spotify, album_url) -> list:
    track_items = []

    album: Any = sp.album(album_url)
    total_tracks = album['tracks']['total']

    album_page_offset = 0
    while album_page_offset < total_tracks:
        results: Any = sp.album_tracks(album_url, limit=50, offset=album_page_offset)
        track_items += results['items']
        album_page_offset += len(results['items'])

    for track in track_items:
        track['album'] = album

    return track_items