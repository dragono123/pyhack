#!/usr/bin/env python3


import curses
from dungeon import Dungeon
from system import system
import entities
import components


def game(stdscr, dungeon, registry):
    stdscr.clear()
    system(registry, dungeon)
    stdsrc.refresh()


def main():
    """
    Main function used to start the program
    """
    curses.curs_set(False)
    stdscr = curses.initscr()

    dungeon = Dungeon().random_generation()
    registry = entities.Registry()

    while True:
        game(stdscr, dungeon, registry)


if __name__ == "__main__":
    main()
