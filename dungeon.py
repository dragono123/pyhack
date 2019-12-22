"""
Dungeon : Generate the levels for the dungeon
"""

import random


class Leaf:
    """
    Leaf Class representing each node in a binary tree.
    Used to generate each rooms
    """
    def __init__(self, x, y, width, height):
        self.coords = (y, x)
        self.dims = (height, width)
        self.child_1 = None
        self.child_2 = None
        self.room = None

    def split(self, leaf_min_size, horizontal=True):
        """
        Split the leaf in two new leafs
        """

        def create_new_dim(dim):
            """Generate a new random dimension"""
            while True:
                new_dim = random.gauss(dim/2, dim/4)
                if dim/5 <= new_dim <= dim - dim/5 and leaf_min_size \
                        < new_dim and leaf_min_size < dim - new_dim:
                    break
            return int(new_dim)

        y_coord, x_coord = self.coords
        height, width = self.dims
        if horizontal:
            if width <= 2*leaf_min_size:
                return False
            new_width = create_new_dim(width)
            leaf_1 = Leaf(x_coord, y_coord, new_width, height)
            leaf_2 = Leaf(x_coord + new_width, y_coord,
                          width - new_width, height)

        else:
            if height <= 2*leaf_min_size:
                return False
            new_height = create_new_dim(height)
            leaf_1 = Leaf(x_coord, y_coord, width, new_height)
            leaf_2 = Leaf(x_coord, y_coord + new_height, width,
                          height - new_height)

        self.child_1, self.child_2 = leaf_1, leaf_2

        return True

    def __str__(self):
        return "{} {} : {} {}".format(self.coords[1], self.coords[0],
                                      self.dims[0], self.dims[1])

    def add_rooms(self, dungeon):
        """
        Keep looking until the leaf has no child.
        Then create a new room with the child
        """
        if self.child_1:
            self.child_1.add_rooms(dungeon)
            self.child_2.add_rooms(dungeon)
            dungeon.create_corridor(self.child_1.get_random_room(),
                                    self.child_2.get_random_room())
        else:
            y_coord, x_coord = self.coords
            height, width = self.dims
            room_width = random.randint(dungeon.room_min_size, width - 1)
            room_height = random.randint(dungeon.room_min_size, height - 1)
            room_x = random.randint(x_coord, x_coord +
                                    width - 1 - room_width)
            room_y = random.randint(y_coord, y_coord +
                                    height - 1 - room_height)
            self.room = Room(room_x, room_y, room_width, room_height)
            dungeon.create_room(self.room)

    def get_random_room(self):
        """ Return a random room from the tree """
        if not self.room:
            return random.choice((self.child_1, self.child_2)).\
                    get_random_room()
        return self.room

class Room:
    """
    Room
    """
    def __init__(self, x, y, width, height):
        self.coords = (y, x)
        self.dims = (height, width)

    def get_center(self):
        """
        Return the center of the room
        """
        return (self.coords[0] + self.dims[0]//2, self.coords[1]
                + self.dims[1]//2)


class Dungeon:
    """
    Dungeon Class that allows us to store data about our dungeon
    """
    def __init__(self):
        # init dimensions
        self.width = 80
        self.height = 60
        self.room_min_size = 5
        self.board = [[0 for _ in range(self.width)]
                      for _ in range(self.height)]
        self.rooms = []

    def random_generation(self):
        """
        Generate a random dungeon
        """

        leaf_min_size = 10
        root = Leaf(0, 0, self.width, self.height)

        def leaf_spliting(leaf):
            """
            Split each leafs recursively until the new leaf cannot be split
            """

            if leaf.split(leaf_min_size, leaf.dims[1] > leaf.dims[0]):
                leaf_spliting(leaf.child_1)
                leaf_spliting(leaf.child_2)
            return True

        leaf_spliting(root)
        root.add_rooms(self)
        return self

    def __str__(self):
        string = ""

        def format_char(char):
            if char == 1:
                return '\x1b[0;30;47m' + '.' + '\x1b[0m'
            if char == 2:
                return '\x1b[0;30;45m' + '#' + '\x1b[0m'
            return '\x1b[0;32;40m' + ' ' + '\x1b[0m'

        for line in self.board:
            str_line = "".join(format_char(c) for c in line)
            string += str_line + '\n'
        return string

    def create_room(self, room):
        """ Add the room to the board """
        self.rooms.append(room)
        room_y, room_x = room.coords
        room_height, room_width = room.dims
        for line in range(room_y, room_y + room_height):
            for col in range(room_x, room_x + room_width):
                self.board[line][col] = 1

    def create_corridor(self, room_1, room_2):
        """
        Create a hall from two rooms
        """
        center_1 = room_1.get_center()
        center_2 = room_2.get_center()
        if random.getrandbits(1) == 0:
            for y_coord in range(center_1[0], center_2[0]):
                self.board[y_coord][center_1[1]] = 1
            for x_coord in range(center_1[1], center_2[1]):
                self.board[center_2[0]][x_coord] = 1
        else:
            for x_coord in range(center_1[1], center_2[1]):
                self.board[center_1[0]][x_coord] = 1
            for y_coord in range(center_1[0], center_2[0]):
                self.board[y_coord][center_2[1]] = 1


if __name__ == "__main__":
    FLOOR = Dungeon().random_generation()
    print(FLOOR)
