import math
import threading
import time

import spotipy


def print_progress(text: str, progress_state: int, gap=False):
    if gap:
        print("")
    print(f"{math.ceil(progress_state)}% - {text}")


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

        print_progress("Done!", 100, True)
        time.sleep(2)
        self.done = True

    def get_playlist_items(self, playlist_url) -> list:
        print_progress("Fetching all tracks", 0, True)
        track_items = []

        playlist = self.sp.playlist(playlist_url)
        total_tracks = playlist['tracks']['total']

        playlist_page_offset = 0
        while True:
            print_progress("Fetching all tracks", (playlist_page_offset / total_tracks) * 100)

            results = self.sp.playlist_items(playlist_url, limit=100, offset=playlist_page_offset)

            track_items += results['items']

            playlist_page_offset += 100
            if len(results['items']) != 100:
                break

        print_progress("Fetching all tracks", 100)
        return track_items

    """
    #### Sorts the spotify playlist ####
    ##
    ## 1. Artist added to playlist
    ## 2. Album release date
    ## 2. Replicates the album order found in the original album
    ##
    """
    def sort_playlist(self, playlist_tracks):
        print_progress("Sorting playlist - Apply date fixed", 0, True)

        # 1. Fix playlist tracks album release dates
        for index, track in enumerate(playlist_tracks):
            # Add a date if one doesn't exist
            if track['track']['album']['release_date'] is None:
                track['track']['album']['release_date'] = '1970-01-01'

            # Add month and date if those do not exist
            if len(track['track']['album']['release_date'].split('-')) == 1:
                track['track']['album']['release_date'] += '-01-01'
            elif len(track['track']['album']['release_date'].split('-')) == 2:
                track['track']['album']['release_date'] += '-01'

            if index % 10 == 0:
                print_progress("Sorting playlist", (index // len(playlist_tracks)) * 25)

        # 2. Determine which artist name will be used to sort the albums with
        print_progress("Sorting playlist", 25)
        sorted_playlist = {}
        for index, item in enumerate(playlist_tracks):
            album_key = item['track']['album']['name']

            # If track is a local track, use tracks artist as a key
            if item['is_local'] is True:
                artist_key = item['track']['artists'][0]['name']

            # If track album is compilation, use album name as the artist
            elif item['track']['album']['album_type'] == 'compilation':
                artist_key = item['track']['album']['name']

            # If track album artist is named "Various Artists", use the first artist named in the track
            elif item['track']['album']['artists'][0]['name'] == 'Various Artists':
                artist_key = item['track']['artists'][0]['name']

            # If no edge cases are detected, use tracks album artist as a key
            else:
                artist_key = item['track']['album']['artists'][0]['name']

            if artist_key is None:
                raise Exception("artist_key is None, which should no be possible.")

            # Initialize dictionary based on playlist track data
            if artist_key not in sorted_playlist.keys():
                sorted_playlist[artist_key] = {}
            if album_key not in sorted_playlist[artist_key].keys():
                sorted_playlist[artist_key][album_key] = []

            sorted_playlist[artist_key][album_key].append(item)

            if index % 10 == 0:
                print_progress("Sorting playlist - Create dictionary for tracks",
                               25 + (index // len(playlist_tracks)) * 25)  # 50%

        # 3. Sort the playlist based on the previously created key values on the dictionary (sorted_playlist)
        print_progress("Sorting playlist - Sort playlist", 50)
        for index, artist_key in enumerate(sorted_playlist.keys()):
            sorted_albums = []

            for album_key in sorted_playlist[artist_key].keys():
                # Add the local tracks to sorted list. No album to base off an album sorting
                if sorted_playlist[artist_key][album_key][0]['track']['is_local'] is True:
                    sorted_albums += list(sorted_playlist[artist_key][album_key]).copy()
                    continue

                # Sort tracks according to the actual album they are from
                album_spotify_id = sorted_playlist[artist_key][album_key][0]['track']['album']['id']
                album_tracks = self.sp.album_tracks(album_spotify_id)['items']

                # Loop through the fetched spotify playlist and the dictionary.
                # Add the tracks to the sorted list when it loops to the correct position.
                # Left over tracks will be put into the sorted list
                other = list(sorted_playlist[artist_key][album_key]).copy()
                for sp_track in album_tracks:
                    for track in sorted_playlist[artist_key][album_key]:
                        if sp_track['id'] == track['track']['id']:
                            sorted_albums.append(track)
                            other.remove(track)
                sorted_albums += other

            # Sort the tracks based on albums release date and insert the sorted list to the dictionary
            sorted_albums.sort(key=lambda i: time.strptime(i['track']['album']['release_date'], '%Y-%m-%d'))
            sorted_playlist[artist_key] = sorted_albums

            if index % 10 == 0:
                print_progress("Sorting playlist - Sort playlist",
                               50 + (index / len(sorted_playlist.keys())) * 25)  # 75%

        # 4. Create a list of the dictionary where every track is in the right positions
        print_progress("Sorting playlist - Create a list of the sorted tracks", 75)
        sorted_list = []
        for index, artists in enumerate(sorted_playlist.keys()):
            album_list = list(sorted_playlist[artists])

            for track in album_list:
                sorted_list.append(track)

            if index % 10 == 0:
                print_progress("Sorting playlist - Create a list of the sorted tracks",
                               75 + (index // len(sorted_playlist.keys())) * 25)  # 100%

        print_progress("Sorting playlist - Sort completed", 100)
        return sorted_list

    # This executes the sorting of the playlist and commits the action to the playlist in spotify
    def execute_sort(self, playlist_url, playlist_items, sorted_playlist_items):
        snapshot = None

        progress = 0
        max_progress = len(sorted_playlist_items) - 1
        print_progress("Applying change to playlist", (progress // max_progress) * 100, True)

        for j in range(0, len(sorted_playlist_items) - 1):
            if playlist_items[j]['track']['uri'] != sorted_playlist_items[j]['track']['uri']:
                for i, t1 in enumerate(playlist_items):
                    if t1['track']['uri'] == sorted_playlist_items[j]['track']['uri']:

                        if snapshot is None:
                            response = self.sp.playlist_reorder_items(playlist_url, range_start=i, insert_before=j)
                            snapshot = response['snapshot_id']

                            playlist_items.insert(j, playlist_items.pop(i))

                        else:
                            response = self.sp.playlist_reorder_items(playlist_url, range_start=i, insert_before=j,
                                                                      snapshot_id=snapshot)
                            snapshot = response['snapshot_id']

                            playlist_items.insert(j, playlist_items.pop(i))
                        break
            progress += 1
            print_progress("Applying change to playlist", (progress // max_progress) * 100)
