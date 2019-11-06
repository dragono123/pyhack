"""
Dungeon : Generate the levels for the dungeon
"""

import random


class Room:
    """
    Room Class that describe each rooms during the generation process
    """
    def __init__(self, x_coord, y_coord, width, height):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height

    def split(self, vertical=True):
        """
        Split the room in two new rooms
        """
        def create_new_dim(dim):
            """Generate a new random dimension"""
            while True:
                new_dim = random.gauss(dim/2, dim/10)
                if dim/5 <= new_dim <= dim - dim/5:
                    break
            return int(new_dim)

        if vertical:
            new_height = create_new_dim(self.height)
            room_1 = Room(self.x_coord, self.y_coord, self.width, new_height)
            room_2 = Room(self.x_coord, self.y_coord + new_height, self.width,
                          self.height - new_height)

        else:
            new_width = create_new_dim(self.width)
            room_1 = Room(self.x_coord, self.y_coord, new_width, self.height)
            room_2 = Room(self.x_coord + new_width, self.y_coord,
                          self.width - new_width, self.height)

        return room_1, room_2


class Dungeon:
    """
    Dungeon Class that allows us to store data about our dungeon
    """
    def __init__(self, board):
        self.board = board

    @staticmethod
    def random_generation():
        """
        Generate a random dungeon
        """
        # starting dimensions
        width = 800
        height = 1200
        number_of_rooms = 20

        room = Room(0, 0, width, height)
