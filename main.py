import os
import sys
import threading
import time

from art import tprint
from dotenv import load_dotenv

import spotify_util
import util
from duplicator import Duplicator
from sorter import Sorter


class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loading_progress = 0
        self.spotify = None
        self.current_menu = "MainMenu"
        self.start()

    def run(self, invalid_input=False):
        self.set_spotify()
        tprint("Spotify  Playlist  Sorter")

        if self.current_menu == "MainMenu":
            self.render_main_menu()

        if self.current_menu != 'EXIT':
            self.run()

    def render_main_menu(self, invalid_input=False):
        util.clear()
        tprint("Spotify  Playlist  Sorter")
        if invalid_input:
            print("Invalid input!\n")
        print("")

        print('1) Sort playlist')
        print('2) Duplicate playlist')
        print('0) Exit')

        value = input('>>> ')
        if value == "1":
            self.render_sort_menu()
        elif value == "2":
            self.render_duplication_menu()
        elif value == "0":
            self.current_menu = "EXIT"
        else:
            self.render_main_menu(True)

    def render_sort_menu(self, invalid_input=False):
        util.clear()
        tprint("Spotify  Playlist  Sorter")
        if invalid_input:
            print("Invalid input!\n")
        print("")

        print('1) Own playlist')
        print('2) Custom playlist (URL)')
        print('0) Return')

        value = input('>>> ')
        if value == "1":
            util.clear()
            tprint("Spotify  Playlist  Sorter")

            user_playlists = spotify_util.get_all_user_playlists(self.spotify)
            print("")
            for index, p in enumerate(user_playlists):
                print(f"{index + 1}) {p['name']}")
            print("\n0) Return")

            selected = input(">> ")
            if selected == "0":
                self.render_sort_menu()

            selected_playlist = user_playlists[int(selected) - 1]
            sorter = Sorter(self.spotify, selected_playlist)

            while not sorter.done:
                time.sleep(1)

        elif value == "2":
            util.clear()
            tprint("Spotify  Playlist  Sorter")

            print("")
            print("What is the playlists url?")
            playlist_url = input(">> ")
            playlist = spotify_util.get_playlist(self.spotify, playlist_url)
            sorter = Sorter(self.spotify, playlist)

            while not sorter.done:
                time.sleep(1)

        elif value == "0":
            self.current_menu = "MainMenu"
            self.render_main_menu()
        else:
            self.render_sort_menu(True)

    def render_duplication_menu(self, invalid_input=False):
        util.clear()
        tprint("Spotify  Playlist  Duplicator")
        if invalid_input:
            print("Invalid input!\n")
        print("")

        print("\nURL of playlist to duplicate")
        duplication_playlist_url = input(">> ")

        print("\nPlaylists name (empty for identical name)")
        new_playlist_name = input(">> ")
        if new_playlist_name == "":
            new_playlist_name = None

        valid_input = False
        duplicate_is_public = True
        while not valid_input:
            print("\nMake playlist public (it doesn't matter because the Spotify API is broken) [y/N]")
            duplicate_is_public_input = input(">> ").lower()
            print(duplicate_is_public_input)

            if duplicate_is_public_input == "n" or duplicate_is_public_input == "":
                duplicate_is_public = False
                valid_input = True
            elif duplicate_is_public_input == "y":
                duplicate_is_public = True
                valid_input = True

        duplicator = Duplicator(self.spotify, new_playlist_name, duplication_playlist_url, duplicate_is_public)

        while not duplicator.done:
            time.sleep(1)

        self.current_menu = "MainMenu"
        self.render_main_menu()

    def set_spotify(self):
        if self.spotify is not None:
            return

        missing_env_variables = False

        if not os.getenv('SPOTIPY_CLIENT_ID'):
            print("Env file is missing SPOTIPY_CLIENT_ID")
            missing_env_variables = True

        if not os.getenv('SPOTIPY_CLIENT_SECRET'):
            print("Env file is missing SPOTIPY_CLIENT_SECRET")
            missing_env_variables = True

        if not missing_env_variables:
            self.spotify = spotify_util.get_user_token()


if __name__ == '__main__':
    load_dotenv()

    if len(sys.argv) >= 2 and sys.argv[1] == "-sort":
        playlist_url = sys.argv[2]

        spotify = spotify_util.get_user_token()
        playlist = spotify_util.get_playlist(spotify, playlist_url)
        sorter = Sorter(spotify, playlist)

        while not sorter.done:
            time.sleep(1)
    else:
        app = App()
