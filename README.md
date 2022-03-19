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