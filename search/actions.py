from game import Piece, Stack, Directions, Board

# Move action function that actually does the action on the piece i.e. piece will changee
# takes in neighbours of a current state, and the piece itself, 
# returns a copy of a new potetial

# explores the possible adjacent tiles and return the state of the board
def explore(board, stack, no_pieces, spaces, direction):
    
    # TODO:
    # Explore is going to be called over and over to explore the neighbouring
    # tiles, therefore the value of board and stack must be updated as well.
    # Explore is used in a_search.py to expand neighbouring coordinates, but right now it can only
    # explore the neighbouring node of the initial node.
    
    coord = stack.coordinates 
    print("First coord: ", coord)

    new_coord = valid_move_check(board, stack, no_pieces, direction, spaces)
    pieces = stack.pieces[:no_pieces]

    new_board = board.get_copy()

    if new_coord:

        if board.white[coord].number == no_pieces:
            new_board.white[coord] = new_board.white[coord]
            new_board.white[new_coord] = board.white[coord]
            
            # new_board.white[new_coord].coordinates = new_coord
            # ^^^^
            # If i try to update the new coordinate of the stack, 
            # the value of coord = stack.coordinates will also change and 
            # will cause KeyError
        
            new_board.white[new_coord].prev_coordinates = coord
            del new_board.white[coord]
            # ^^^^
            # Doing this will also cause a KeyError

        elif new_board.white[coord].number > no_pieces:
            new_board.white[new_coord] = Stack(pieces, stack.colour)
            new_board.white[coord].remove_pieces(pieces)

        for piece in pieces:
            piece.set_coordinates(new_coord)
            piece.coordinates = new_coord
        return new_board
    else:
        return False

def move(board, stack, no_pieces, spaces, direction):
    coord = stack.coordinates
    new_coord = valid_move_check(board, stack, no_pieces, direction, spaces)
    pieces = stack.pieces[:no_pieces]

    for piece in pieces:
        piece.set_coordinates(new_coord)
        
    if new_coord:
        if board.white[coord].number == no_pieces:
            if new_coord in board.white:
                board.white[new_coord].add_stack(board.white[coord])
            else:
                board.white[new_coord] = board.white[coord]
                board.white[new_coord].set_coordinates(new_coord)
            del board.white[coord]
        elif board.white[coord].number > no_pieces:
            board.white[new_coord] = Stack(pieces, stack.colour)
            board.white[coord].remove_pieces(pieces)

        return board.white[new_coord]
    else:
        return False

# check if moving piece to specified direction is a valid move i.e. not blocked by wall or enemy token


def valid_move_check(board, stack, no_pieces, direction, spaces):
    if stack.number < no_pieces or stack.number < spaces:
        return False

    if direction == Directions.left:
        new_coord = (stack.coordinates[0] - spaces, stack.coordinates[1])
        if new_coord[0] < 0 or (new_coord in board.black):
            return False
        else:
            return new_coord

    if direction == Directions.right:
        new_coord = (stack.coordinates[0] + spaces, stack.coordinates[1])
        if new_coord[0] > 7 or (new_coord in board.black):
            return False
        else:
            return new_coord

    if direction == Directions.up:
        new_coord = (stack.coordinates[0], stack.coordinates[1] + spaces)
        if new_coord[1] > 7 or (new_coord in board.black):
            return False
        else:
            return new_coord

    if direction == Directions.down:
        new_coord = (stack.coordinates[0], stack.coordinates[1] - spaces)
        if new_coord[1] < 0 or (new_coord in board.black):
            return False
        else:
            return new_coord

# boom a stack - uses range_check and remove_stack
# will actually take the action


def boom(board, stack):
    stacks = range_check(board, stack)
    remove_stack(board, stack)
    for stack in stacks:
        boom(board, stack)

# remove stack from the game/dict


def remove_stack(board, stack):
    if stack.coordinates in board.get_board_dict():
        coord = stack.coordinates
        if stack.colour == 'B':
            board.black.pop(coord)
        elif stack.colour == 'W':
            board.white.pop(coord)

# return stacks that is in the range of the stack specified


def range_check(board, stack):
    coordinates = stack.coordinates
    stacks = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.get_board_dict():
                if (x == 1 and y == 1):
                    continue
                stacks.append(board.get_board_dict()[check_coord])
    return stacks

# return white stacks that is in the range of the stack specified


def white_range_check(board, stack):
    coordinates = stack.coordinates
    stacks = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.white:
                if (x == 1 and y == 1):
                    continue
                stacks.append(board.white[check_coord])
    return stacks

# return black stacks that is in the range of the stack specified


def black_range_check(board, stack):
    coordinates = stack.coordinates
    stacks = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.black:
                if (x == 1 and y == 1):
                    continue
                stacks.append(board.black[check_coord])
    return stacks
