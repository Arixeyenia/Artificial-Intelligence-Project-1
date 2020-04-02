import sys
import json

from search.util import print_move, print_boom, print_board
from search.game import Piece, Stack, Directions
from search.actions import move_left, move_right, move_up, move_down, valid_move_check, boom, remove_stack, range_check

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        black_data = data["black"]
        
        #TODO: REMOVE AFTER COMPLETION
        print(black_data)

        board_dict = {}
        for stack in black_data:
            coords = tuple(stack[1:])

            no_pieces = stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "B"))
            board_dict[coords] = Stack(Pieces, "B")

        white_data = data["white"]

        #TODO: REMOVE AFTER COMPLETION
        print(white_data)
        
        for stack in white_data:
            coords = tuple(stack[1:])

            no_pieces = stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "W"))
            board_dict[coords] = Stack(Pieces, "W")

        print_board(board_dict)
        for key, value in board_dict.items():
            print(str(key) + ": " + str(value))
    # TODO: find and print winning action sequence



# TODO: output moves
def output_moves():
    print("Output moves here")

if __name__ == '__main__':
    main()
    