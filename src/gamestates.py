from enum import Enum

class GameState(Enum):
    QUIT = 0
    START = 1
    MENU = 2
    PLAY = 3
    PAUSE = 4
    END = 5
