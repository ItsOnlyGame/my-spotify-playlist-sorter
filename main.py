import spotipy
import os
from dotenv import load_dotenv
import list_utils

def getPlaylistItems():
    offset = 0
    items = []
    artist_order = []

    while True:
        results = sp.playlist_items(playlist_url, limit=100, offset=offset)

        for item in results['items']:
            artist_order.append(item['track']['artists'][0]['name'])
            items.append(item)

        offset += 100
        if len(results['items']) != 100:
            break

    iterated_artists = []
    for item in artist_order[:]:
        if item in iterated_artists:
            artist_order.remove(item)
        else:
            iterated_artists.append(item)

    return { 'tracks': items, 'sort_order': iterated_artists }


def sortPlaylistList(data):
    grouped_artists = []

    for order in data['sort_order']:
        artist_group = []

        for track_item in data['tracks']:
            if (order == track_item['track']['artists'][0]['name']):
                artist_group.append(track_item)
                pass

        grouped_artists.extend(artist_group);

    return grouped_artists


def execute():
    playlist = getPlaylistItems()
    sorted_list = sortPlaylistList(playlist)

    for i, t1 in enumerate(sorted_list):
        for j, t2 in enumerate(playlist['tracks']):
            if i == j:
                continue

            if t1['track']['uri'] == t2['track']['uri']:
                sp.playlist_reorder_items(playlist_url, range_start=j, insert_before=i)
                list_utils.move_list_item(playlist['tracks'], j, i)
                

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
    print('Finished!')   
 