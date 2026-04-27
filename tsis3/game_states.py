from enum import Enum, auto

class GameStates(Enum):
    MAIN_MENU    = auto()
    SET_USERNAME = auto()
    PLAYING      = auto()
    GAME_OVER    = auto()
    LEADERBOARD  = auto()
    SETTINGS     = auto()
    SETTINGS_SAVED = auto()
    QUIT         = auto()
