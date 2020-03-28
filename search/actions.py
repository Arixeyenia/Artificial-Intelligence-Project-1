from search.game import Piece, Stack, Directions

#Move action functions that actually does the action on the piece i.e. piece will change
def move_left(board_dict, piece, spaces):
    coord = piece.coordinates
    new_coord = valid_move_check(board_dict, piece, Directions.left, spaces)
    if new_coord:
        if board_dict[coord].number == 1:
            board_dict[new_coord] = board_dict[coord]
            del board_dict[coord]
        elif board_dict[coord].number > 1:
            board_dict[new_coord] = Stack([piece], piece.colour)
            board_dict[coord].remove_piece(piece)
        piece.set_coordinates(new_coord)
        return True
    else:
        return False

def move_right(board_dict, piece, spaces):
    coord = piece.coordinates
    new_coord = valid_move_check(board_dict, piece, Directions.right, spaces)
    if new_coord:
        if board_dict[coord].number == 1:
            board_dict[new_coord] = board_dict[coord]
            del board_dict[coord]
        elif board_dict[coord].number > 1:
            board_dict[new_coord] = Stack([piece], piece.colour)
            board_dict[coord].remove_piece(piece)
        piece.set_coordinates(new_coord)
        return True
    else:
        return False

def move_up(board_dict, piece, spaces):
    coord = piece.coordinates
    new_coord = valid_move_check(board_dict, piece, Directions.up, spaces)
    if new_coord:
        if board_dict[coord].number == 1:
            board_dict[new_coord] = board_dict[coord]
            del board_dict[coord]
        elif board_dict[coord].number > 1:
            board_dict[new_coord] = Stack([piece], piece.colour)
            board_dict[coord].remove_piece(piece)
        piece.set_coordinates(new_coord)
        return True
    else:
        return False

def move_down(board_dict, piece, spaces):
    coord = piece.coordinates
    new_coord = valid_move_check(board_dict, piece, Directions.down, spaces)
    if new_coord:
        if board_dict[coord].number == 1:
            board_dict[new_coord] = board_dict[coord]
            del board_dict[coord]
        elif board_dict[coord].number > 1:
            board_dict[new_coord] = Stack([piece], piece.colour)
            board_dict[coord].remove_piece(piece)
        piece.set_coordinates(new_coord)
        return True
    else:
        return False

#check if moving piece to specified direction is a valid move i.e. not blocked by wall or enemy token
def valid_move_check(board_dict, piece, direction, spaces):
    if direction == Directions.left:
        new_coord = (piece.coordinates[0] - spaces, piece.coordinates[1])
        if new_coord[0] < 0 or (new_coord in board_dict and board_dict[new_coord] == 'B'):
            return False
        else:
            return new_coord

    if direction == Directions.right:
        new_coord = (piece.coordinates[0] + spaces, piece.coordinates[1])
        if new_coord[0] > 7 or (new_coord in board_dict and board_dict[new_coord] == 'B'):
            return False
        else:
            return new_coord

    if direction == Directions.up:
        new_coord = (piece.coordinates[0], piece.coordinates[1] + spaces)
        if new_coord[1] > 7 or (new_coord in board_dict and board_dict[new_coord] == 'B'):
            return False
        else:
            return new_coord

    if direction == Directions.down:
        new_coord = (piece.coordinates[0], piece.coordinates[1] - spaces)
        if new_coord[1] < 0 or (new_coord in board_dict and board_dict[new_coord] == 'B'):
            return False
        else:
            return new_coord

#boom a piece - uses range_check and remove_pieces
#will actually take the action
def boom(board_dict, piece):
    pieces = range_check(board_dict, piece)
    pieces.append(piece)
    remove_stack(board_dict, pieces)
    

#remove stack from the game/dict
def remove_stack(board_dict, stacks):
    for stack in stacks:
        coord = stack.coordinates
        board_dict.pop(coord)

#return pieces that is in the range of the piece specified
def range_check(board_dict, piece):
    coordinates = piece.coordinates
    stacks = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)
    
    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            print(check_coord in board_dict)
            if check_coord in board_dict:
                if (x == 1 and y == 1):
                    continue
                stacks.append(board_dict[check_coord])


    return stacks