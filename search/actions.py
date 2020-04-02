from search.game import Piece, Stack, Directions

#Move action function that actually does the action on the piece i.e. piece will changee
def move(board, stack, no_pieces, spaces, direction):
    coord = stack.coordinates
    new_coord = valid_move_check(board, stack, no_pieces, direction, spaces)
    pieces = stack.pieces[:no_pieces]

    if new_coord:
        if board.white[coord].number == no_pieces:
            board.white[coord] = board.white[coord]
            board.white[new_coord].set_coordinates(new_coord)
            del board.white[coord]
        elif board.white[coord].number > no_pieces:
            board.white[new_coord] = Stack(pieces, stack.colour)
            board.white[coord].remove_pieces(pieces)

        for piece in pieces:
            piece.set_coordinates(new_coord)
        return True
    else:
        return False

#check if moving piece to specified direction is a valid move i.e. not blocked by wall or enemy token
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

#boom a piece - uses range_check and remove_pieces
#will actually take the action
def boom(board, piece):
    pieces = range_check(board, piece)
    pieces.append(piece)
    remove_stack(board, pieces)    

#remove stack from the game/dict
def remove_stack(board, stacks):
    for stack in stacks:
        coord = stack.coordinates
        if stack.colour == 'B':
            board.black.pop(coord)
        elif stack.colour == 'W':
            board.white.pop(coord)

#return pieces that is in the range of the piece specified
def range_check(board, piece):
    coordinates = piece.coordinates
    stacks = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.get_board_dict:
                if (x == 1 and y == 1):
                    continue
                stacks.append(board.get_board_dict[check_coord])
    return stacks