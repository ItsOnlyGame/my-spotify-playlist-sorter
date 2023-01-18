import threading
import time
import spotipy
from art import tprint
import util
import math

class Sorter(threading.Thread):

    def __init__(self, sp, playlist):
        threading.Thread.__init__(self)
        self.sp: spotipy.Spotify = sp
        self.playlist = playlist
        self.done = False
        self.start()

    def run(self):
        playlist_url = self.playlist['external_urls']['spotify']
        playlist_items = self.get_playlist_items(playlist_url)
        sorted_playlist_items = self.sort_playlist(playlist_items.copy())
        self.execute_sort(playlist_url, playlist_items, sorted_playlist_items)
        
        self.print_progress("Done!", 100, True)
        time.sleep(2)
        self.done = True

    def get_playlist_items(self, playlist_url) -> list:
        self.print_progress("Fetching all tracks", 0, True)
        offset = 0
        items = []

        playlist = self.sp.playlist(playlist_url)
        total_tracks = playlist['tracks']['total']

        while True:
            self.print_progress("Fetching all tracks", (offset / total_tracks) * 100)

            results = self.sp.playlist_items(playlist_url, limit=100, offset=offset)

            items += results['items']

            offset += 100
            if len(results['items']) != 100:
                break

        self.print_progress("Fetching all tracks", 100)
        return items


    #### Sorts the spotify playlist ####
    ##
    ## 1. Artist added to playlist
    ## 2. Album release date
    ## 2. Replicates the album order found in the original album
    ##
    #####
    def sort_playlist(self, playlist_tracks):
        self.print_progress("Sorting playlist", 0, True)

        # 1. Fix playlist tracks album release dates
        for track in playlist_tracks:
            if track['track']['album']['release_date'] is None:
                track['track']['album']['release_date'] = '1970-01-01'

            if len(track['track']['album']['release_date'].split('-')) == 1:
                track['track']['album']['release_date'] = track['track']['album']['release_date']+'-01-01'
        self.print_progress("Sorting playlist", 25)


        # 2. Determine which artist name will be used to sort the albums with
        data = {};
        for item in playlist_tracks:
            album_name = item['track']['album']['name']

            # If is a local track, use tracks artist
            if item['is_local'] is True:
                artist_name = item['track']['artists'][0]['name']

            # If track album is compilation, use albums artist
            elif item['track']['album']['album_type'] == 'compilation':
                artist_name = item['track']['album']['name']

            # If tracks albums artist is named "Various Artists", use tracks first artist
            elif item['track']['album']['artists'][0]['name'] == 'Various Artists':
                artist_name = item['track']['artists'][0]['name']

            # If no special condition exist use albums first artist
            else:
                artist_name = item['track']['album']['artists'][0]['name']

            # Initialize dictionary
            if not artist_name in data.keys():
                data[artist_name] = {};
            if not album_name in data[artist_name].keys():
                data[artist_name][album_name] = [];

            data[artist_name][album_name].append(item)
        self.print_progress("Sorting playlist", 50)

        # 3. Sort playlist
        for artist_name in data.keys():
            temp = []
            for album_name in data[artist_name].keys():
                # Handle local files
                if data[artist_name][album_name][0]['track']['is_local'] is True:
                    temp += list(data[artist_name][album_name]).copy()
                    continue

                # Sort album according to the actual album
                album_tracks = self.sp.album_tracks(data[artist_name][album_name][0]['track']['album']['id'])['items']

                other = list(data[artist_name][album_name]).copy()
                for sp_track in album_tracks:
                    for track in data[artist_name][album_name]:
                        if sp_track['id'] == track['track']['id']:
                            temp.append(track)
                            other.remove(track)
                temp += other

            def sort_by_date(item):
                if int(item['track']['album']['release_date'].split('-')[0]) < 2000:
                    item['track']['album']['release_date'] = '2000-01-01'

                return time.mktime(time.strptime(item['track']['album']['release_date'], '%Y-%m-%d'))

            temp.sort(key=lambda i: sort_by_date(i))
            data[artist_name] = temp
        self.print_progress("Sorting playlist", 75)

        # 4. Finalize sort
        sorted_playlist = []
        for artists in data.keys():
            album_list = list(data[artists])

            for track in album_list:
                sorted_playlist.append(track)
        self.print_progress("Sorting playlist", 100)


        return sorted_playlist


    # This executes the sorting of the playlist and commits the action to the playlist in spotify
    def execute_sort(self, playlist_url, playlist_items, sorted_playlist_items):
        snapshot = None

        progress = 0
        max_progress = len(sorted_playlist_items)-1
        self.print_progress("Applying change to playlist", (progress / max_progress) * 100, True)

        for j in range(0, len(sorted_playlist_items)-1):
            if playlist_items[j]['track']['uri'] != sorted_playlist_items[j]['track']['uri']:
                for i, t1 in enumerate(playlist_items):
                    if t1['track']['uri'] == sorted_playlist_items[j]['track']['uri']:

                        if snapshot is None:
                            response = self.sp.playlist_reorder_items(playlist_url, range_start=i, insert_before=j)
                            snapshot = response['snapshot_id']

                            playlist_items.insert(j, playlist_items.pop(i))

                        else:
                            response = self.sp.playlist_reorder_items(playlist_url, range_start=i, insert_before=j, snapshot_id=snapshot)
                            snapshot = response['snapshot_id']

                            playlist_items.insert(j, playlist_items.pop(i))
                        break
            progress += 1
            self.print_progress("Applying change to playlist", (progress / max_progress) * 100)  
            
    def print_progress(self, text: str, progress_state: int, gap = False):
        if gap:
            print("")
        print(f"{math.ceil(progress_state)}% - {text}")