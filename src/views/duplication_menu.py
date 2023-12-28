import time

import duplicator
import views.view
from . import main_menu, state_manager
import spotify_util


class DuplicationMenu(views.view.View):

    def get_input(self):
        super().get_input(text="Duplicate Playlist")

        print("URL of playlist to duplicate")
        duplication_playlist_url = input(">> ")

        print("")
        print("Playlists name (empty for identical name)")
        new_playlist_name = input(">> ")
        if new_playlist_name == "":
            new_playlist_name = None

        valid_input = False
        duplicate_is_public = True
        while not valid_input:
            print("")
            print("Make playlist public (it doesn't matter because the Spotify API is broken) [y/N]")
            duplicate_is_public_input = input(">> ").lower()
            print(duplicate_is_public_input)

            if duplicate_is_public_input == "n" or duplicate_is_public_input == "":
                duplicate_is_public = False
                valid_input = True
            elif duplicate_is_public_input == "y":
                duplicate_is_public = True
                valid_input = True

        spotify = spotify_util.get_spotify()
        duplicator.duplicate_playlist(spotify, new_playlist_name, duplication_playlist_url, duplicate_is_public)

        time.sleep(3)
        state_manager.StateManager.set_state(main_menu.MainMenu())

