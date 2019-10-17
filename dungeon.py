"""
Dungeon : Generate the levels for the dungeon
"""

from random import randint


class dungeon:
    """
    Dungeon Class that allows to control the current situation of our code
    """
    def __init__(self, board):
        self.board = board

    @staticmethod
    def randomGeneration():
        """
        Generate a random dungeon
        """

        # Generate dimensions
        width = round(randint(500, 1500), 2)
        length = round(randint(500, 1500), 2)

        # 
