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

class Action_List(enum.IntFlag):
    NOTHING = 0
    MOVE = 8
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Position:
    """
    Component describing the Position of the player
    """
    def __init__(self, y=0, x=0):
        self.x_coord = x
        self.y_coord = y


class Icon:
    """
    How the entity is represented in the display
    """
    def __init__(self, display):
        self.display = display
