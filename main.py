import spotipy
import numpy as np
from dotenv import load_dotenv
import os
import time
import math
import sys

##  Fetch spotify playlist tracks into an array
def getPlaylistItems() -> list:
    offset = 0
    items = []

    while True:
        results = sp.playlist_items(playlist_url, limit=100, offset=offset)

        items +=results['items']

        offset += 100
        if len(results['items']) != 100:
            break

    return items


## Sorts the spotify playlist
##
## 1. Artist added to playlist
## 2. Album release date
## 2. Replicates the album order found in the original album
##
def sort_playlist():
    playlist_tracks = getPlaylistItems()

    for track in playlist_tracks:
        if track['track']['album']['release_date'] == None:
            track['track']['album']['release_date'] = '2000-01-01'

        if len(track['track']['album']['release_date'].split('-')) == 1:
            track['track']['album']['release_date'] = track['track']['album']['release_date']+'-01-01'


    data = {};
    for item in playlist_tracks:
        album_name = item['track']['album']['name']
        if item['is_local'] == True:
            artist_name = item['track']['artists'][0]['name']
        elif item['track']['album']['album_type'] == 'compilation':
            artist_name = item['track']['album']['name']
        elif item['track']['album']['artists'][0]['name'] == 'Various Artists':
            artist_name = item['track']['artists'][0]['name']
        else:
            artist_name = item['track']['album']['artists'][0]['name']

        if not artist_name in data.keys():
            data[artist_name] = {};
        if not album_name in data[artist_name].keys():
            data[artist_name][album_name] = [];
        data[artist_name][album_name].append(item)

    for artist_name in data.keys():
        temp = []
        for album_name in data[artist_name].keys():
            # Handle local files
            if data[artist_name][album_name][0]['track']['is_local'] == True:
                temp += list(data[artist_name][album_name]).copy()
                continue
            
            # Sort album according to the actual album
            album_tracks = sp.album_tracks(data[artist_name][album_name][0]['track']['album']['id'])['items']

            other = list(data[artist_name][album_name]).copy()
            for sp_track in album_tracks:
                for track in data[artist_name][album_name]:
                    if sp_track['id'] == track['track']['id']:
                        temp.append(track)
                        other.remove(track)
            temp += other

        temp.sort(key=lambda item: time.mktime(time.strptime(item['track']['album']['release_date'], '%Y-%m-%d')))
        data[artist_name] = temp

    sorted_playlist = []
    for artists in data.keys():
        album_list = list(data[artists])

        for track in album_list:
            sorted_playlist.append(track)
    return sorted_playlist


# This executes the sorting of the playlist and commits the action to the playlist in spotify
def execute_sort():
    # Fetch playlist to list 
    print('Feching tracks from playlist... ')
    original = getPlaylistItems()
    with open('original.txt', mode='w', encoding='utf-8') as f:
        for item in original:
            f.write(item['track']['name']+'\n')

    print('Sorting playlist. ')
    sorted_list = sort_playlist()
    with open('sorted.txt', mode='w', encoding='utf-8') as f:
        for item in sorted_list:
            f.write(item['track']['name']+'\n')


    snapshot = None

    print('Applying change to playlist. ')
    playlist = getPlaylistItems()

    for j in range(0, len(sorted_list)-1):
        if playlist[j]['track']['uri'] != sorted_list[j]['track']['uri']:
            for i, t1 in enumerate(playlist):
                if t1['track']['uri'] == sorted_list[j]['track']['uri']:

                    if snapshot == None:
                        response = sp.playlist_reorder_items(playlist_url, range_start=i, insert_before=j)
                        snapshot = response['snapshot_id']

                        playlist.insert(j, playlist.pop(i))

                    else:
                        response = sp.playlist_reorder_items(playlist_url, range_start=i, insert_before=j, snapshot_id=snapshot)
                        snapshot = response['snapshot_id']

                        playlist.insert(j, playlist.pop(i))
                    break

                
if __name__ == '__main__':
    # Find env file containing the spotify client id and secret
    # If they are not found ask the user for the variables
    load_dotenv()
    requireInput = len(sys.argv) == 1

    if not os.getenv('SPOTIPY_CLIENT_ID'):
        os.environ['SPOTIPY_CLIENT_ID'] = input('Spotify client id: \n')
    
    if not os.getenv('SPOTIPY_CLIENT_SECRET'):
        os.environ['SPOTIPY_CLIENT_SECRET'] = input('Spotify client secret: \n')

    token = spotipy.util.prompt_for_user_token(None, scope='playlist-modify-private,playlist-modify-public', client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'), redirect_uri='http://localhost:8080') 
    sp = spotipy.Spotify(auth=token)

    while True:
        print('#######')
        print('What do you want to do?')
        print('0: Exit')
        print('1: Sort playlist')
        print('2: Duplicate playlist')
        print('#######\n')

        # Check for a automated response for this user action
        if requireInput == False:
            option = sys.argv[1]
        else:
            option = input('Which option?\n')



        if option == '0': # Exit
            break

        elif option == '1': # Sort playlist
            print("You need to create a developer application in the Spotify Developer Panel \nhttps://developer.spotify.com/")
            print("----------------------------------------------------------------------------------------------------------")
            
            if requireInput == False:
                playlist_url = sys.argv[2]
            else:
                playlist_url = input('Give playlist url: \n')
            
            execute_sort()
            
            break

        elif option == '2': # Duplicate playlist
            print("You need to create a developer application in the Spotify Developer Panel \nhttps://developer.spotify.com/")
            print("----------------------------------------------------------------------------------------------------------")

            if requireInput == False:
                playlist_url = sys.argv[2]
                new_playlist_name = sys.argv[3]
            else:
                playlist_url = input('Give playlist url that you want to copy: \n')
                print('')
                new_playlist_name = input('New playlist name: \n')

            print('')
            
            new_playlist = sp.user_playlist_create(sp.current_user()['id'], new_playlist_name, description='This playlist was created with automated software!')
            print('New playlist created with the name:', new_playlist_name, '\n')

            playlistItems = getPlaylistItems();
            filteredPlaylistItems = filter(lambda item: item['is_local'] == False, playlistItems)
            items = list(map(lambda item: item['track']['uri'], filteredPlaylistItems));

            arrays = np.array_split(items, math.ceil(len(items)/100))
            for array in arrays:
                sp.playlist_add_items(new_playlist['id'], array)

            break
        else: # Invalid
            print('Invalid option. Retry!\n\n')

    print('Finished!') 
  


