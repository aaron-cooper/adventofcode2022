import re
from helpers.bsearch import bsearch
from collections import deque

class PerimeterPoint:
    def __init__(self, loc, centre):
        self.x, self.y = loc
        self.cx, self.cy = centre

    def __lt__(self, other):
        if self.y >= self.cy and other.y >= self.cy:
            return self.x < other.x
        elif self.y < self.cy and other.y < self.cy:
            return self.x > other.x
        else:
            return self.y >= self.cy

    def centre(self):
        return self.cx, self.cy

    def loc(self):
        return self.x, self.y

class Interval:
    def __init__(self, sensor):
        self.sensor = sensor
        self.start = (sensor.x - sensor.r, sensor.y)
        self.stop = (sensor.x - sensor.r + 1, sensor.y - 1)

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

class PerimeteredDiamond(Diamond):
    def __init__(self, x, y, r):
        super().__init__(x, y, r)
        self.overlappers = set()
        self.perimeter = [Interval(self)]

    def overlaps(self, other):
        return self.distance(other.loc()) <= self.r + other.r

    def add_overlappers(self, sensor_iter):
        for sensor in sensor_iter:
            if self.overlaps(sensor):
                self.overlappers.add(sensor)
                sensor.overlappers.add(self)

    def remove_overlapping_perimeter(self, other):
        raise NotImplementedError()

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


def read_input():
    with open('input.txt', 'r') as f:
        sensors=[]
        beacons=set()
        for line in map(lambda l: l.strip(), f):
            m = re.search(r"Sensor at x=([+-]?\d+), y=([+-]?\d+): closest beacon is at x=([+-]?\d+), y=([+-]?\d+)", line)
            sx = int(m.group(1))
            sy = int(m.group(2))
            bx = int(m.group(3))
            by = int(m.group(4))
            sensors.append(Diamond.from_sensor_and_beacon((sx, sy), (bx, by)))
            beacons.add((bx, by))
    return sensors, beacons

# sensors, _ = read_input()

# for i, sensor in enumerate(sensors):
#     sensor.add_overlappers(sensors[0:i])

# pass

# for s in sensors:
#     print (s.desmos_repr())
