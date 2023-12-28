from os import system, name
from art import tprint

class View:
    def __init__(self) -> None:        
        pass

    def get_input(self, text="Spotify Playlist Sorter"):
        self.clear()
        tprint(text)

    def clear(self):
        # for windows
        if name == 'nt':
            system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            system('clear')

