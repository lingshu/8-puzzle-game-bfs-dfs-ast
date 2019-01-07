from collections import deque
import sys
import time
import resource

class Solver(object):
    def __init__(self, initNode, searchType):
        self.initNode = initNode
        self.searchType = searchType
        if searchType == 'bfs':
            self.frontier = deque([initNode])
        elif searchType == 'dfs':
            self.frontier = deque([initNode])
        elif searchType == 'ast':
            self.frontier = [(initNode.h, initNode)]
        self.expandedSet = set([initNode.state])
        self.goal = '0,1,2,3,4,5,6,7,8'
        self.path_to_goal = []
        self.goalFound = False
        self.nodes_expanded = 0
        self.max_search_depth = 0
        self.start_time = 0
        self.end_time = 0
        self.max_ram_usage = 0


    def exchange(self, board, n_bi, new_bi):
        new_board = board[:]
        new_board[n_bi] = board[new_bi]
        new_board[new_bi] = '0'
        return new_board


    def heuristic(self, node):
        for i in range(len(node.board)):
            X = abs(i // 3 - node.board.index(str(i))// 3)
            Y = abs(i % 3 - node.board.index(str(i))% 3)
            d = X + Y
            node.h = d + node.h
        node.h = node.h + node.depth
        return node


    def run(self):
        self.start_time = time.time()
        while len(self.frontier) > 0:
            if self.searchType == 'bfs':
                node = self.frontier.popleft()

            elif self.searchType == 'dfs':
                node = self.frontier.pop()

            else:
                node = self.frontier.pop(0)[1]

            self.goal_test(node)
            if self.goalFound:
                return

        return print('no solution')

    def goal_test(self, node):
        if node.state == self.goal:
            self.goalFound = True
            self.end_time = time.time()
            return self.success(node)
        else:
            self.nodes_expanded += 1
            return self.exNodes(node)


    def exNodes(self, node):
        n_b = node.board
        n_bi = node.board.index('0')

        if self.searchType == 'bfs' or self.searchType == 'ast':
            if n_bi - 3 >= 0:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi - 3), node, 'Up'))
            if n_bi + 3 <= 8:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi + 3), node, 'Down'))
            if n_bi % 3 - 1 >= 0:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi - 1), node, 'Left'))
            if n_bi % 3 + 1 < 3:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi + 1), node, 'Right'))

        else:
            if n_bi % 3 + 1 < 3:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi + 1), node, 'Right'))
            if n_bi % 3 - 1 >= 0:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi - 1), node, 'Left'))
            if n_bi + 3 <= 8:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi + 3), node, 'Down'))
            if n_bi - 3 >= 0:
                self.addNode(Node(self.exchange(n_b, n_bi, n_bi - 3), node, 'Up'))

    def addNode(self, newNode):
        if newNode.state not in self.expandedSet:
            self.expandedSet.add(newNode.state)
            if self.searchType == 'bfs'or searchType == 'dfs':
                self.frontier.append(newNode)
                self.max_search_depth = max(newNode.depth, self.max_search_depth)
            else:
                self.max_search_depth = max(newNode.depth, self.max_search_depth)
                newNode = self.heuristic(newNode)
                self.frontier.append((newNode.h, newNode))

                self.frontier.sort(key=lambda tup: tup[0])


    def success(self, node):
        successfulPath = self.getPath(node)
        print('path_to_goal:', successfulPath)
        print('cost_of_path:', len(successfulPath))
        print('nodes_expanded:', self.nodes_expanded)
        print('search_depth:', node.depth)
        print('max_search_depth:', self.max_search_depth)
        print('running_time:', self.end_time - self.start_time)
        self.max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024 / 1024
        print('max_ram_usage:', self.max_ram_usage)


    def getPath(self, node):
        while node.parent:
            self.path_to_goal.append(node.action)
            node = node.parent
        self.path_to_goal.reverse()
        return self.path_to_goal




class Node(object):
    def __init__(self, board, parentNode, action):
        self.state = ','.join(board)
        self.board = board
        self.h = 0

        if parentNode == False:
            self.parent = False
            self.depth = 0
            self.action = ''
        else:
            self.parent = parentNode
            self.depth = parentNode.depth + 1
            self.action = action

    def __str__(self):
        return self.state



if len(sys.argv) != 3:
    sys.stderr.write('Error: must have 3 command arguments"\n')
    sys.exit()

if sys.argv[1] not in ['bfs', 'dfs', 'ast']:
    sys.stderr.write('Error: <method> argument must be "bfs", "dfs", "ast"\n')
    sys.exit()

input_board = sys.argv[2].split(',')


if len(input_board) != 9:
    sys.stderr.write('Error: input board must be 0 to 8 numbers')
    sys.exit()

ordered_board = sorted(map(int, input_board))
for i, element in enumerate(ordered_board):
    if element != i:
        sys.stderr.write('Error: input board must contain all 0 to 8 numbers')
        sys.exit()

searchType = sys.argv[1]
initNode = Node(input_board, False, '')
mySolver = Solver(initNode, searchType)
mySolver.run()