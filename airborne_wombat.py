import json

def wombat(state, time_left):
    action = 'turn'
    metadata = {'direction': 'right'}
    state = {'hello': 'world'}


    command = { 'command': {
        'action': action,
        'metadata': metadata,
        },
        'state': state
    }

    return json.dumps(command)

