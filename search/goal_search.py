
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
            if (x == 1 and y == 1) or (check_coord in coordinates):
                continue
            black_coordinates.append(check_coord)

    return black_coordinates

# get all the black token and use the black range function


def get_all_black_ranges(board):

    black_ranges_dict = {}  # store {(x,y):[(a,b),(e,f)]}
    coordinates = list(board.black.values())

    for coordinate in coordinates:
        black_stacks = get_black_range(board, coordinate)
        black_ranges_dict[coordinate.coordinates] = black_stacks

    # return a dictionary of {(x,y): [(a,b),(c,d),(e,f)]}
    # {(1,1), [(0,1),(0,2)]}
    return black_ranges_dict

# check for adjacent pieces for chain explosions


def check_chaining(board):
    black_ranges = get_all_black_ranges(board)
    # black_ranges = {(x,y): [(a,b),(c,d),(e,f)]}
    blacks = list(black_ranges.keys())
    # blacks = list(board.black.keys())
    black_ranges_list = list(black_ranges.values())

    # # new_black_ranges = []
    for i in range(len(blacks)):
        print("{" + str(blacks[i]) + ": " +
              str(black_ranges[blacks[i]]) + "}" + "\n")
    # blacks = [(x,y), (z,a)] a list of black coordinates
    for i in range(len(blacks)):
        # print("{" + str(blacks[i]) + ": " + str(black_ranges_list[i])+ "}")
        for j in range(len(black_ranges_list)):
            # print(blacks[i])

            if blacks[i] in black_ranges_list[j]:
                black_ranges[blacks[j]] = list(
                    set(black_ranges[blacks[i]] + black_ranges_list[j]).difference(set([blacks[j]])))
                print("old:	" + str(blacks[j]) + "	| " + str(black_ranges_list[j]) + "\n" + "new:	" + str(
                    blacks[i]) + "	| " + str(black_ranges[blacks[i]]) + "\n" + "	{" + str(blacks[j]) + " : " +
                    str(black_ranges[blacks[j]]) + "}" + "\n")
                # black_ranges[blacks[i]] = [0]
                # delete black_range
    print(black_ranges)
    print("\n")
    return black_ranges

# get the intersecting black ranges


def get_intersections(board):
    intersection_list = []
    a_list = []
    black_ranges_dict = check_chaining(board)

    blacks = list(black_ranges_dict.keys())
    # blacks = list(board.black.keys())
    black_ranges_list = list(black_ranges_dict.values())

    # turn dictionary into a pair of list
    black_ranges = list(black_ranges_dict.items())
    print(black_ranges)
    print("\n")

    for i in range(len(black_ranges)):
        current = set(black_ranges[i][1])

        print("current i:" + str(black_ranges[i][0]))

        for j in range(len(black_ranges)):
            print("current j:" + str(black_ranges[j][1]))

            # add all intersections to a list
            if len(list(set(black_ranges[i][1]).intersection(set(black_ranges[j][1])))) != 0:

                current = set(black_ranges[i][1]).intersection(
                    black_ranges[j][1])
                intersection_class = Cluster(
                    [black_ranges[i][0], black_ranges[j][0]], list(current))
                intersection_list.append(intersection_class)
                a_list.append([black_ranges[i][0], black_ranges[j][0]])

            # if no intersection found, add one coordinate as a intersection anyways
            if (j+1 == len(black_ranges)) and (current == set(black_ranges[i][1])):
                print("CURR NO: " + str(black_ranges[i][0]))
                intersection_class = Cluster(
                    [black_ranges[i][0]], list(current))
                intersection_list.append(intersection_class)
                a_list.append(black_ranges[i][0])

        if (i+2 == len(black_ranges)) and (current == set(black_ranges[i][1])):
            print("CURR NOss: " + str(black_ranges[i+1][0]))
            intersection_class = Cluster(
                [black_ranges[i+1][0]], list(current))
            intersection_list.append(intersection_class)
            a_list.append(black_ranges[i+1][0])

    print(a_list)  # [Cluster1, Cluster2, Cluster3]
    return intersection_list  # [Cluster1, Cluster2, Cluster3]


def get_cluster(board):

    # Get list of clusters Cluster(black_coordinates, [intersections])
    intersection_list = get_intersections(board)

    cluster_dict = {}

    print(len(intersection_list))
    # cluster_dict = {cluster.coordinate : cluster.intersection}

    for i in range(len(intersection_list)):
        print("BOYYY" + str(i) + " : " + str(intersection_list[i].coordinates))
    # determine all the clusters aka goal tile
    print("\n")
    for i in range(len(intersection_list)):

        current = set(intersection_list[i].coordinates)
        current_inter = set(intersection_list[i].intersection)
        print("hello" + str(i) + " : " + str(intersection_list[i].coordinates))

        for j in range(len(intersection_list)):

            print("hellos" + str(j) + " : " +
                  str(intersection_list[j].coordinates) +  str(intersection_list[j].intersection))
            print(len(board.white))

            # if there's only one cluster
            if len(current.union(set(intersection_list[j].coordinates))) == len(list(board.black)):

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
                # print("inter" + str(current_inter))

            if j+1 == len(intersection_list):
                cluster_dict[tuple(current)] = list(current_inter)

        if i+2 == len(intersection_list):
            cluster_dict[tuple(current)] = list(current_inter)
            
    # print(cluster_dict)
    if len(cluster_dict) == len(board.white):
        return cluster_dict
    else:
        return False

#  get the goal tile


def get_goal_tile(cluster_dict):

    goal_tile_list=[]

    cluster_list=list(cluster_dict.values())

	# edit this
    for cluster in cluster_list:
        # just get the first intersection in list
        goal_tile_list.append(cluster[0])

        # TODO: assuming something didnt work, check range later?

    return goal_tile_list

def match_with_white(goal_tiles, board):

    white_stacks=board.white

    for i, goal_tile in enumerate(goal_tiles):
        white_stacks[i]
