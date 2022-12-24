import re
from functools import cmp_to_key
from queue import deque
from sortedcontainers import SortedSet

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
            self.sensors = set()
            self.sensors.add(sensor)
        elif interval and sensors and not sensor:
            self.interval = interval
            self.sensors = sensors
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

    def lowest(self):
        return self.interval[0]

class UnionFinder:
    def spots_covered(self, sensors):
        overlap_key = lambda o: o.lowest()
        overlapers = dict()
        singleoverlaps = SortedSet([Overlap(sensor=s) for s in sensors], overlap_key)
        overlaps = [set(singleoverlaps), set()]

        # break this down into methods ...
        for i, initial_overlap in enumerate(singleoverlaps):
            overlapers[initial_overlap] = set()
            for j in reversed(range(i)):
                if new_overlap := initial_overlap.intersect(singleoverlaps[j]):
                    overlaps[1].add(new_overlap)
                    overlapers[initial_overlap].add(singleoverlaps[j])
                else: # if we don't overlap with singleoverlaps[j], then we only
                      # need to check overlaps which do overlap it
                    for overlap in overlapers[singleoverlaps[j]]:
                        if new_overlap := initial_overlap.intersect(overlap):
                            overlaps[1].add(new_overlap)
                            overlapers[initial_overlap].add(singleoverlaps[j])
                    break
        covered = 0
        for o in overlaps[0]:
            covered += o.interval[1] - o.interval[0] + 1
        for o in overlaps[1]:
            covered -= o.interval[1] - o.interval[0] + 1
        return covered