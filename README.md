# Spotify playlist sorter
This script sorts your spotify playlist.  

Sorting of the playlist follows these rules:
1. Tracks are sorted into groups of albums, that are ordered in the manner of the album.
2. Albums are grouped by artist and release date. (Artist is determined from the album rather than the track)
3. Artist groups are sorted depending on the first tracks appearance date on the playlist.

## Automation
To automate this process, you may use any utility that you seem fit.
The script has arguments that can so that it can automatically sort a playlist.

```
python3 ./main.py -sort 'playlist url here'
```

It executes the sorting with console output.
Recommended tools for the automation process is pm2, mostly used on node applications but can also be used to run python
scripts.

For some guidance on how to use pm2 with python, see [this link](https://pm2.io/blog/2018/09/19/Manage-Python-Processes)


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

or

```
python ./main.py
```

After that follow the script instructions.
There is an option to clone an existing playlist. This can be used to test the script before applying any permanent
sorting to your original playlist. 
