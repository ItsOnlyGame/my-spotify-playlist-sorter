import spotipy
import os
from dotenv import load_dotenv
import time
import numpy as np
import math
from datetime import datetime

##  Fetch spotify playlist tracks into an array
def getPlaylistItems():
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
        if len(track['track']['album']['release_date'].split('-')) == 1:
            track['track']['album']['release_date'] = track['track']['album']['release_date']+'-01-01'


    data = {};
    for item in playlist_tracks:
        album_name = item['track']['album']['name']
        artist_name = item['track']['artists'][0]['name']

        if not artist_name in data.keys():
            data[artist_name] = {};
        if not album_name in data[artist_name].keys():
            data[artist_name][album_name] = [];
        data[artist_name][album_name].append(item)

    for artist_name in data.keys():
        temp = []
        for album_name in data[artist_name].keys():
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


# https://open.spotify.com/playlist/60xD9HqNbgojJpeCLiUNJX?si=208e5d5e8c39474e


def execute():
    # Fetch playlist to list 
    print('Feching tracks from playlist...')
    original = getPlaylistItems()
    with open('original.txt', mode='w', encoding='utf-8') as f:
        for item in original:
            f.write(item['track']['name']+'\n')

    print('Sorting playlist')
    sorted_list = sort_playlist()
    with open('sorted.txt', mode='w', encoding='utf-8') as f:
        for item in sorted_list:
            f.write(item['track']['name']+'\n')


    snapshot = None

    print("Sorting playlist. This might take a while depending on the size of your playlist")
    iteration = 1
    while True:
        playlist = getPlaylistItems()
        sorted = True

        print("Running the "+str(iteration)+" iteration.")

        for j in range(0, len(sorted_list)-1):
            if playlist[j]['track']['uri'] != sorted_list[j]['track']['uri']:
                print(playlist[j]['track']['name'])
                print(sorted_list[j]['track']['name'])
                print('###')
                sorted = False
                for i, t1 in enumerate(sorted_list):
                    if t1['track']['uri'] == playlist[j]['track']['uri']:
                        if snapshot == None:
                            response = sp.playlist_reorder_items(playlist_url, range_start=j, insert_before=i+1)
                            snapshot = response['snapshot_id']

                            playlist.insert(i, playlist.pop(j))

                        else:
                            response = sp.playlist_reorder_items(playlist_url, range_start=j, insert_before=i+1, snapshot_id=snapshot)
                            snapshot = response['snapshot_id']

                            playlist.insert(i, playlist.pop(j))
                        break

        iteration += 1
        if sorted: 
            break
                

if __name__ == '__main__':
    load_dotenv()

    if not os.getenv('SPOTIPY_CLIENT_ID'):
        os.environ['SPOTIPY_CLIENT_ID'] = input('Spotify client id: \n')
    
    if not os.getenv('SPOTIPY_CLIENT_SECRET'):
        os.environ['SPOTIPY_CLIENT_SECRET'] = input('Spotify client secret: \n')

    token = spotipy.util.prompt_for_user_token(None, scope='playlist-modify-private,playlist-modify-public', client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'), redirect_uri='http://localhost:8080') 
    sp = spotipy.Spotify(auth=token)


    while True:
        print('#######')
        print('What do you want to do?')
        print('0: Sort playlist')
        print('1: Duplicate playlist')
        print('#######\n')
        option = input('Which option?\n')

        if option == '0':
            print("You need to create a developer application in the Spotify Developer Panel \nhttps://developer.spotify.com/")
            print("----------------------------------------------------------------------------------------------------------")
            playlist_url = input('Give playlist url: \n')

            
            execute()
            
            break

        if option == '1':
            print("You need to create a developer application in the Spotify Developer Panel \nhttps://developer.spotify.com/")
            print("----------------------------------------------------------------------------------------------------------")
            playlist_url = input('Give playlist url that you want to copy: \n')
            print('')
            new_playlist_name = input('New playlist name: \n')

            print('')
            
            new_playlist = sp.user_playlist_create(sp.current_user()['id'], new_playlist_name, description='This playlist was created with automated software!')
            print('New playlist created with the name:', new_playlist_name, '\n')

            playlistItems = getPlaylistItems();
            items = list(map(lambda item: item['track']['uri'], playlistItems));

            arrays = np.array_split(items, math.ceil(len(items)/100))
            for array in arrays:
                sp.playlist_add_items(new_playlist['id'], array)

            break
        else:
            print('Invalid option. Retry!\n\n')

    print('Finished!') 
  


