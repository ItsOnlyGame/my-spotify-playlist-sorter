import unittest
import os
import copy
import random
import json

import spotify_util
import sorter

class SortTest(unittest.TestCase):

    def test_sort_on_album(self):
        # Fail test if environment variables are not set
        self.assertFalse(check_env_secrets())

        spotify = spotify_util.get_spotify()

        # Album that the sorting is tested on Talor Swift - 1989
        album_url = "https://open.spotify.com/album/64LU4c1nfjz1t4VnGhagcg?si=Tfw33Uv2QXmmx0zXvufE6Q"

        original_list = spotify_util.get_album_tracks(spotify, album_url)
        album_tracks = copy.deepcopy(original_list)

        # Randomize the album so that it can be sorted correcly.
        random.shuffle(album_tracks)

        # Sorting
        unique_album_items = sorter.remove_duplicate_tracks(album_tracks)
        sorter.fix_track_release_dates(unique_album_items)
        keyed_album = sorter.sort_tracks_into_keys(unique_album_items)
        sorter.sort_albums(spotify, keyed_album)
        album_tracks = sorter.map_to_list(keyed_album)

        # Map the lists to only contain the ids of the tracks and compare them.
        original_id_list = [track['id'] for track in original_list]
        sorted_id_list = [track['id'] for track in album_tracks]

        self.maxDiff = None
        self.assertEqual(original_id_list, sorted_id_list)


    def test_sort_on_playlist(self):
        # Fail test if environment variables are not set
        self.assertFalse(check_env_secrets())

        spotify = spotify_util.get_spotify()

        with open('./src/test/test_playlist_items.json', 'r') as file:
            playlist_items = json.load(file)
            playlist_items = [item['track'] for item in playlist_items]
        
        with open('./src/test/test_playlist_items_sorted.json', 'r') as file:
            presorted_list = json.load(file)
            presorted_list = [item['track'] for item in presorted_list]

        # Sorting
        unique_playlist_items = sorter.remove_duplicate_tracks(playlist_items)
        sorter.fix_track_release_dates(unique_playlist_items)        
        grouped_playlist = sorter.sort_tracks_into_keys(unique_playlist_items)
        sorter.sort_albums(spotify, grouped_playlist)
        playlist_tracks = sorter.map_to_list(grouped_playlist)

        # Map the lists to only contain the ids of the tracks and compare them.
        sorted_id_list = [track['id'] for track in playlist_tracks]
        presorted_id_list = [track['id'] for track in presorted_list]

        self.maxDiff = None
        self.assertEqual(sorted_id_list, presorted_id_list)

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
        return True

    with open('./config.json', 'r') as config:
        data = json.load(config)
        os.environ['SPOTIPY_CLIENT_ID'] = data['SPOTIPY_CLIENT_ID']
        os.environ['SPOTIPY_CLIENT_SECRET'] = data['SPOTIPY_CLIENT_SECRET']

    return False

if __name__ == '__main__':
    unittest.main()