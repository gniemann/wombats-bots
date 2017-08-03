
def wombat(state, time_left):
    import random
    from collections import namedtuple
    Coordinates = namedtuple('Coordinates', ('row', 'col'))

    actions = ['turn', 'move', 'shoot', 'smoke']
    turn_directions = ['right', 'left', 'about-face']
    smoke_directions = ['forward', 'behind', 'left', 'right']

    arena = state['arena']
    local_coords = Coordinates((int(x) for x in arena['local-coordinates']))
    hp = arena[local_coords.row][local_coords.col]['contents']['hp']

    action = None
    metadata = {}
    state = {'coords': local_coords, 'hp': hp }



    saved_state = state['saved-state']

    if saved_state and saved_state['prev_action'] is 'turn':
        action = 'shoot'
    else:
        action = 'turn'
        direction = random.choice(turn_directions)
        metadata['direction'] = direction

    command = { 'command': {
        'action': action,
        'metadata': metadata,
        },
        'state': state
    }


    return command
