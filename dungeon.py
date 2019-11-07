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
                new_dim = random.gauss(dim/2, dim/4)
                if dim/5 <= new_dim <= dim - dim/5:
                    break
            return int(new_dim)

        if vertical:
            new_width = create_new_dim(self.width)
            room_1 = Room(self.x_coord, self.y_coord, new_width, self.height)
            room_2 = Room(self.x_coord + new_width, self.y_coord,
                          self.width - new_width, self.height)

        else:
            new_height = create_new_dim(self.height)
            room_1 = Room(self.x_coord, self.y_coord, self.width, new_height)
            room_2 = Room(self.x_coord, self.y_coord + new_height, self.width,
                          self.height - new_height)

        return room_1, room_2

    def __str__(self):
        return "{} {} : {} {}".format(self.x_coord,
                                      self.y_coord, self.height, self.width)

    def fill(self, board):
        """
        Fill a 2D matrix using its specific schema
        """
        for line in range(self.y_coord, self.y_coord + self.height):
            for col in range(self.x_coord, self.x_coord + self.width):
                if line in (self.y_coord, self.y_coord + self.height - 1)\
                       or col in (self.x_coord, self.x_coord + self.width - 1):
                    board[line][col] = 2
                else:
                    board[line][col] = 1


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
        # init dimensions
        width = 80
        height = 60
        number_of_rooms = 5
        max_size = 20
        board = [[0 for _ in range(width)] for _ in range(height)]

        room = Room(0, 0, width, height)

        def room_spliting(room):
            """
            Split each rooms recursively until both width and height
            are below the minimum size
            """

            if room.width <= max_size and room.height <= max_size:
                return [room]

            room_1, room_2 = room.split(room.width > room.height)
            rooms_1 = room_spliting(room_1)
            rooms_2 = room_spliting(room_2)

            return rooms_1 + rooms_2

        rooms = room_spliting(room)
        random.shuffle(rooms)
        rooms = rooms[:number_of_rooms]
        for room in rooms:
            room.fill(board)
        return Dungeon(board)

    def __str__(self):
        string = ""

        def format_char(char):
            if char == 1:
                return '\x1b[0;30;47m' + '.' + '\x1b[0m'
            elif char == 2:
                return '\x1b[0;30;45m' + '#' + '\x1b[0m'
            return '\x1b[0;32;40m' + ' ' + '\x1b[0m'

        for line in self.board:
            str_line = "".join(format_char(c) for c in line)
            string += str_line + '\n'
        return string


if __name__ == "__main__":
    dungeon = Dungeon.random_generation()
    print(dungeon)
