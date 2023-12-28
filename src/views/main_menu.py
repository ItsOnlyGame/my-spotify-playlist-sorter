from sys import exit

from . import sort_menu, duplication_menu, state_manager
import views.view

class MainMenu(views.view.View):

    def get_input(self):
        super().get_input()

        print('1) Sort playlist')
        print('2) Duplicate playlist')
        print('0) Exit')

        value = input('>>> ')
        if value == "1":
            state_manager.StateManager.set_state(sort_menu.SortMenu())
        elif value == "2":
            state_manager.StateManager.set_state(duplication_menu.DuplicationMenu())
        elif value == "0":
            exit()

