import re

class Sensor:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def distance(self, p):
        return abs(p[0] - self.x) + abs(p[1] - self.y)

    def contains(self, p):
        return self.distance(p) <= self.r

    def loc(self):
        return (self.x, self.y)

    def __repr__(self):
        return f'{type(self).__name__}(x={self.x}, y={self.y}, r={self.r})'

    @classmethod
    def from_sensor_and_beacon(cls, sensor_point, beacon_point):
        sensor = cls.__new__(cls)
        sensor.x, sensor.y = sensor_point
        sensor.r = sensor.distance(beacon_point)
        return sensor

class Bound:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.corners = [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)]

    def contains(self, point):
        return self.minx <= point[0] and point[0] <= self.maxx and self.miny <= point[1] and point[1] <= self.maxy

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
            sensors.append(Sensor.from_sensor_and_beacon((sx, sy), (bx, by)))
            beacons.add((bx, by))
    return sensors, beacons


target = 2000000

sensors, _ = read_input()

minx = 0
miny = 0
maxx = 4000000
maxy = 4000000

bounds = Bound(minx, miny, maxx, maxy)

nsensors = 0
print (','.join(map(lambda c: str(c), bounds.corners)))
for s in sensors:
    if (bounds.contains(s.loc())):
        corners = [(s.x - s.r, s.y), (s.x, s.y + s.r), (s.x + s.r, s.y), (s.x, s.y - s.r)]
        print (f"polygon({','.join(map(lambda c: str(c), corners))})")
        nsensors += 1
        continue
    for c in bounds.corners:
        if s.contains(c):
            corners = [(s.x - s.r, s.y), (s.x, s.y + s.r), (s.x + s.r, s.y), (s.x, s.y - s.r)]
            print (f"polygon({','.join(map(lambda c: str(c), corners))})")
            nsensors += 1
            break

print("copy above lines into desmos and look for part of the grid that isn't covered")