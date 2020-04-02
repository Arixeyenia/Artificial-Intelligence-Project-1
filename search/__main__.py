import sys
import json

from search.util import print_move, print_boom, print_board
from search.game import Piece, Stack, Board, Directions
from search.actions import move, valid_move_check, boom, remove_stack, range_check

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        black_data = data["black"]
        
        #TODO: REMOVE AFTER COMPLETION
        print(black_data)

        black_dict = {}
        for input_stack in black_data:
            coords = tuple(input_stack[1:])

            no_pieces = input_stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "B"))

            stack = Stack(Pieces, "B")
            black_dict[coords] = stack

        white_data = data["white"]
        white_dict = {}
        #TODO: REMOVE AFTER COMPLETION
        print(white_data)
        
        for input_stack in white_data:
            coords = tuple(input_stack[1:])

            no_pieces = input_stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "W"))

            stack = Stack(Pieces, "W")
            white_dict[coords] = stack

        board = Board(black_dict, white_dict)
        board_dict = board.get_board_dict()
        print_board(board_dict)

        for key, value in board_dict.items():
            print(str(key) + ": " + str(value))
    # TODO: find and print winning action sequence



# TODO: output moves
def output_moves():
    print("Output moves here")

if __name__ == '__main__':
    main()
    