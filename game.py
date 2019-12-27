#!/usr/bin/env python3
"""
Game : Executable file
"""

import curses
from dungeon import Dungeon
from system import start_system
import entities


def main():
    """
    Main function
    """
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.curs_set(False)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    dungeon = Dungeon().random_generation()
    registry = entities.Registry()

    entities.add_entities(dungeon, registry)

    while True:
        start_system(registry, dungeon, stdscr)


if __name__ == "__main__":
    main()
