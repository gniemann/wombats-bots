
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
    def get_contents(arena, row, col):
        return arena[row][col]['contents']['type']

    def adj_items(arena, coords):
        row = coords.row
        col = coords.col
        return [get_contents(arena, row - 1, col),
                get_contents(arena, row, col + 1),
                get_contents(arena, row + 1, col),
                get_contents(arena, row, col - 1)]

    def check_for_enemy(arena, row, col):
        contents = get_contents(arena, row, col)
        return contents == 'zakano' or contents == 'wombat' or contents == 'wood-barrier'


    arena = state['arena']
    local_coords = Coordinates(*[int(x) for x in state['local-coords']])
    global_coords = Coordinates(*[int(x) for x in state['global-coords']])
    global_dimensions = Coordinates(*[int(x) for x in state['global-dimensions']])

    me = arena[local_coords.row][local_coords.col]['contents']
    hp = me['hp']
    orientation = me['orientation']
    action = None
    metadata = {}
    direction = None
    next_to = adj_items(arena, local_coords)
    current_orientation = orientations[orientation]
    in_front = next_to[current_orientation]

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
        if in_front == FOOD:
            action = MOVE
        elif in_front == 'wood-barrier':
            action = SHOOT
        elif FOOD in next_to:
            action = TURN

            dir_to_food = 0
            while next_to[dir_to_food] != FOOD:
                dir_to_food = dir_to_food + 1

            if dir_to_food == (current_orientation + 1) % 4:
                direction = 'right'
            elif dir_to_food == (current_orientation - 1) % 4:
                direction = 'left'
            else:
                direction = 'about-face'

        elif next_to[current_orientation] != 'open':
            action = TURN
            direction = random.choice(turn_directions)
        else:
            move_or_turn = [MOVE, TURN]
            action = random.choice(move_or_turn)

            if action == TURN:
                direction = random.choice(turn_directions)


    if action == TURN:
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
