
from search.game import Piece, Stack, Board, Directions, Cluster
from search.actions import move, valid_move_check, boom, remove_stack, range_check

# Get one black token and find its range

def get_black_range(board, stack):
    coordinates = stack.coordinates
    black_coordinates = []
    top_left = (coordinates[0] - 1, coordinates[1] + 1)

    for x in range(3):
        for y in range(3):
            check_coord = (top_left[0] + x, top_left[1] - y)
            if check_coord in board.get_board_dict():
                if (x == 1 and y == 1):
                    continue
                black_coordinates.append(check_coord)
    return black_coordinates

# get all the black token and use the black range function


def get_all_black_ranges(board):

    black_ranges_dict = {}  # store {(x,y):[(a,b),(e,f)]}
    coordinates = list(board.black.values())

    for coordinate in coordinates:
        black_stacks = get_black_range(board, coordinate)
        black_ranges_dict[coordinate] = black_stacks

    # return a dictionary of {(x,y): [(a,b),(c,d),(e,f)]}
    # {(1,1), [(0,1),(0,2)]}
    return black_ranges_dict

# check for adjacent pieces for chain explosions


def check_chaining(board):
    black_ranges = get_all_black_ranges(board)
    # black_ranges = {(x,y): [(a,b),(c,d),(e,f)]}
    blacks = list(board.black.keys())
    
    black_ranges_list = black_ranges.items()
    
    # blacks = [(x,y), (z,a)] a list of black coordinates
    for i in range(len(blacks)):
        for j in range(len(list(black_ranges.values()))):
            if set(blacks[i]).intersection(black_ranges_list[1][j]) != set():
                black_ranges[blacks[j]] = black_ranges_list[1][j].append(blacks[i])
                del black_ranges[blacks[i]]
                # delete black_range
    return black_ranges

# get the intersecting black ranges

def get_intersections(board):
    intersection_list = []
    black_ranges_dict = check_chaining(board)

    intersection_list = []

    # turn dictionary into a pair of list
    black_ranges = black_ranges_dict.items()

    for i in range(len(black_ranges)-1):
        current = set(black_ranges[i][1])

        for j in range(i, len(black_ranges)):

            # add all intersections to a list
            if(set(black_ranges[i][1]).intersection(black_ranges[j[1]]) == set()):
                current = set(black_ranges[i][1]).intersection(
                    black_ranges[j][1])
                cluster_class = Cluster(
                    [black_ranges[i][0], black_ranges[j][0]], list(current))
                intersection_list.append(cluster_class)

            # if no intersection found, add one coordinate as a intersection anyways
            if (j == len(black_ranges)) and (current == set(black_ranges[i][1])):
                intersection_class = Cluster(black_ranges[i][0], list(current))

        return intersection_list  # [Cluster1, Cluster2, Cluster3]


def get_cluster(board):

    # Get list of clusters Cluster(black_coordinates, [intersections])
    intersection_list = get_intersections(board)

    cluster_dict = {}
    # cluster_dict = {cluster.coordinate : cluster.intersection}

    # determine all the clusters aka goal tile
    for i in range(len(intersection_list) - 1):

        current = set(intersection_list[i].coordinates)
        current_inter = set(intersection_list[i].intersection)

        for j in range(i, len(intersection_list)):

            # if there's only one cluster
            if len(current.union(set(intersection_list[j].coordinates))) == len(board.white):

                current = current.union(set(intersection_list[j].coordinates))
                # cluster_coords = tuple(list(current.union(set(intersection_list[j].coordinates))))
                current_inter = current_inter.intersection(
                    set(intersection_list[j].intersection))

                cluster_dict[tuple(current)] = list(current_inter)

                return cluster_dict  # {()}

            if (current.intersection(set(intersection_list[j].coordinates)) != set()) and (current_inter.intersection(set(intersection_list[j].intersection)) != set()):

                # unionize the coordinates
                current = current.union(set(intersection_list[j].coordinates))

                # find the intersection from the intersections
                current_inter = current_inter.intersection(
                    set(intersection_list[j].intersection))

            if j == len(intersection_list):
                cluster_dict[tuple(current)] = list(current_inter)

    if len(cluster_dict) == len(board.white):
        return cluster_dict
    else:
        return False

#  get the goal tile


def get_goal_tile(cluster_dict):

    goal_tile_list = []

    cluster_list = list(cluster_dict.keys())

    for cluster in cluster_list:
        # just get the first intersection in list
        goal_tile_list.append(cluster[0])

        # TODO: assuming something didnt work, check range later?

    return goal_tile_list


def match_with_white(goal_tiles, board):

    white_stacks = board.white

    for i, goal_tile in enumerate(goal_tiles):
        white_stacks[i]