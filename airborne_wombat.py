
def wombat(state, time_left):
    import random
    from collections import namedtuple
    Coordinates = namedtuple('Coordinates', ('row', 'col'))

    actions = ['turn', 'move', 'shoot', 'smoke']
    turn_directions = ['right', 'left', 'about-face']
    smoke_directions = ['forward', 'behind', 'left', 'right']

    arena = state['arena']
    local_coords = Coordinates(arena['local-coordinates'])
    hp = arena[local_coords.row][local_coords.col]['contents']['hp']

    action = None
    metadata = {}
    state = {'coords': local_coords, 'hp': hp }

    action = random.choice(actions)

    if action is 'turn':
        direction = random.choice(turn_directions)
        metadata['direction'] = direction
    elif action is 'smoke':
        direction = random.choice(smoke_directions)
        metadata['direction'] = direction

    command = { 'command': {
        'action': action,
        'metadata': metadata,
        },
        'state': state
    }


    return command
