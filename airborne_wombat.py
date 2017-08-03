def wombat(state, time_left):
    # Note that the function name MUST be wombat
    return {
        'command': {
            'action': 'turn',
            'metadata': {
                'direction': 'right'
            }
        },
        'state': {
            'hello': 'world'
        }
    }
