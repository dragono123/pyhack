"""
Components management
"""
# pylint: disable=R0903


import enum


class Player:
    """
    Player component : Says if an entity is the player
    """
    def __init__(self):
        self.action = Action_List.NOTHING

class Action_List(enum.Enum):
    NOTHING = 0
    MOVE = 8
    MOVE_UP = 1 | MOVE
    MOVE_DOWN = 2 | MOVE
    MOVE_RIGHT = 3 | MOVE
    MOVE_LEFT = 4 | MOVE


class Position:
    """
    Component describing the Position of the player
    """
    def __init__(self, y=0, x=0):
        self.x_coord = x
        self.y_coord = y
