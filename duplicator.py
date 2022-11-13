import threading
import time
import spotipy
from art import tprint
import util
import numpy as np
import math
import spotify_util

class Duplicator(threading.Thread):

    def __init__(self, sp, new_playlist_name: str, playlist_url_to_duplicate: str):
        threading.Thread.__init__(self)
        self.sp: spotipy.Spotify = sp
        self.new_playlist_name = new_playlist_name
        self.playlist_url_to_duplicate = playlist_url_to_duplicate 
        self.done = False
        self.start()

    def run(self):
        if self.new_playlist_name is None:
            playlist = spotify_util.get_playlist(self.sp, self.playlist_url_to_duplicate)
            self.new_playlist_name = playlist['name']
                
        self.print_progress(f"Creating playlist with name {self.new_playlist_name}", 0, True)
        new_playlist = self.sp.user_playlist_create(self.sp.current_user()['id'], self.new_playlist_name, description='This playlist was created with automated software!')
        self.print_progress(f"Created playlist with name {self.new_playlist_name}", 100)


        playlistItems = self.get_playlist_items(self.playlist_url_to_duplicate);
        
        filteredPlaylistItems = filter(lambda item: item['is_local'] == False, playlistItems)
        items = list(map(lambda item: item['track']['uri'], filteredPlaylistItems));


        self.print_progress(f"Adding tracks to new playlist", 0)
        arrays = np.array_split(items, math.ceil(len(items)/100))
        for index, array in enumerate(arrays):
            self.sp.playlist_add_items(new_playlist['id'], array)
            
            self.print_progress(f"Adding tracks to new playlist", (index * 100)/len(items))

        
        self.print_progress("Done!", 100)
        time.sleep(2)
        self.done = True

    def get_playlist_items(self, playlist_url) -> list:
        self.print_progress("Fetching tracks in playlist", 0)
        offset = 0
        items = []

        playlist = self.sp.playlist(playlist_url)
        total_tracks = playlist['tracks']['total']

        while True:
            self.print_progress("Fetching tracks in playlist", (offset / total_tracks) * 100)

            results = self.sp.playlist_items(playlist_url, limit=100, offset=offset)

            items += results['items']

            offset += 100
            if len(results['items']) != 100:
                break

        self.print_progress("Fetching tracks in playlist", 100)
        return items

            
    def print_progress(self, text: str, progress_state: int, clear = False):
        if clear:
            util.clear()
            tprint("Spotify  Playlist  Sorter")
        print(f"{math.ceil(progress_state)}% - {text}")