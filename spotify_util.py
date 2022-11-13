import spotipy
import os

def get_user_token() -> spotipy.Spotify:
    scopes = [
        "playlist-modify-private",
        "playlist-modify-public",
        "playlist-read-private",
        "user-library-read"
    ]
    scope_string = ','.join(scopes)
    token = spotipy.util.prompt_for_user_token(None, scope=scope_string, client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'), redirect_uri='http://localhost:8080') 
    sp = spotipy.Spotify(auth=token)
    return sp

def get_all_user_playlists(sp: spotipy.Spotify):
    all_playlists = []
    
    while True:
        playlist = sp.current_user_playlists(limit=50, offset=0)
        
        all_playlists += playlist['items']
        
        if playlist['next'] == None:
            break
    
    return all_playlists

def get_playlist(sp: spotipy.Spotify, url: str):
    playlist = sp.playlist(url)
    return playlist
    
