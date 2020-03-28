
# Define the node
class Node():
    def __init__(self, parent=None, state=None):

        # previous node
        self.parent = parent
        # state = [number of tokens in a stack, position x, position y]
        self.state = state

        # values to be calculated:

        # g value - distance from start node to current node
        self.g = 0
        # h value - distance from end node to current node
        self.h = 0
        # f value - g + h
        self.f = 0

        def __str__(self):
            return "parent:%s | state:%s" % (self.parent, self.state)

# - intiialize tree
def initialize_start(start):
    start_node = Node(None, start)
    start_node.g = 0
    start_node.h = 0
    start_node.f = 0
    return start_node


def initialize_end(end):
    end_node = Node(None, end)
    end_node.g = 0
    end_node.h = 0
    end_node.f = 0
    return end_node

# - expand node
def explore_neighbours(current_node):
    # neighbour node data structure =

    neighbours_list = []
    # to be updated depending on the number of tokens in the stack
    adjacent_neighbours = [[0, 1], [0, -1], [-1, 0], [1, 0]]

    for i in range(len(adjacent_neighbours)):
        # get current state
        node_state = [0, current_node.state[1] + adjacent_neighbours[i][0],
                      current_node.state[2] + adjacent_neighbours[i][1]]

        # move validity check
        # if out of bounds
        if node_state[1] < 0 or node_state[2] < 0:
            continue
        # range check

        # create neigbours node node
        neighbours_node = Node(current_node, node_state)

        # add to neighbours array
        neighbours_list.append(neighbours_node)

    return neighbours_list

# find the distance between two nodes
# - get best node (the thing a* is based on) = heuristics
def heuristics(start_node, target_node):
    D = 5
    dx = abs(start_node.state[1] - target_node.state[1])
    dy = abs(start_node.state[2] - target_node.state[2])
    return D * (dx + dy)

# - a star search - the main search function, adapted from: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
def a_star_search(start, end):

    # Initialize the start and end node
    start_node = initialize_start(start)
    end_node = initialize_end(end)

    # Initialize open list = nodes that we've calculated the f value
    open_list = []
    # initialize closed list = nodes that has been evaluated
    closed_list = []

    # add the first node to the open list
    open_list.append(start_node)

    # open FUNCTION: while open list is not empty
    while len(open_list) > 0:

        # the current_node = node in open list with lowest f_value
        current_node = open_list[0]
        current_node_index = 0

        for i in range(len(open_list)):

            # make a sorting function comparing the open and closed list
            if open_list[i].f < current_node.f:
                current_node == open_list[i]
                current_node_index = i

                # remove current_node from open list
        open_list.remove(current_node)
        # add current_node to closed list
        closed_list.append(current_node)
        # if current_node reached the goal_node
        if current_node.state[1:] == end_node.state[1:]:
            # return
            path = []
            state_path = []
            path_node = current_node
            # current_node = end_node
            while path_node is not None:
                path.append(path_node)
                state_path.append(path_node.state)
                path_node = path_node.parent
            # return path
            print(state_path[::-1])
            return path[::-1]

        # # generate neighbouring nodes
        neighbours_list = explore_neighbours(current_node)

        for neighbour_node in neighbours_list:
            # check if node is explored and if not just skip
            for closed_node in closed_list:
                if neighbour_node.state[1:] == closed_node.state[1:]:
                    continue
            
            # calculate f value of current path
            neighbour_path_cost = current_node.g + \
                heuristics(current_node, neighbour_node)

            # - goal test
            # check if the new path is shorter or neighbour is not included in open list yet
            if (neighbour_path_cost < current_node.g) or (neighbour_node not in open_list):
                neighbour_node.g = neighbour_path_cost
                neighbour_node.h = heuristics(neighbour_node, end_node)
                neighbour_node.f = neighbour_node.g + neighbour_node.h
                
                neighbour_node.parent = current_node

                # if node is already in open list, dont add it in
                for open_node in open_list:
                    if neighbour_node.state[1:] == open_node.state[1:]:
                        continue

            # Add the child to the open list
            open_list.append(neighbour_node)
        print(current_node.state)


a_star_search([0, 0, 1], [0, 5, 2])
