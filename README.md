# 8-puzzle-game-bfs-dfs-ast

# Introduction
The N-puzzle game consists of a board holding N = m^2 − 1 distinct movable tiles, plus one empty space. There is one tile for each number in the set {1, ..., m^2 − 1}. In this project, I represent the blank space with the number 0 and focus on the m = 3 case (8-puzzle). In this combinatorial search problem, the aim is to get from any initial board state to theconfiguration with all tiles arranged in ascending order ⟨0, 1,..., m^2 − 1⟩ -- this is the goal state. The search space is the set of all possible states reachable from the initial state. Each move consists of swapping the empty space with a component in one of the four directions {‘Up’, ‘Down’, ‘Left’, ‘Right’}. Give each move a cost of one. Thus, the total cost of a path will be equal to the number of moves made.

# Algorithm
Search begins by visiting the root node of the search tree, given by the initialstate. Three main events occur when visiting a node:

  -First, we remove a node from the frontier set.
  
  -Second, we check if this node matches the goal state.
  
  -If not, we then expand the node. To expand a node, we generate all of its immediate successorsand add them to the frontier, if they (i) are not yet already in the frontier, and (ii) have not beenvisited yet.
  
This describes the life cycle of a visit, and is the basic order of operations for search agents in this project—(1) remove, (2) check, and (3) expand.
