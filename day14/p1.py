from itertools import chain
from helpers.tupletools import tuple_range, tuple_add
from helpers.bounds import BoundsChecker

EMPTY=0
ROCK=1
SAND=2

class SandFall:
    def __init__(self, cave):
        self.cave = cave
        self.check = BoundsChecker((1, 0), (len(cave) - 2, len(cave[0]) - 1))
        pass

    def fall(self, start):
        (self.x, self.y) = start
        while self.__fall_one():
            pass
        return self.check((self.x, self.y))

    def __fall_one(self):
        if cave[self.x][self.y + 1] == EMPTY:
            self.y += 1
        elif cave[self.x - 1][self.y + 1] == EMPTY:
            self.x -= 1
            self.y += 1
        elif cave[self.x + 1][self.y + 1] == EMPTY:
            self.x += 1
            self.y += 1
        else:
            return False
        return self.check((self.x, self.y))



c = {EMPTY: '.', ROCK: '#', SAND: 'O'}

paths = []
with open('input.txt') as f:
    while line := f.readline().strip():
        path = [p for p in line.split(' -> ')]
        path = [p.split(',') for p in path]
        path = [(int(p[0]), int(p[1])) for p in path]
        paths.append(path)

maxx = maxy = 0
minx = 100000 
miny = 0
for x, y in chain.from_iterable(paths):
    maxx = max(maxx, x)
    maxy = max(maxy, y)
    minx = min(minx, x)

rows = maxy - miny + 1
cols = maxx - minx + 1

transform = lambda t: tuple_add(t, (-minx + 1, 0))

cave = [[EMPTY for _ in range(rows + 1)] for _ in range(cols + 2)]

for path in paths: 
    for i in range(1, len(path)):
        for x, y in tuple_range(transform(path[i - 1]), transform(path[i])):
            cave[x][y] = ROCK

start = transform((500, 0))
fall = SandFall(cave)
sands = 0
while fall.fall(start):
    cave[fall.x][fall.y] = SAND
    sands += 1

for y in range(rows + 1):
    for x in range(cols + 2):
        print(c[cave[x][y]], end='')
    print()

print (sands)