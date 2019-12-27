"""
System : System Management
"""

import curses
import components

def system_update_pos(registry, dungeon):
    """
    If the player action is moving, move the player
    """
    player = registry.get_multiple_components(components.Player,
                                              components.Position)[0]
    player_action = registry.entities[player][components.Player]
    position = registry.entities[player][components.Position]
    if player_action.action & components.Action_List.MOVE != 0:
        new_x, new_y = position.x_coord, position.y_coord
        direction = player_action.action ^ components.Action_List.MOVE
        if direction == components.Action_List.UP:
            new_y -= 1
        elif direction == components.Action_List.DOWN:
            new_y += 1
        elif direction == components.Action_List.LEFT:
            new_x -= 1
        elif direction == components.Action_List.RIGHT:
            new_x += 1
        if test_move(dungeon, (new_y, new_x)):
            dungeon.board[position.y_coord][position.x_coord] = 1
            dungeon.board[new_y][new_x] = player
            position.y_coord = new_y
            position.x_coord = new_x
        else:
            player_action = components.Action_List.NOTHING


def test_move(dungeon, position):
    """
    Returns true if the player can move to the new position
    """
    new_y, new_x = position[0], position[1]
    is_valid = new_y in range(len(dungeon.board)) \
             and new_x in range(len(dungeon.board[0]))
    is_valid = is_valid and dungeon.board[new_y][new_x] == 1
    return is_valid


def get_action(registry, stdscr):
    """
    Get the current player action
    """
    player = registry.entities[registry.get_single_component(components.Player)[0]]\
                [components.Player]
    key = stdscr.getch()
    if key == curses.KEY_UP:
        player.action = components.Action_List.UP | components.Action_List.MOVE
    elif key == curses.KEY_DOWN:
        player.action = components.Action_List.DOWN | components.Action_List.MOVE
    elif key == curses.KEY_LEFT:
        player.action = components.Action_List.LEFT | components.Action_List.MOVE
    elif key == curses.KEY_RIGHT:
        player.action = components.Action_List.RIGHT | components.Action_List.MOVE


def display_dungeon(registry, dungeon, stdscr):
    """
    Display the dungeon
    """
    position = registry.entities[registry.get_single_component(components.Player)[0]]\
                [components.Position]

    height, width = stdscr.getmaxyx()

    stdscr.clear()
    for h in range(max(0, position.y_coord - height//2), min(position.y_coord + height//2 - 1, dungeon.height)):
        for w in range(max(0, position.x_coord - width//2), min(position.x_coord + width//2 - 1, dungeon.width)):
            min_y = position.y_coord - height//2
            min_x = position.x_coord - width//2
            if dungeon.board[h][w] == 1:
                character = '.'
                id_color = 1
            elif dungeon.board[h][w] > 1:
                entity = dungeon.board[h][w]
                character = registry.entities[entity][components.Icon].display
                id_color = 1
            else:
                character = ' '
                id_color = 2
            stdscr.addstr(h - min_y, w - min_x, character, curses.color_pair(id_color))
    stdscr.refresh()


def reset_action_player(registry):
    """
    Reset the player action so that he can move again
    """
    player = registry.entities[registry.get_single_component(components.Player)[0]]\
                [components.Player]
    player.action = components.Action_List.NOTHING


def start_system(registry, dungeon, stdscr):
    """
    Launch all system rules
    """
    display_dungeon(registry, dungeon, stdscr)
    get_action(registry, stdscr)
    system_update_pos(registry, dungeon)
    reset_action_player(registry)
