import re
from helpers.bsearch import bsearch
from collections import deque
from sortedcontainers import SortedSet
from itertools import chain
from functools import cmp_to_key

class PointLocator:
    def ceil_div(self, n):
        return (n >> 1) + (n & 1)

    def floor_div(self, n):
        return n >> 1


class PointLocator1(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.floor_div(-(-x1-y1-x2+y2+r1-r2)), self.ceil_div(-(-x1-y1+x2-y2+r1+r2)))

class PointLocator2(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.floor_div(-(-x1+y1-x2-y2+r1-r2)), self.floor_div((-x1+y1+x2+y2+r1+r2)))

class PointLocator3(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.ceil_div(-(-x1+y1-x2-y2+r1+r2)), self.ceil_div((-x1+y1+x2+y2+r1-r2)))

class PointLocator4(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.floor_div((x1+y1+x2-y2+r1+r2)), self.ceil_div((x1+y1-x2+y2+r1-r2)))

class PointLocator5(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.ceil_div((x1+y1+x2-y2+r1-r2)), self.floor_div((x1+y1-x2+y2+r1+r2)))

class PointLocator6(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.ceil_div((x1-y1+x2+y2+r1-r2)), self.ceil_div(-(x1-y1-x2-y2+r1+r2)))

class PointLocator7(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.floor_div((x1-y1+x2+y2+r1+r2)), self.floor_div(-(x1-y1-x2-y2+r1-r2)))

class PointLocator8(PointLocator):
    def __call__(self, x1, y1, r1, x2, y2, r2):
        return (self.ceil_div(-(-x1-y1-x2+y2+r1+r2)), self.floor_div(-(-x1-y1+x2-y2+r1-r2)))

class DiamondIntersectionFinder:
    LEFT = 0
    TOP = 2
    RIGHT = 4
    BOTTOM = 6

    def __init__(self):
        self.pointLocators = [PointLocator1(), PointLocator2(), PointLocator3(), PointLocator4(), PointLocator5(), PointLocator6(), PointLocator7(), PointLocator8()]

    def intersects(self, left, right):
        params = (left.x, left.y, left.r, right.x, right.y, right.r)
        corners = [
            left.left(),
            left.top(),
            left.right(),
            left.bottom()
        ]

        pts = deque()
        for corner, i in zip(corners, [self.LEFT, self.TOP, self.RIGHT, self.BOTTOM]):
            if corner not in left:
                continue
            p1 = self.pointLocators[i](*params)
            if p1 in left and p1 in right:
                pts.append(p1)
                p2 = self.pointLocators[i + 1](*params)
                if p2 in left and p2 in right:
                    pts.append(None)
                    pts.append(p2)
        if (pts[0] == pts[-1]):
            return (pts[0], pts[-1])
        if pts[0] in corners:
            pts.popleft()
        if pts[-1] in corners:
            pts.pop()
        while(pts[0] == None or pts[-1] == None):
            pts.rotate()
        return (pts[0], pts[-1])

class Diamond:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def distance(self, p):
        return abs(p[0] - self.x) + abs(p[1] - self.y)

    def __contains__(self, p):
        return self.distance(p) <= self.r

    def left(self):
        return (self.x - self.r, self.y)

    def top(self):
        return (self.x, self.y + self.r)

    def right(self):
        return (self.x + self.r, self.y)

    def bottom(self):
        return (self.x, self.y - self.r)

    def corners(self):
        yield self.left()
        yield self.top()
        yield self.right()
        yield self.bottom()

    def loc(self):
        return (self.x, self.y)

class PerimeterPointToIntConverter:
    def __init__ (self, diamond):
        self.diamond = diamond

    def __call__(self, p):
        x, y = p
        if y >= self.diamond.y:
            if x <= self.diamond.x:
                return y - self.diamond.y
            else:
                return self.diamond.r + x - self.diamond.x
        else:
            if y >= self.diamond.y:
                return 2 * self.diamond.r + self.diamond.y - y
            else:
                return 3 * self.diamond.r + self.diamond.x - x

    def back(self, n):
        if n >= (rx3 := 3 * self.diamond.r):
            return (rx3 + self.diamond.x - n, n - 4 * self.diamond.r + self.diamond.y)
        elif n > (rx2 := 2 * self.diamond.r):
            return (rx3 + self.diamond.x - n, rx2 + self.diamond.y - n)
        elif n > (r := self.diamond.r):
            return (self.diamond.x + n - r, self.diamond.y + rx2 - n)
        else:
            return (self.diamond.x + n - r, self.diamond.y + n)


class PerimeteredDiamond(Diamond):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.overlappers = set()
        self.converter = PerimeterPointToIntConverter(self)
        self.by_start = cmp_to_key(lambda t, i: t[0] - i)
        self.by_stop = cmp_to_key(lambda t, i: t[1] - i)
        self.perimeter = [(0, 4 * r - 1)]

    def overlaps(self, other):
        return self.distance(other.loc()) <= self.r + other.r

    def add_overlappers(self, sensor_iter):
        for sensor in sensor_iter:
            if self.overlaps(sensor):
                self.overlappers.add(sensor)
                sensor.overlappers.add(self)

    def constrain_perimeter(self, min, max):
        minx, miny = min
        maxx, maxy = max
        if (diff := minx - self.left()[0]) >= 0:
            self.remove_from_perimeter((minx, self.y - diff), (minx, self.y + diff))
        if (diff := self.right()[0] - maxx) >= 0:
            self.remove_from_perimeter((maxx, self.y + diff), (maxx, self.y - diff))
        if (diff := miny - self.bottom()[1]) >= 0:
            self.remove_from_perimeter((self.x + diff, miny), (self.x - diff, miny))
        if (diff := self.top()[1] - maxy) >= 0:
            self.remove_from_perimeter((self.x - diff, maxy), (self.x + diff, maxy))

    def remove_from_perimeter(self, interval):
        start, stop = tuple(map(self.converter, interval))

        if stop < start:
            if (i := bsearch(self.perimeter, start, key=self.by_stop)) < 0:
                i = ~i

            if i < len(self.perimeter) and self.perimeter[i][0] < start:
                self.perimeter[i] = (self.perimeter[i][0], start - 1)
                i += 1

            while i < len(self.perimeter):
                self.perimeter.pop()

            if (i := bsearch(self.perimeter, stop, key=self.by_start)) < 0:
            i = ~i - 1

            if 0 <= i and stop < self.perimeter[i][1]:
                self.perimeter[i] = (stop + 1, self.perimeter[i][1])
                i -= 1

            while 0 <= i:
                self.perimeter.pop(i)
                i -= 1

        else:
            if (i := bsearch(self.perimeter, start, self.by_stop)) < 0:
                i = ~i
            if (j := bsearch(self.perimeter, stop, self.by_start)) < 0:
                j = ~j - 1

            if i == j:
                old = self.perimeter.pop(i)
                left = (old[0], start - 1)
                right = (stop + 1, old[1])
                if right[0] <= right[1]:
                    self.perimeter.insert(i, right)
                if left[0] <= left[1]:
                    self.perimeter.insert(i, left)
            else:
                if self.perimeter[i][0] < start:
                    self.perimeter[i] = (self.perimeter[i][0], start - 1)
                    i += 1
                if stop < self.perimeter[j][1]:
                    self.perimeter[j] = (stop + 1, self.perimeter[j][1])
                    j -= 1
                for k in range(j, i - 1, -1):
                    self.perimeter.pop(k)

    def __repr__(self):
        return f'{type(self).__name__}(x={self.x}, y={self.y}, r={self.r})'

class DiamondFactory:
    def __init__(self, diamond_class):
        self.diamond_class = diamond_class

    def create(self, sensor_loc, beacon_loc):
        r = abs(beacon_loc[0] - sensor_loc[0]) + abs(beacon_loc[1] - sensor_loc[1])
        return self.diamond_class(sensor_loc[0], sensor_loc[1], r)

class DiamondBorderFactory:
    def __init__(self, diamond_class):
        self.diamond_class = diamond_class

    def create(self, sensor_loc, beacon_loc):
        r = abs(beacon_loc[0] - sensor_loc[0]) + abs(beacon_loc[1] - sensor_loc[1]) + 1 # + 1 so that the edges of the diamond are the border
        return self.diamond_class(sensor_loc[0], sensor_loc[1], r)

class DiamondLookup:
    def __init__(self):
        self.setx = SortedSet(key=lambda p: p[0])
        self.sety = SortedSet(key=lambda p: p[1])
        self.point_to_diamond = dict()

    def add(self, diamond):
        for corner in diamond.corners():
            self.setx.add(corner)
            self.sety.add(corner)
            self._map(corner, diamond)

    def nearby(self, diamond):
        points = self.setx.irange(diamond.left(), diamond.right())
        points = self.sety.intersection(points).irange(diamond.bottom(), diamond.top())
        return set(chain.from_iterable(map(lambda p: self.point_to_diamond[p])))

    def _map(self, point, diamond):
        if point not in self.point_to_diamond:
            self.point_to_diamond[point] = []
        self.point_to_diamond[point].append(diamond)

def read_input():
    with open('input.txt', 'r') as f:
        diamond_factory = DiamondFactory(Diamond)
        border_factory = DiamondBorderFactory(PerimeteredDiamond)

        diamonds = []
        lookup = DiamondLookup()

        for line in map(lambda l: l.strip(), f):
            m = re.search(r"Sensor at x=([+-]?\d+), y=([+-]?\d+): closest beacon is at x=([+-]?\d+), y=([+-]?\d+)", line)
            sx, sy, bx, by = m.groups()
            diamonds.append(border_factory.create((sx, sy), (bx, by)))
            lookup.add(diamond_factory.create((sx, sy), (bx, by)))
        return diamonds, lookup

# sensors, _ = read_input()

# for i, sensor in enumerate(sensors):
#     sensor.add_overlappers(sensors[0:i])

# pass

# for s in sensors:
#     print (s.desmos_repr())
