import sys
import json

from search.util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        black_data = data["black"]
        print(black_data)
        board_dict = {}
        for stack in black_data:
            coords = tuple(stack[1:])
            board_dict[coords] = "B"

        white_data = data["white"]
        print(white_data)
        for stack in white_data:
            coords = tuple(stack[1:])
            board_dict[coords] = "W"

        print_board(board_dict)
    # TODO: find and print winning action sequence

if __name__ == '__main__':
    main()
