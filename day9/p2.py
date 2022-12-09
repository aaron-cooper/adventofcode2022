import re

def sign(x):
  return int(x > 0) - int(x < 0)

class Movement:
    def __init__(self, distance):
        self.distance = distance

    def step(self, knot):
        if self.distance == 0:
            return False
        self.step_knot_one(knot)
        self.distance -= 1
        return True

class UpMovement(Movement):
    def __init__(self, distance):
        super().__init__(distance)

    def step_knot_one(self, knot):
        knot.y += 1

class DownMovement(Movement):
    def __init__(self, distance):
        super().__init__(distance)

    def step_knot_one(self, knot):
        knot.y -= 1

class LeftMovement(Movement):
    def __init__(self, distance):
        super().__init__(distance)

    def step_knot_one(self, knot):
        knot.x -= 1

class RightMovement(Movement):
    def __init__(self, distance):
        super().__init__(distance)

    def step_knot_one(self, knot):
        knot.x += 1

class MovementFactory:
    def __init__(self):
        self.string_to_type = {
            'U': UpMovement,
            'D': DownMovement,
            'L': LeftMovement,
            'R': RightMovement
        }

    def create_movement(self, movement_string):
        m = re.search("([UDLR]) (\d+)", movement_string)
        return self.string_to_type[m.group(1)](int(m.group(2)))

class Knot:
    def __init__(self):
        self.x = 0
        self.y = 0

    def follow(self, other_knot):
        delta_x = other_knot.x - self.x
        delta_y = other_knot.y - self.y
        if abs(delta_x) + abs(delta_y) - int(delta_x != 0 and delta_y != 0) > 1:
            self.x += sign(delta_x)
            self.y += sign(delta_y)


    def as_tuple(self):
        return (self.x, self.y)


class Rope:
    def __init__(self, knots):
        self.knots = [Knot() for i in range(knots)]
        self.visited_by_tail = set()

    def head(self):
        return self.knots[0]

    def tail(self):
        return self.knots[len(self.knots) - 1]

    def move(self, movement):
        while movement.step(self.head()):
            for i in range(1, len(self.knots)):
                self.knots[i].follow(self.knots[i - 1])
            self.visited_by_tail.add(self.tail().as_tuple())

    def num_visited_by_tail(self):
        return len(self.visited_by_tail)

factory = MovementFactory()
rope = Rope(10)
with open("input.txt", "r") as infile:
    for line in infile:
        movement = factory.create_movement(line.strip())
        rope.move(movement)

print(rope.num_visited_by_tail())
