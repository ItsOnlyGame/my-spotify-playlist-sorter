from os import system, name
from art import tprint

class View:
    def __init__(self, title) -> None:        
        self.clear()
        tprint("Spotify Playlist Sorter")

    def get_input(self):
        pass

    def clear(self):
        # for windows
        if name == 'nt':
            system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            system('clear')

