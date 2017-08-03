
def wombat(state, time_left):
    import random
    actions = ['turn', 'move', 'shoot', 'smoke']
    turn_directions = ['right', 'left', 'about-face']
    smoke_directions = ['forward', 'behind', 'left', 'right']


    action = None
    metadata = {}
    state = {}

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
