from os import system, name, getenv
from sys import argv
from art import tprint

class View:
    def __init__(self) -> None:        
        pass

    def get_input(self, text="Spotify Playlist Sorter"):
        if "--debug" not in argv:
            self.clear()
        tprint(text)

    def clear(self):
        # for windows
        if name == 'nt':
            system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            system('clear')

