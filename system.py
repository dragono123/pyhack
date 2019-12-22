"""
System : System Management
"""

import components
import curses

def system_update_pos(registry, dungeon):
    player = registry.get_multiple_components(components.Player,
                                              components.Position)[0]
    player_action = registry.entities[player][components.Player]
    position = registry.entities[player][components.Position]
    if player_action.action & components.Action_List.MOVE != 0:
        new_x, new_y = position.x_coord, position.y_coord
        if player_action.action == components.Action_List.MOVE_UP:
            new_y -= 1
        elif player_action.action == components.Action_List.MOVE_DOWN:
            new_y += 1
        elif player_action.action == components.Action_List.MOVE_LEFT:
            new_x -= 1
        elif player_action.action == components.Action_List.MOVE_RIGHT:
            new_x += 1
        if test_move(dungeon, (new_y, new_x)):
            dungeon.board[position.y_coord][position.x_coord] = 0
            dungeon.board[new_y][new_y] = player
            position.y = new_y
            position.x = new_x
        else:
            player_action = components.Action_List.NOTHING


def test_move(dungeon, position):
    new_y, new_x = position[0]
    is_valid = new_y in range(len(dungeon.board)) \
             and new_x in range(len(dungeon.board[0]))
    is_valid = is_valid and dungeon.board[new_y][new_x] == 0
    return is_valid


def get_action(registry, stdscr):
    key = stdscr.getch()
    player = registry.get_single_component(components.Player)
    if key == curses.KEY_UP:
        player.action = components.Action_List.MOVE_UP
    elif key == curses.KEY_DOWN:
        player.action = components.Action_List.MOVE_DOWN
    elif key == curses.KEY_LEFT:
        player.action = components.Action_List.MOVE_LEFT
    elif key == curses.KEY_RIGHT:
        player.action = components.Action_List.MOVE_RIGHT
    

def system_get_action(registry, dungeon, stdscr):
    player = registry.get_single_components(components.Player)[0]
    while player.action == components.Action_List.NOTHING:
        get_action(registry, stdscr)
        system_update_pos(registry, dungeon)

    player.action = components.Action_List.NOTHING

    

def system(registry, dungeon, stdscr):
    """
    Launch all system rules
    """
    system_get_action(registry, dungeon, stdscr)
