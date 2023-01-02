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
    pointLocators = [
        PointLocator1(),
        PointLocator2(),
        PointLocator3(),
        PointLocator4(),
        PointLocator5(),
        PointLocator6(),
        PointLocator7(),
        PointLocator8(),
    ]
    LEFT = 0
    TOP = 2
    RIGHT = 4
    BOTTOM = 6
    corner_inds = [LEFT, TOP, RIGHT, BOTTOM]
    center_inds = [0, 2, 6, 4]

    def __call__(self, left, right):
        params = (left.x, left.y, left.r, right.x, right.y, right.r)
        corners = list(left.corners())

        i = 0
        while i != 4 and corners[i] not in right:
            i += 1

        if i == 4: # no corners from left are in right
            i = int(left.x < right.x)
            i <<= 1
            i += int(left.y < right.y)
            return (self.pointLocators[self.center_inds[i]](*params), self.pointLocators[self.center_inds[i] - 1](*params))
        else:
            while corners[i] in right:
                i -= 1
            going_in = self.corner_inds[i + 1]
            while corners[i] not in right:
                i -= 1
            coming_out = self.corner_inds[i]
            return (self.pointLocators[going_in](*params), self.pointLocators[coming_out + 1](*params))

def square_intersection1(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx1, dx + dy - dr - sx1)

def square_intersection2(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx1, -dx + dy + dr + sx1)

def square_intersection3(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx1, -dx + dy - dr + sx1)

def square_intersection4(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx1, dx + dy + dr - sx1)

def square_intersection5(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx - dy - dr + sy2, sy2)

def square_intersection6(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx + dy + dr - sy2, sy2)

def square_intersection7(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx + dy - dr - sy2, sy2)

def square_intersection8(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx - dy + dr + sy2, sy2)

def square_intersection9(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx2, dx + dy + dr - sx2)

def square_intersection10(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx2, -dx + dy - dr + sx2)

def square_intersection11(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx2, -dx + dy + dr + sx2)

def square_intersection12(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (sx2, dx + dy - dr - sx2)

def square_intersection13(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx - dy + dr + sy1, sy1)

def square_intersection14(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx + dy - dr - sy1, sy1)

def square_intersection15(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx + dy + dr - sy1, sy1)

def square_intersection16(sx1, sy1, sx2, sy2, dx, dy, dr):
    return (dx - dy - dr + sy1, sy1)

class OutOfBoundsIntervalFinder:
    def __init__(self):
        self.locators = [
                [
                    [square_intersection1, square_intersection2],
                    [square_intersection3, square_intersection4],
                ],
                [
                    [square_intersection5, square_intersection6],
                    [square_intersection7, square_intersection8],
                ],
                [
                    [square_intersection9, square_intersection10],
                    [square_intersection11, square_intersection12],
                ],
                [
                    [square_intersection13, square_intersection14],
                    [square_intersection15, square_intersection16],
                ],
            ]
        self.conds = [
            [lambda d, s: d.left()[0] <= s.x1, lambda d, s: d.x < s.x1],
            [lambda d, s: d.top()[1] >= s.y2, lambda d, s: d.y > s.y2],
            [lambda d, s: d.right()[0] >= s.x2, lambda d, s: d.x > s.x2],
            [lambda d, s: d.bottom()[1] <= s.y1, lambda d, s: d.y < s.y1]
        ]

    def __call__(self, diamond, square):
        args = (square.x1,  square.y1, square.x2, square.y2, diamond.x, diamond.y, diamond.r)
        for i, conds in enumerate(self.conds):
            if not conds[0](diamond, square):
                continue
            j = conds[1](diamond, square)
            locators = self.locators[i][j]
            p = (locators[0](*args), locators[1](*args))
            yield p


class Square:
    def __init__(self, lower, upper):
        self.x1, self.y1 = lower
        self.x2, self.y2 = upper

    def __contains__(self, p):
        return self.lower[0] <= p[0] and p[0] <= self.upper[0] and self.lower[1] <= p[1] and p[1] <= self.upper

class Diamond:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def distance(self, p):
        return abs(p[0] - self.x) + abs(p[1] - self.y)

    def __contains__(self, p):
        return self.distance(p) <= self.r

    def fully_contains(self, diamond):
        return diamond.r + self.distance(diamond.loc()) <= self.r

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
    find_bounds_intersection = OutOfBoundsIntervalFinder()
    find_intersections = DiamondIntersectionFinder()
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.overlappers = set()
        self.converter = PerimeterPointToIntConverter(self)
        self.by_start = cmp_to_key(lambda t, i: t[0] - i)
        self.by_stop = cmp_to_key(lambda t, i: t[1] - i)
        self.perimeter = [(0, 4 * r - 1)]

    def overlaps(self, other):
        return self.distance(other.loc()) <= self.r + other.r

    def add_overlappers(self, diamonds):
        for diamond in diamonds:
            if self.overlaps(diamond) and self.loc() != diamond.loc():
                self.overlappers.add(diamond)

    def constrain_perimeter(self, square):
        for interval in self.find_bounds_intersection(self, square):
            self.remove_from_perimeter(interval)

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
                if i < len(self.perimeter) and self.perimeter[i][0] < start:
                    self.perimeter[i] = (self.perimeter[i][0], start - 1)
                    i += 1
                if 0 <= j and stop < self.perimeter[j][1]:
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
