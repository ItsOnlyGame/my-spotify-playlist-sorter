import os
import sys
import json
from sys import exit

from dotenv import load_dotenv

from views.state_manager import StateManager
import spotify_util
import sorter

def check_env_secrets():
    """
    Checks the presence of Spotify API environment variables.

    This function verifies the existence of required Spotify API environment variables
    ('SPOTIPY_CLIENT_ID' and 'SPOTIPY_CLIENT_SECRET') and prints an error message
    for each missing variable. It returns a boolean indicating whether any of the
    required variables are missing.

    Returns:
        bool: True if any required environment variables are missing, False otherwise.
    """
    if not os.path.exists('./config.json'):
        print("Config file doesn't exist")
        with open('./config.json', 'w') as config:
            json.dump({ "SPOTIPY_CLIENT_ID": "", "SPOTIPY_CLIENT_SECRET": "" }, config)
        return True

    with open('./config.json', 'r') as config:
        data = json.load(config)
        
        os.environ['SPOTIPY_CLIENT_ID'] = data['SPOTIPY_CLIENT_ID']
        os.environ['SPOTIPY_CLIENT_SECRET'] = data['SPOTIPY_CLIENT_SECRET']

    return False


if __name__ == '__main__':
    load_dotenv()

    if check_env_secrets():
        exit()
        
    
    if "--sort" in sys.argv and len(sys.argv) >= 3:
        argv_index = sys.argv.index("--sort")
        playlists = sys.argv[argv_index + 1]
        
        for playlist_url in playlists.split(','):
            spotify = spotify_util.get_spotify()
            playlist = spotify_util.get_playlist(spotify, playlist_url)
            sorter.sort_playlist(spotify, playlist)
    else:
        # app = App()
        while True:
            StateManager.get_current_state().get_input()
