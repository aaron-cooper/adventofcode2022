#from helpers import MultiIndexSet
from helpers.MultiIndexSet import MultiIndexSet

class Node:
    def __init__(self, elevation):
        self.neighbours = set()
        self.elevation = elevation

    def try_add_neighbour(self, node):
        if self.elevation - node.elevation <= 1:
            self.neighbours.add(node)

neighbour_ind_offsets = [
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0)
]

class BoundChecker:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def __call__(self, i, j):
        return 0 <= i and i < self.rows and 0 <= j and j < self.cols

def dijkstra(graph, start):
    to_visit = MultiIndexSet()
    to_visit.add_index(lambda n: n.dist, 'distance')
    for n in graph:
        n.dist = 10000 # not infinity, close enough for our purposes
        n.prev = None
        to_visit.add(n)
    to_visit.remove(start)
    start.dist = 0
    to_visit.add(start)

    while len(to_visit):
        curr = to_visit.pop_min('distance')
        for n in curr.neighbours:
            if n not in to_visit:
                continue
            if curr.dist + 1 < n.dist:
                to_visit.remove(n)
                n.dist = curr.dist + 1
                n.prev = curr
                to_visit.add(n)


stoi = dict([(chr(97 + i), i) for i in range(26)])
stoi['S'] = 0
stoi['E'] = 25




grid = []
graph = set()
with open ('input.txt', 'r') as file:
    for line in file:
        grid.append([])
        for c in line.strip():
            n = Node(stoi[c])
            grid[len(grid) - 1].append(n)
            graph.add(n)
            if c == 'S':
                start = n
            elif c == 'E':
                end = n

rows = len(grid)
cols = len(grid[0])
checker = BoundChecker(rows, cols)

for i in range(rows):
    for j in range(cols):
        for x, y in neighbour_ind_offsets:
            (x, y) = (x + i, y + j)
            if checker(x, y):
                grid[i][j].try_add_neighbour(grid[x][y])

dijkstra(graph, end)

m = 10000

for n in graph:
    if n.elevation == 0 and n.dist < m:
        m = n.dist

print (m)

