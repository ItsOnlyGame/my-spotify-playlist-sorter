# Spotify playlist sorter
This script sorts your spotify playlist.  

Sorting of the playlist follows these rules:
1. Tracks are sorted into groups of albums, that are ordered in the manner of the album.
2. Albums are grouped by artist and release date. (Artist is determined from the album rather than the track)
3. Artist groups are sorted depending on the first tracks appeatance date on the playlist.

## Automation
This repo contains [automation python example](example_automated.py).
This file can be used to automate the main script process.
Every argument in the automation file answers to input required by the main file.

## How to use
### Requirements
- Spotify API credentials (SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET)
    - Get these by creating an application in the [spotify developer portal](https://developer.spotify.com/dashboard/applications)
- Python 3
- Pip dependencies in the requirements.txt file

### Get started
After getting your spotify credentials create a .env and insert the client id and client secret like this 
```
SPOTIPY_CLIENT_ID=Insert client id here
SPOTIPY_CLIENT_SECRET=Insert client secret here
```

Now you can start the script by running 
```
python3 ./main.py
```

After that follow the script instuctions.
Also there is an option to clone an existing playlist. This can be used to test the script before applying any permanent sorting to your original playlist. 