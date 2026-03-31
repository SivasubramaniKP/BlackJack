from lib.menu import Menu
from lib.gameplay import Gameplay

class StateMachine:

    def __init__(self, q0):
        self.current_state = q0

    def set_state(self, state):
        self.current_state = state
    
    def get_state(self):
        return self.current_state