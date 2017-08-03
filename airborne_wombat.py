
def wombat(state, time_left):
    import random
    from collections import namedtuple
    Coordinates = namedtuple('Coordinates', ('row', 'col'))

    actions = ['turn', 'move', 'shoot', 'smoke']
    turn_directions = ['right', 'left', 'about-face']
    smoke_directions = ['forward', 'behind', 'left', 'right']

    arena = state['arena']
    local_coords = Coordinates(*[int(x) for x in state['local-coords']])
    hp = arena[local_coords.row][local_coords.col]['contents']['hp']

    action = None
    metadata = {}

    saved_state = state.get('saved-state', None)

    if saved_state and saved_state.get('prev_action', None) is 'turn':
        action = 'shoot'
    else:
        action = 'turn'
        direction = random.choice(turn_directions)
        metadata['direction'] = direction

    save_state = {'coords': local_coords,
                  'hp': hp,
                  'prev_action': action,
                  'old_state': state}

    command = { 'command': {
        'action': action,
        'metadata': metadata,
        },
        'state': save_state
    }


    return command
