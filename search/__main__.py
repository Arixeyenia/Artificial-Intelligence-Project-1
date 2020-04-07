import sys
import json

from search.util import print_move, print_boom, print_board
from search.game import Piece, Stack, Board, Cluster, Directions
from search.actions import move, valid_move_check, boom, remove_stack, range_check
from search.goal_search import get_black_range, get_all_black_ranges, get_cluster, get_goal_tiles, get_intersections, check_chaining, match_with_white, goal_state
from search.a_star import a_star_search, a_star_main, explore_neighbours
from search.bfs import bfs


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        black_data = data["black"]

        # TODO: REMOVE AFTER COMPLETION
        # print(black_data)

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
        # TODO: REMOVE AFTER COMPLETION
        # print(white_data)

        for input_stack in white_data:
            coords = tuple(input_stack[1:])

            no_pieces = input_stack[0]
            Pieces = []
            for x in range(no_pieces):
                Pieces.append(Piece(coords, "W"))

            stack = Stack(Pieces, "W")
            white_dict[coords] = stack

        board = Board(black_dict, white_dict)
        goal_board = Board(black_dict, white_dict)
        # print(board.black)
             # Find the range of all black tiles
        all_black_range = get_all_black_ranges(board)
        print("All black range: " + str(all_black_range) + "\n")

        # Combine ranges of black tokens to take into account chain explosions
        chaining_range = check_chaining(board)
        print("Chaining range: " + str(chaining_range) + "\n")

        # Find the intersections of adjacent black tokens
        get_intersection = get_intersections(board)
        print("Intersections: " + str(get_intersection) + "\n")

        # Find the clusters of black tokens
        clusters = get_cluster(board)
        print("Cluster: " + str(clusters) + "\n")

        list_of_goal_tiles = get_goal_tiles(clusters)
        print("Goals: " + str(list_of_goal_tiles))

        # Match a black cluster with a white token
        match_pairs = match_with_white(board, list_of_goal_tiles)
        print("matching: " + str(match_pairs))
        

        board_dict = board.get_board_dict()
        # set up the goals
        goals = set_up_goal(goal_board, list_of_goal_tiles, match_pairs)
        print_board(board_dict)
        

        goal_dict_list = []
        
        for goal in goals:
            goal_dict = goal
            goal_dict_list.append(goal_dict)
            
            # print_board(goal_dict)
            # for key, value in goal_dict.items():
            #     print(str(key) + ": " + str(value))
        white_stacks = []
        for key, value in board.white.items():
            white_stacks.append(board.white[key])
            
        bfs(board, goal_state, white_stacks, white_stacks[0])
        # total_paths = a_star_main(board, goal_dict_list, match_pairs)
        # print(total_paths)
        # for key, value in board_dict.items():
        #     print(str(key) + ": " + str(value))

    # TODO: find and print winning action sequence

    # lets say theres only one Stack (piece)
    # path = a_star_search(board, white_stack.coordinate, end_coordinate)
    # path will be saved as stacks, everything else is just coordinate.
    # path = [Stack.coord, Stack.coord]

    # white_stacks = board_white
    # for white_stack in white_stacks
        # # do a_star_search for all the white pieces

        # path = a_star_search(board, white_stack.coordinate, find_nearest_black_range(black_stacks))

# 



def set_up_goal(board, list_of_goal_tiles, match_pairs):

    # Get a list of boards of the final states
    goal_states = goal_state(board, list_of_goal_tiles, match_pairs)
    print("goal state: " + str(goal_states))

    return goal_states


# TODO: output moves
def output_moves():
    print("Output moves here")


if __name__ == '__main__':
    main()
