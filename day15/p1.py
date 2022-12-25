import re
from functools import cmp_to_key
from queue import deque
from sortedcontainers import SortedSet
from helpers.bsearch import bsearch

class Sensor:
    def __init__(self, x: int, y: int, point):
        px, py = point
        self.x = x
        self.y = y
        self.r = abs(px - x) + abs(py - y)

    def within_y(self, y):
        return abs(self.y - y) <= self.r

    def flatten_y(self, y):
        return FlatSensor.from_sensor(self, y)

class FlatSensor:
    def __init__(self, x, r):
        self.x = x
        self.r = r

    def lowest(self):
        return self.x - self.r

    def highest(self):
        return self.x + self.r

    def coverage(self):
        return (self.lowest(), self.highest())

    def __lt__(self, other):
        return self.x < other.x

    def __repr__(self):
        return f'{type(self).__name__}(x={self.x}, r={self.r})'

    @classmethod
    def from_sensor(cls, sensor, y):
        return cls(sensor.x, sensor.r - abs(sensor.y - y))


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
            sensors.append(Sensor(sx, sy, (bx, by)))
            beacons.add((bx, by))
    return sensors, beacons

class Overlap:
    def __init__(self, sensor=None, interval=None, sensors=None):
        if sensor and not interval and not sensors:
            self.interval = sensor.coverage()
            self.sensors = frozenset([sensor])
        elif interval and sensors and not sensor:
            self.interval = interval
            self.sensors = frozenset(sensors)
        else:
            raise ValueError('specify sensor OR interval and sensors; not both')

    def intersection(self, left, right):
        # if one of them is None, return the other. If both are None, return None
        if not left:
            return right
        if not right:
            return left
        new_interval = (max(left[0], right[0]), min(left[1], right[1]))
        return new_interval if new_interval[0] <= new_interval[1] else None

    def intersect(self, other):
        if not (new_interval := self.intersection(self.interval, other.interval)):
            return None
        new_sensors = self.sensors.union(other.sensors)
        return type(self)(interval=new_interval, sensors=new_sensors)

    def covered(self):
        return self.interval[1] - self.interval[0] + 1

    def __lt__(self, other):
        if self.covered() % 2 == other.covered() % 2:
            return sum(self.interval) // 2 < sum(other.interval) // 2
        elif self.covered() % 2:
            sum(self.interval) / 2 < sum(other.interval) // 2
        else:
            sum(self.interval) // 2 < sum(other.interval) / 2

class UnionFinder:

    def __init__(self, sensors):
        self.sensors = sensors

    def spots_covered(self):
        self.initial_overlaps = sorted(map(lambda s: Overlap(sensor=s), self.sensors))
        self.construct_overlappers()
        overlaps = [self.initial_overlaps]

        i = 0
        while (overlaps[i]):
            overlaps.append(self.new_covered(overlaps[i]))
            i+= 1

        covered = 0
        add_or_sub = 1
        for l in overlaps[0:-1]:
            for o in l:
                covered += add_or_sub * (o.interval[1] - o.interval[0] + 1)
            add_or_sub *= -1

        return covered

    def new_covered(self, previous):
        overlaps = []
        already_added = set()
        for i, overlap in enumerate(previous):
            ind = bsearch(self.initial_overlaps, overlap)
            ind = ~ind if ind < 0 else ind
            for other in reversed(self.initial_overlaps[0:i]):
                new_overlap = overlap.intersect(other)
                if new_overlap and new_overlap.sensors != overlap.sensors and new_overlap.sensors not in already_added:
                    overlaps.append(new_overlap)
                    already_added.add(new_overlap.sensors)
                else:
                    for other in self.overlappers[other]:
                        new_overlap = overlap.intersect(other)
                        if new_overlap and new_overlap.sensors != overlap.sensors and new_overlap.sensors not in already_added:
                            overlaps.append(new_overlap)
                            already_added.add(new_overlap.sensors)
        return overlaps

    def construct_overlappers(self):
        overlappers = dict()
        for i, overlap in enumerate(self.initial_overlaps):
            overlappers[overlap] = set()
            for other in reversed(self.initial_overlaps[0:i]):
                if overlap.intersect(other):
                    overlappers[overlap].add(other)
                else:
                    for other in overlappers[other]:
                        if overlap.intersect(other):
                            overlappers[overlap].add(other)
                break
        self.overlappers = overlappers

target = 2000000

sensors, beacons = read_input()
sensors = map(lambda s: s.flatten_y(target), sensors)
sensors = list(filter(lambda s: s.r >= 0, sensors))
beacons = list(filter(lambda b: b[1] == target, beacons))

finder = UnionFinder(sensors)

print(finder.spots_covered() - len(beacons))
