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
from game import Directions
from typing import List
from util import Stack, Queue, PriorityQueue, PriorityQueueWithFunction

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

def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState()) -- returns coordinates (x, y)
    print("Is the start a goal?", problem.isGoalState(problem.getStartState())) -- returns True/False
    print("Start's successors:", problem.getSuccessors(problem.getStartState())) -- returns list of tuples
    (successor, action, stepCost)
    """
    "*** YOUR CODE HERE ***"
    stack = Stack()
    visited = set()

    stack.push((problem.getStartState(), []))
    while not stack.isEmpty():
        location, path = stack.pop()

        if problem.isGoalState(location):
            return path

        if location not in visited:
            visited.add(location)

            for successor, action, _ in problem.getSuccessors(location):
                if successor not in visited:
                    new_path = path + [action]
                    stack.push((successor, new_path))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = Queue()
    visited = set()

    queue.push((problem.getStartState(), []))
    while not queue.isEmpty():
        location, path = queue.pop()

        if problem.isGoalState(location):
            return path

        if location not in visited:
            visited.add(location)

            for successor, action, _ in problem.getSuccessors(location):
                if successor not in visited:
                    new_path = path + [action]
                    queue.push((successor, new_path))

    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pqueue = PriorityQueue()
    visited_costs = {} # maps location to cost

    pqueue.push((problem.getStartState(), [], 0), 0) # (location, path, cost), priority
    while not pqueue.isEmpty():
        location, path, cost = pqueue.pop()

        if problem.isGoalState(location):
            return path

        if location not in visited_costs or visited_costs[location] > cost:
            visited_costs[location] = cost

            for successor, action, step_cost in problem.getSuccessors(location):
                new_cost = cost + step_cost
                new_path = path + [action]
                pqueue.update((successor, new_path, new_cost), new_cost)

    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def priorityFunction(node):
        location, path, cost = node
        return cost + heuristic(location, problem)

    hqueue = PriorityQueueWithFunction(priorityFunction)
    visited_costs = {} # maps location to cost

    hqueue.push((problem.getStartState(), [], 0)) # (location, path, cost)
    while not hqueue.isEmpty():
        location, path, cost = hqueue.pop()

        if problem.isGoalState(location):
            return path

        if location not in visited_costs or visited_costs[location] > cost:
            visited_costs[location] = cost

            for successor, action, step_cost in problem.getSuccessors(location):
                new_cost = cost + step_cost
                new_path = path + [action]
                hqueue.push((successor, new_path, new_cost))

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
