import os
import sys

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
    missing_env_variables = False

    if not os.getenv('SPOTIPY_CLIENT_ID'):
        print("Env file is missing SPOTIPY_CLIENT_ID")
        missing_env_variables = True

    if not os.getenv('SPOTIPY_CLIENT_SECRET'):
        print("Env file is missing SPOTIPY_CLIENT_SECRET")
        missing_env_variables = True

    return missing_env_variables


if __name__ == '__main__':
    load_dotenv()

    if check_env_secrets():
        exit()

    if len(sys.argv) >= 2 and sys.argv[1] == "--sort":
        playlist_url = sys.argv[2]

        spotify = spotify_util.get_spotify()
        playlist = spotify_util.get_playlist(spotify, playlist_url)
        sorter.sort_playlist(spotify, playlist)
    else:
        # app = App()
        while True:
            StateManager.get_current_state().get_input()
