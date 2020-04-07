from collections import deque

from search.actions import explore
from search.game import Piece, Stack, Directions, Board
from search.util import print_board


class Node():
    def __init__(self, parent=None, state=None, stack=None, direction=None, path_cost=0):

        # previous node
        self.parent = parent
        # state = board
        self.state = state

        self.stack = stack

        self.direction = direction

        self.path_cost = 0

        def expand(self, stacks):
            explored_nodes = []
            for stack in stacks:
                for direction in Directions:
                    current_node = self.child_node(direction, stack)
                    explored_nodes.append(current_node)

                return explored_nodes

        def child_node(self, direction, stack):
            next_state = explore(self.state, stack, stack.number, 1, direction)
            next_node = Node(self, next_state, stack, direction, 0)
            return next_node

        def __str__(self):
            return "parent:%s | state:%s" % (self.parent, self.state)

        def __eq__(self, other):
            return isinstance(other, Node) and self.state == other.state


# Main BFS function to iterate all the tile


# BFS function to tend to the state of each tile
def bfs(start_state, goal_state, white_stacks, white_stack):

    initial_node = Node(None, start_state, white_stack, None)
    initial_node.path_cost = 0

    frontier = deque([initial_node])

    while frontier:
        # get the first node
        current_node = frontier.popleft()

        # Implement Goal test
        # make a better goal test
        if current_node.state == goal_state:
            path = []
            path_node = current_node

            while path_node is not None:

                path.append(path_node)
                path_node = path_node.parent
                
            print(path)
            return path[::-1]

        # frontier.extend(current_node.expand(current_node, white_stacks))
        print_board(current_node.state.get_board_dict())

    return None


def goal_test(current_state, goal_state):
    if current_state == goal_state:
        print(current_state)
        print("fsdfsdfsd: ",goal_state)
        # if its within range of exploding all the black ones
        return True
