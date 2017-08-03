
def wombat(state, time_left):
    import random
    import time
    from collections import namedtuple

    random.seed(time.time())

    Coordinates = namedtuple('Coordinates', ('row', 'col'))
    SHOOT = 'shoot'
    MOVE = 'move'
    TURN = 'turn'
    SMOKE = 'smoke'
    FOOD = 'food'

    actions = ['turn', 'move', 'shoot', 'smoke']
    turn_directions = ['right', 'left', 'about-face']
    smoke_directions = ['forward', 'behind', 'left', 'right']
    orientations = {'n': 0,
                    'e': 1,
                    's': 2,
                    'w': 3}

    #functions
    def check_for_enemy(arena, row, col):
        contents = arena[row][col]
        other_wombat = contents.get('type', None)
        if other_wombat == 'zakano' or other_wombat == 'wombat' or other_wombat == 'wood-barrier':
            return True
        else:
            return False

    def whats_in_front(arena, coords, orientation):
        row = coords.row
        col = coords.col
        if orientation == 'n':
            row = row - 1
        elif orientation == 's':
            row = row + 1
        elif orientation == 'e':
            col = col + 1
        else:
            col = col - 1

        if row < 0 or row >= len(arena) or col < 0 or col >= len(arena):
            return None

        contents = arena[row][col]['contents']
        return contents.get('type', None)

    def get_contents(arena, row, col):
        return arena[row][col]['contents']['type']

    def adj_items(arena, coords):
        row = coords.row
        col = coords.col
        return [get_contents(arena, row - 1, col),
                get_contents(arena, row, col + 1),
                get_contents(arena, row + 1, col),
                get_contents(arena, row, col - 1)]


    arena = state['arena']
    local_coords = Coordinates(*[int(x) for x in state['local-coords']])
    global_coords = Coordinates(*[int(x) for x in state['global-coords']])
    global_dimensions = Coordinates(*[int(x) for x in state['global-dimensions']])

    me = arena[local_coords.row][local_coords.col]['contents']
    hp = me['hp']
    orientation = me['orientation']
    action = None
    metadata = {}
    in_front = whats_in_front(arena, local_coords, orientation)

    # first see if we can blaze something
    if orientation == 'n':
        # look all rows above us
        for row in range(0, local_coords.row):
            if check_for_enemy(arena, row, local_coords.col):
                action = SHOOT
                break
    elif orientation == 's':
        #all rows below
        for row in range(local_coords.row + 1, len(arena)):
            if check_for_enemy(arena, row, local_coords.col):
                action = SHOOT
                break
    elif orientation == 'e':
        #all cols to right
        for col in range(local_coords.col + 1, len(arena)):
            if check_for_enemy(arena, local_coords.row, col):
                action = SHOOT
                break
    else:
        #all cols left
        for col in range(0, local_coords.col):
            if check_for_enemy(arena, local_coords.row, col):
                action = SHOOT
                break

    if not action:
        next_to = adj_items(arena, local_coords)
        if next_to[orientations[orientation]] == FOOD:
            action = MOVE
        elif FOOD in next_to:
            action = TURN

            dir_to_food = 0
            while next_to[dir_to_food] != FOOD:
                dir_to_food = dir_to_food + 1

            current_orientation = orientations[orientation]

            if dir_to_food == current_orientation + 1 % 4:
                direction = 'right'
            elif dir_to_food == current_orientation - 1 % 4:
                direction = 'left'
            else:
                direction = 'about-face'

            metadata['direction'] = direction
        else:
            move_or_turn = [MOVE, TURN]
            action = random.choice(move_or_turn)
            if action == MOVE:
                direction = random.choice(turn_directions)
                metadata['direction'] = direction


    save_state = {'coords': local_coords,
                  'hp': hp,
                  'prev_action': action,
                  'prev_orientation': orientation,
                  'in_front': in_front
                  }

    command = { 'command': {
        'action': action,
        'metadata': metadata,
        },
        'state': save_state
    }


    return command
