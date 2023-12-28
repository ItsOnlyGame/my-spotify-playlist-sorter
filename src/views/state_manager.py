from . import  main_menu

class StateManager:
    current_state = main_menu.MainMenu()

    @staticmethod
    def set_state(new_state):
        StateManager.current_state = new_state
    
    @staticmethod
    def get_current_state():
        return StateManager.current_state