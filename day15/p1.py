import re
from functools import cmp_to_key
from queue import deque

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
    def __init__(self, interval=None, sensors=set()):
        self.interval = interval
        self.sensors = sensors

    def intersection(self, left, right):
        # if one of them is None, return the other. If both are None, return None
        if not left:
            return right
        if not right:
            return left
        return (max(left[0], right[0]), min(left[1], right[1]))

    def intersect(self, sensor):
        new_interval = self.intersection(self.interval, sensor.coverage())
        new_sensors = set(self.sensors)
        new_sensors.add(sensor)
        return type(self)(interval=new_interval, sensors=new_sensors)

class UnionFinder:
    def spots_covered(self, sensors):
        sensors.sort()
        overlappers = dict(map(lambda s: (s, set()), sensors))
        overlaps = [Overlap().intersect(sensors[0])]
        for i, sensor in enumerate(sensors, 1):
            overlap = Overlap().intersect(sensor)
            overlaps.append(overlap)
            tocheck = sensors[i - 1]
            while tocheck:
                if tocheck.highest() >= sensor.lowest(): #overlap
                    





