class BoundsChecker:
    def __init__(self, lower, upper):
        (self.lower_x, self.lower_y) = lower
        (self.upper_x, self.upper_y) = upper

    def __call__(self, point):
        (x, y) = point
        return self.lower_x <= x and x <= self.upper_x and self.lower_y <= y and y <= self.upper_y

    def check(self, point):
        return self(point)