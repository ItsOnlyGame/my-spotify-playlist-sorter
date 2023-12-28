import time

from . import main_menu, state_manager
import views.view
import spotify_util
import sorter

class SortMenu(views.view.View):

    def get_input(self):
        super().get_input(text="Sort Playlist")

        print('1) Own playlist')
        print('2) Custom playlist (URL)')
        print('0) Return')

        value = input('>>> ')
        spotify = spotify_util.get_spotify()

        if value == "1":
            user_playlists = spotify_util.get_all_user_playlists(spotify)
            print("")
            for index, p in enumerate(user_playlists):
                print(f"{index + 1}) {p['name']}")
            print("\n0) Return")

            selected = input(">> ")
            if selected == "0":
                print("")
                return

            selected_playlist = user_playlists[int(selected) - 1]            
            sorter.sort_playlist(spotify, selected_playlist)

            time.sleep(3)
            state_manager.StateManager.set_state(main_menu.MainMenu())
                

        elif value == "2":
            print("What is the playlists url?")
            playlist_url = input(">> ")
            playlist = spotify_util.get_playlist(spotify, playlist_url)

            sorter.sort_playlist(spotify, playlist)

            time.sleep(3)
            state_manager.StateManager.set_state(main_menu.MainMenu())

        elif value == "0":
            state_manager.StateManager.set_state(main_menu.MainMenu())
