# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    """
    The state can be represented by the pair of the coordinates of the given position and the path it took to reach there. This can be pushed on stack while the node is encountered first and poppped one by one.

    The visitedNodes array will be used to avoid visiting the same state twice. It will maintain a list of all the nodes which have been visited.
    """
    visited = []
    path = []
    stack = util.Stack()
    start_state = problem.getStartState()
    stack.push((start_state,path))
    while not stack.isEmpty():
        curr_state, path = stack.pop()
        if curr_state not in visited:
            visited.append(curr_state)
            if problem.isGoalState(curr_state):
                return path
            for state, direction, cost in problem.getSuccessors(curr_state):
                stack.push((state, path+[direction]))
    return path
        

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
#  
#     startState = problem.getStartState()
#     queue.push((startState, path, visitedNodes))
#     while queue.isEmpty() == False:
#         currentState, path, visitedNodes = queue.pop()
#         
#         if currentState not in visitedNodes:
#             successors = problem.getSuccessors(currentState)
              # if problem.isGoalState(currentState):
#             return path
#             for sucessorNode, action, stepCost in successors :
#                 queue.push((sucessorNode, path + [action], visitedNodes + [sucessorNode]))
#     return []
    visited = []
    path = []
    queue = util.Queue()
    start_state = problem.getStartState()
    queue.push((start_state,path))
    while not queue.isEmpty():
        curr_state, path = queue.pop()
        if curr_state not in visited:
            visited.append(curr_state)
            if problem.isGoalState(curr_state):
                return path
            for state, direction, cost in problem.getSuccessors(curr_state):
                queue.push((state, path+[direction]))
    return path

def uniformCostSearch(problem):
#     """Search the node of least total cost first."""
    
#     """
#     PriorityQueue will be added state and the path cost required to reach that state (0 for startState).
#     """
    visited = list()
    path =list()
    start_state = problem.getStartState()
    pq = util.PriorityQueue()
    pq.push((start_state,path),0)
    
    while not pq.isEmpty() :
            best_cost_state,directions_from_start= pq.pop()
                        
            if problem.isGoalState(best_cost_state):
                    return directions_from_start
					
            if best_cost_state not in visited :
                visited.append(best_cost_state)
                for successor,parent_sucessor_dist,stepCost in problem.getSuccessors(best_cost_state):
                	    updated_directions = directions_from_start + [parent_sucessor_dist]
                	    cost_of_reaching =  problem.getCostOfActions(updated_directions)
                	    pq.push((successor, updated_directions ) , cost_of_reaching)
    
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    """
    PriorityQueue will be states according to the evaulation function using path cost and manhattan distance cost required to reach that state (0 + manhattan distance for start state). Rets all similar to ucs
    """

    start_state = problem.getStartState()
    visited= list()
    pq =util.PriorityQueue()
    pq.push((start_state,list(),0),0)
    best_cost_state,directions,tot_cost= pq.pop()
    visited.append((start_state,0))
	
    while (not problem.isGoalState(best_cost_state)) :
			for successor,parent_sucessor_dir,stepCost in problem.getSuccessors(best_cost_state):
				new_directions = directions + [parent_sucessor_dir]
				cost_total = problem.getCostOfActions(new_directions)
				flag = False
				
				for i in range(len(visited)):
				  temp_state,temp_cost=visited[i] #checks if node is at same position of successor
				  if (successor==temp_state) and (cost_total>=temp_cost):
					flag=True
				if (not flag):
				  cost_total=problem.getCostOfActions(directions+[parent_sucessor_dir])
				  pq.push((successor,directions+[parent_sucessor_dir],cost_total),cost_total+heuristic(successor,problem))
				  visited.append((successor,cost_total))
			best_cost_state,directions,tot_cost=pq.pop()
    return  directions

# Abbreviations


bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
