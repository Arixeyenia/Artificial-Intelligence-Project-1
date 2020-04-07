

# Combining the best of both worlds of DFS and BFS
# Time O(b^d)
# Space = Linear O(n)


class Node():
    def __init__(self, parent=None, state=None, stack=None, direction=None):

        # previous node
        self.parent = parent
        # state = board
        self.state = state
        # board.white().that particular stack
        self.stack = stack
        
        self.direction = direction
                
        # self.actions = []
        # self.path_cost = 0
        # self.expand = []

        def __str__(self):
            return "parent:%s | state:%s" % (self.parent, self.state)

# Problem:
	# state = state of the board
	# actions = moving the white tiles towards the goal
	# path cost = each state generated
	# goal test = given goal state / search by yourself

# Keep searching the nodes until you find the ultimate state

#  Adapted from: https://github.com/aimacode/aima-python/blob/master/search.py
def iterative_deepening_search(start_state, goal_state):
    return "IDF"


# Will be used inside iterative deepening search.
# Recursively increase the max depth to be search before finding the node
def depth_limited_search(start_state, goal_state, limit):
    
    # if start state == goal state, return true
    if start_state == goal_state:
        return True
    elif limit == 0:
        return False
    # else:
        
        # for all the kids in the node
			# recursively do this again
			# if child == 'cutoff'
				# cutoff_occured = True
			# elif result not None
			# return result
   
    
    # Actions
    
    
    # Expand: expand the possible child nodes
    
    
    return "Depth limited search"

