import spotipy
import os
from dotenv import load_dotenv
import time

def getPlaylistItems():
    offset = 0
    items = []

    while True:
        results = sp.playlist_items(playlist_url, limit=100, offset=offset)

        for item in results['items']:
            items.append(item)

        offset += 100
        if len(results['items']) != 100:
            break

    return items


def sort_playlist():
    playlist_tracks = getPlaylistItems()

    data = {};
    for item in playlist_tracks:
        album_name = item['track']['album']['name']
        artist_name = item['track']['artists'][0]['name']

        if not artist_name in data.keys():
            data[artist_name] = {};
        if not album_name in data[artist_name].keys():
            data[artist_name][album_name] = [];
        data[artist_name][album_name].append(item)

    for artists in data.keys():
        for album in data[artists].keys():
            album_tracks = sp.album_tracks(data[artists][album][0]['track']['album']['id'])['items']
            
            new_track_array = []
            for sp_track in album_tracks:
                for track in data[artists][album]:
                    if sp_track['id'] == track['track']['id']:
                        new_track_array.append(track)

            data[artists][album] = new_track_array

    
    sorted_playlist = []
    for artists in data.keys():
        album_list = list(data[artists])

        for i in range(0, len(album_list) - 1):

            first_key = album_list[i];
            second_key = album_list[i + 1];

            first_album = sp.album(data[artists][first_key][0]['track']['album']['id'])
            second_album = sp.album(data[artists][second_key][0]['track']['album']['id'])

            first_release_date = time.strptime(first_album['release_date'], "%Y-%m-%d")
            second_release_date = time.strptime(second_album['release_date'], "%Y-%m-%d")

            print(first_release_date)
            print(second_release_date)

            if (first_release_date > second_release_date): 
                album_list.insert(i+1, album_list.pop(i))

            print([album for album in album_list])
        
        for album in album_list:
            for track in data[artists][album]:
                sorted_playlist.append(track)

    return sorted_playlist


# https://open.spotify.com/playlist/60xD9HqNbgojJpeCLiUNJX?si=208e5d5e8c39474e

def execute():
    sorted_list = sort_playlist()
    snapshot = None

    print("Sorting playlist. This might take a while depending on the size of your playlist")
    iteration = 1
    while True:
        playlist = getPlaylistItems()
        sorted = True

        print("Running the "+iteration+" iteration.")

        for j in range(0, len(playlist)):
            if playlist[j]['track']['uri'] != sorted_list[j]['track']['uri']:
                sorted = False
                for i, t1 in enumerate(sorted_list):
                    if t1['track']['uri'] == playlist[j]['track']['uri']:
                        if snapshot == None:
                            response = sp.playlist_reorder_items(playlist_url, range_start=j, insert_before=i+1)
                            snapshot = response['snapshot_id']
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

    token = spotipy.util.prompt_for_user_token(None, scope='playlist-modify-private', client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'), redirect_uri='http://localhost:8080') 
    sp = spotipy.Spotify(auth=token)


    print("You need to create a developer application in the Spotify Developer Panel \nhttps://developer.spotify.com/")
    print("----------------------------------------------------------------------------------------------------------")
    playlist_url = input('Give playlist url: \n')

    execute()
    #sp.playlist_reorder_items(playlist_url, range_start=0, insert_before=3)

    print('Finished!')   
 