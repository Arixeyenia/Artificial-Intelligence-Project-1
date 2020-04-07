# a_star_search(board_dict, start_node, goal_node): return path from start_node -> goal_node (an array of board dicts)

from operator import itemgetter

from search.game import Piece, Stack, Board, Cluster, Directions
from search.actions import valid_move_check, move, explore
from search.util import print_move, print_boom, print_board
from search.goal_search import match_with_white

# Define the node Node(Node parent, state current_state)


class Node():
    def __init__(self, parent=None, state=None, stack=None, direction=None):

        # previous node
        self.parent = parent
        # state = board
        self.state = state
        # board.white().that particular stack
        self.stack = stack
        self.direction = direction

        # values to be calculated:
        # g value - distance from start node to current node
        self.g = 0
        # h value - distance from end node to current node
        self.h = 0
        # f value - g + h
        self.f = 0

        def __str__(self):
            return "parent:%s | state:%s" % (self.parent, self.state)

# initialize_start(Stack.coordinate start)


def initialize_start(start, white_stack):
    start_node = Node(None, start, white_stack, None)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    return start_node

# initialize_start(Stack.coordinate end)
# stack with 0 coordinates


def initialize_end(end, end_stack):

    # get end node stack

    end_node = Node(None, end, end_stack, None)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0
    return end_node

# convert coordinates to

# - expand node


def explore_neighbours(current_node, white_stack):

    neighbours_list = []

    current_stack = white_stack

    for direction in Directions:

        if not explore(current_node.state, current_stack, white_stack.number, 1, direction):
            continue

        node_state = explore(current_node.state, current_stack,
                             white_stack.number, 1, direction)
        
        print(node_state)

        # create neigbours node node
        neighbours_node = Node(current_node, node_state,
                               current_stack, direction)

        # add to neighbours array
        neighbours_list.append(neighbours_node)

    return neighbours_list

# find the distance between two nodes
# - get best node (the thing a* is based on) = heuristics


def heuristics(start_node, target_node):
    D = 1
    dx = abs(start_node.stack.coordinates[0] -
             target_node.stack.coordinates[0])
    dy = abs(start_node.stack.coordinates[1] -
             target_node.stack.coordinates[1])
    return D * (dx + dy)

# - a star search - the main search function, adapted from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2


def a_star_search(start, end, white_stack, end_stack):

    # Initialize the start and end node
    # star_node = board.white[coord]
    start_node = initialize_start(start, white_stack)
    end_node = initialize_end(end, white_stack)

    # Initialize open list = nodes that we've calculated the f value
    open_list = []
    # initialize closed list = nodes that has been evaluated
    closed_list = []

    curr_stack_list = []

    # add the first node to the open list
    open_list.append(start_node)
    curr_stack_list.append(white_stack)

    # open FUNCTION: while open list is not empty
    while len(open_list) > 0:

        # the current_node = node in open list with lowest f_value
        current_node = open_list[0]
        current_node_index = 0

        for i in range(len(open_list)):
            
            # make a sorting function comparing the open and closed list
            if open_list[i].f < current_node.f:
                current_node = open_list[i]
                current_node_index = i

        # remove current_node from open list
        open_list.remove(current_node)
        # add current_node to closed list
        closed_list.append(current_node)

        # convert the paths from coordinates to Stacks.
        # if current_node reached the goal_node
        if goal_test(current_node, end_node):
            # return
            path = []
            state_path = []
            path_node = current_node

            # current_node = end_node
            while path_node is not None:
                # change the format to board dict now
                path.append(path_node)
                state_path.append(path_node.state)
                path_node = path_node.parent
            # return path
            # print(state_path[::-1])
            # path = [Stack1, Stack2, Stack3]
            return path[::-1]

        # # generate neighbouring nodes

        neighbours_list = []

        #iterate how many piececs to move
        for no_pieces in range(len(current_node.stack.pieces)):
            
            #iterate direction for specified stack (group of pieces) to move
            for direction in Directions:

                #iterate number of spaces to move in that direction
                for spaces in range(len(current_node.stack.pieces)):

                    #current_stack = curr_stack_list[-1]
                
                    new_state = current_node.state.get_copy()
                    new_stack = new_state.white[current_node.stack.coordinates]

                    stack = move(new_state, new_stack, no_pieces+1, spaces+1, direction)
                    if not stack:
                        continue
                    
                    print_board(new_state.get_board_dict())
                    #if not explore(current_node.state, current_stack, current_stack.number, 1, direction):
                    #    continue

                    #node_state = explore(
                    #    current_node.state, current_stack, current_stack.number, 1, direction)

                    # create neigbours node node
                    neighbour_node = Node(current_node, new_state, stack, direction)

                    # update the current stack

                    # add to neighbours array
                    neighbours_list.append(neighbour_node)

        for neighbour_node in neighbours_list:

            # check if node is explored and if not just skip
            if expanded_previously(closed_list, neighbour_node):
                continue

            # calculate f value of current path
            neighbour_path_cost = current_node.g + \
                heuristics(current_node, neighbour_node)

            # - goal test
            # check if the new path is shorter or neighbour is not included in open list yet
            if (neighbour_path_cost < current_node.g) or (neighbour_node not in open_list):
                neighbour_node.g = neighbour_path_cost
                neighbour_node.h = heuristics(
                    neighbour_node, end_node)
                neighbour_node.f = neighbour_node.g + neighbour_node.h
                
                #current_stack = get_current_stack(neighbour_node.state)
                #curr_stack_list.append(current_stack)
                
                
                # if node is already in open list, dont add it in
                for open_node in open_list:
                    if neighbour_node.state == open_node.state:
                        continue

            # Add the child to the open list
            
            open_list.append(neighbour_node)


def a_star_main(board, end_boards, goal_pairs):
    total_paths = []

    # board = initial board
    # end_boards => end state for each
    # goal_pairs = {(white_stack) : end_board}

    white_dict = board.white
    for i, end_board in enumerate(end_boards):
        new_white_dict = end_board.white
        for coordinate, white_stack in white_dict.items():
            for end_coord, end_stack in new_white_dict.items():
                # end_boards[i] = final boards
                if goal_pairs[coordinate] == end_coord:
                    if i == 0:
                        total_paths.append(a_star_search(
                            board, end_boards[i], white_dict[coordinate], new_white_dict[end_coord]))
                    total_paths.append(a_star_search(
                        end_boards[i-1], end_boards[i], white_dict[coordinate], new_white_dict[end_coord]))
    print(total_paths)
    return total_paths

# get current stack by comparing the old state and the new state


def get_current_stack(new_state):
    coord = list(new_state.white.keys())[-1]
    return new_state.white[coord]
    

# Node -> state (board) -> white_stack = board.get_white()
# -> iterate ->  white_stack[goal_tile] = Stack(PIECES, white) (match coordinate with goal coordinate)
# def get_white_piece(board, goal_tile_list, goal_pairs):
#     # get board state
#     white_dict = board.white

#     for coordinate, stack in white_dict.items():
#         for goal_tile in goal_tile_list:

def expanded_previously(closed_list, node):
    node_white_coordinates = sorted(list(node.state.white.keys()), key=itemgetter(0))
    for closed_node in closed_list:
        closed_node_white_coordinates = sorted(list(closed_node.state.white.keys()), key=itemgetter(0))
        if node_white_coordinates == closed_node_white_coordinates:
            return True

    return False

def goal_test(node, end_node):
    node_white_coordinates = sorted(list(node.state.white.keys()), key=itemgetter(0))
    end_node_white_coordinates = sorted(list(end_node.state.white.keys()), key=itemgetter(0))
    if node_white_coordinates == end_node_white_coordinates:
        return True
    else:
        return False