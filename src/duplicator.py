import time
import numpy as np
import math

import spotify_util

def duplicate_playlist(spotify, new_playlist_name, playlist_url, is_public):
    if new_playlist_name is None:
        playlist = spotify_util.get_playlist(spotify, playlist_url)
        new_playlist_name = playlist['name']

    new_playlist = spotify.user_playlist_create(
        user=spotify.current_user()['id'],
        name=new_playlist_name,
        public=is_public,
        collaborative=False,
        description="This playlist was created with automated software!"
    )

    playlistItems = spotify_util.get_playlist_items(spotify, playlist_url)
    filteredPlaylistItems = filter(lambda item: item['is_local'] is False, playlistItems)
    items = list(map(lambda item: item['uri'], filteredPlaylistItems))

    splitList = np.array_split(items, math.ceil(len(items) / 100))
    for split in splitList:
        spotify.playlist_add_items(new_playlist['id'], split)