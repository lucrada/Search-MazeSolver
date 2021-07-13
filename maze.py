class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return (len(self.frontier) == 0)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty!")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty!")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
    def __init__(self, filename):
        self.solutions = None

        with open(filename) as f:
            contents = f.read()

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.walls = []
        for i in  range(self.height):
            row = []
            for j in range(self.width):
                if contents[i][j] == 'A':
                    self.start = (i, j)
                    row.append(False)
                elif contents[i][j] == 'B':
                    self.goal = (i, j)
                    row.append(False)
                elif contents[i][j] == ' ':
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)

    def printMaze(self):
        solutions = self.solutions[1] if self.solutions is not None else None
        print()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif self.walls[i][j]:
                    print('█', end='')
                elif solutions is not None and (i, j) in solutions:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()

    def neighbours(self, state):
        row, col = state
        candidates = [
	    ("up", (row-1, col)),
	    ("right", (row, col+1)),
	    ("down", (row+1, col)),
	    ("left", (row, col-1))
	]
        results = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                results.append((action, (r, c)))
        return results

    def solve(self, printExploredStates = False):
        initial_node = Node(state = self.start, parent = None, action = None)
        frontier = StackFrontier()
        frontier.add(initial_node)
        self.explored_states = set()

        while True:
            if frontier.empty():
                raise Exception("No solution possible")
            node = frontier.remove()
            if node.state == self.goal:
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solutions = [actions, states]
                if printExploredStates:
                    print(f"\nExplored States: {len(self.explored_states)}")
                return
            self.explored_states.add(node.state)
            for action, state in self.neighbours(node.state):
                if state not in self.explored_states and not frontier.contains_state(state):
                    new_node = Node(state, node, action)
                    frontier.add(new_node)

import sys

if len(sys.argv) != 2:
    raise Exception("\n[!] Usage: python3 maze.py <filename>\n")

maze = Maze(sys.argv[1])
maze.printMaze()
maze.solve(True)
maze.printMaze()

