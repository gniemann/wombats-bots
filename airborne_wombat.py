
def wombat(state, time_left):
    import random
    import time
    from collections import namedtuple

    class Actions():
        shoot = 'shoot'
        move = 'move'
        turn = 'turn'
        smoke = 'smoke'

    class TurnDirections():
        right = 'right'
        left = 'left'
        behind = 'about-face'

        @classmethod
        def random_direction(cls):
            return random.choice([cls.right, cls.left, cls.behind])

    class SmokeDirections():
        forward = 'forward'
        behind = 'behind'
        left = 'left'
        right = 'right'

        @classmethod
        def random_direction(cls):
            return random.choice([cls.forward, cls.behind, cls.left, cls.right])

    class Items():
        food = 'food'
        wood_barrier = 'wood-barrier'
        open = 'open'

    Point = namedtuple('Point', ('row', 'col'))

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
        return contents == 'zakano' or contents == 'wombat'

    def visible_enemies(arena, coords):
        enemy_coords = []
        for row in range(len(arena)):
            col = coords.col
            if row != coords.row and check_for_enemy(arena, row, col):
                enemy_coords.append(Point(row, col))
        for col in range(len(arena)):
            row = coords.row
            if col != coords.col and check_for_enemy(arena, row, col):
                enemy_coords.append(Point(row, col))

        return enemy_coords

    # action commands
    def command(action, metadata=None):
        if not metadata:
            metadata = {}
        return {
            'action': action,
            'metadata': metadata
        }


    def shoot():
        return command(Actions.shoot)

    def turn(direction):
        metadata = {
            'direction': direction
        }
        return command(Actions.turn, metadata)

    def smoke(direction):
        metadata = {
            'direction': direction
        }
        return command(Actions.smoke, metadata)

    def move():
        return command(Actions.move)

    def commandToReturn(action, orientation, in_front, direction=None):
        command = ''
        if action is Actions.shoot:
            command = shoot()
        elif action is Actions.move:
            command = move()
        elif action is Actions.turn:
            command = turn(direction)
        elif action is Actions.smoke:
            command = smoke(direction)

        save_state = {
            'orientation': orientation,
            'in_front': in_front,
            'prev_action': action
        }

        return {
            'command': command,
            'state': save_state
        }

    def get_turn_direction(currentOrientation, requiredOrientation):
        if (current_orientation + 1) % 4 == requiredOrientation:
            return TurnDirections.right
        elif (current_orientation - 1) % 4 == requiredOrientation:
            return TurnDirections.left
        else:
            return TurnDirections.behind

    random.seed(time.time())
    arena = state['arena']
    local_coords = Point(*[int(x) for x in state['local-coords']])
    global_coords = Point(*[int(x) for x in state['global-coords']])
    global_dimensions = Point(*[int(x) for x in state['global-dimensions']])

    me = arena[local_coords.row][local_coords.col]['contents']
    hp = me['hp']
    orientation = me['orientation']
    metadata = {}
    next_to = adj_items(arena, local_coords)
    current_orientation = orientations[orientation]
    in_front = next_to[current_orientation]

    enemies = visible_enemies(arena, local_coords)

    # first see if we can blaze something
    for (enemy_row, enemy_col) in enemies:
        if ((orientation == 'n' and enemy_col == local_coords.col and enemy_row < local_coords.row) or
            (orientation == 'e' and enemy_row == local_coords.row and enemy_col > local_coords.col) or
            (orientation == 's' and enemy_col == local_coords.col and enemy_row > local_coords.row) or
            (orientation == 'w' and enemy_row == local_coords.row and enemy_col < local_coords.col)):
            return commandToReturn(Actions.shoot, orientation, in_front)

    # next see if an enemy is pointed at us - if so move, if not turn towards them to blaze em next time
    for (enemy_row, enemy_col) in enemies:
        enemy = get_contents(arena, enemy_row, enemy_col)
        enemy_orientation = enemy['orientation']
        if enemy_row == local_coords.row:
            #east or west
            if enemy_col < local_coords.col:
                #enemy is west
                if enemy_orientation == 'e':
                    #pointed at us
                    return commandToReturn(Actions.move, orientation, in_front)
                else:
                    direction = get_turn_direction(current_orientation, orientations['w'])
                    return commandToReturn(Actions.turn, orientations, in_front, direction)
            else :
                #enemy is east
                if enemy_orientation == 'w':
                    return  commandToReturn(Actions.move, orientation, in_front)
                else:
                    direction = get_turn_direction(current_orientation, orientations['e'])
                    return commandToReturn(Actions.turn, orientation, in_front, direction)
        else:
            #north or south
            if enemy_row < local_coords.row:
                #enemy is north
                if enemy_orientation == 's':
                    return commandToReturn(Actions.move, orientations, in_front)
                else:
                    direction = get_turn_direction(current_orientation, orientations['n'])
                    return commandToReturn(Actions.turn, orientation, in_front, direction)
            else:
                #enemy is south
                if enemy_orientation == 'n':
                    return commandToReturn(Actions.move, orientation, in_front)
                else:
                    direction = get_turn_direction(current_orientation, orientations['s'])
                    return commandToReturn(Actions.turn, orientation, in_front, direction)



    if in_front == Items.food:
        return commandToReturn(Actions.move, orientation, in_front)
    elif Items.food in next_to:
        dir_to_food = 0
        while next_to[dir_to_food] != Items.food:
            dir_to_food = dir_to_food + 1

        direction = get_turn_direction(current_orientation, dir_to_food)

        return commandToReturn(Actions.turn, orientation, in_front, direction)
    elif in_front == Items.wood_barrier:
        return commandToReturn(Actions.shoot, orientation, in_front)
    elif in_front != Items.open:
        return commandToReturn(Actions.turn, orientation, in_front, TurnDirections.random_direction())
    else:
        move_or_turn = [Actions.move, Actions.turn]
        action = random.choice(move_or_turn)

        if action == Actions.move:
            return commandToReturn(action, orientation, in_front)
        elif action == Actions.turn:
            return commandToReturn(action, orientation, in_front, TurnDirections.random_direction())