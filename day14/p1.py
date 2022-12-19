from itertools import chain
from helpers.tupletools import tuple_range, tuple_add
from helpers.bounds import BoundsChecker

EMPTY=0
ROCK=1
SAND=2

class SandTracer:
    def __init__(self, cave):
        self.cave = cave
        self.check = BoundsChecker((1, 0), (len(cave) - 2, len(cave[0]) - 2))
        pass

    def seed(self, start):
        (self.x, self.y) = start
        while self.__fall_one():
            pass
        return (self.x, self.y) if self.check((self.x, self.y)) else None

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

class SeedGrower:
    def __init__(self, cave):
        self.sands = 0
        self.cave = cave

    def grow(self, seed):
        x, y = seed
        startlx, startly = seed
        startrx, startry = tuple_add(seed, (1, 0))
        while self.add_diagonal((startlx, y), (x, startly)):
            startlx -= 1
            startly -= 1
            if not self.add_diagonal((startrx, y), (x, startry)):
                return
            startrx += 1
            startry -= 1

    def add_diagonal(self, start, stop):
        x, y = start
        if self.cave[x][y + 1] == EMPTY:
            return False
        for x, y in tuple_range(start, stop):
            if self.cave[x][y] != EMPTY:
                return False
        for x, y in tuple_range(start, stop):
            self.sands += 1
            self.cave[x][y] = SAND
        return True



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
tracer = SandTracer(cave)
grower = SeedGrower(cave)
while seed := tracer.seed(start):
    grower.grow(seed)

for y in range(rows + 1):
    for x in range(cols + 2):
        print(c[cave[x][y]], end='')
    print()

print(grower.sands)
