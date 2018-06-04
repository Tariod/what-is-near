import math


class Circle:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def isInside(self, rectangle):
        x = (rectangle.rightLower.x + rectangle.leftUpper.x) / 2
        y = (rectangle.leftUpper.y + rectangle.rightLower.y) / 2
        distance = math.sqrt(math.pow(x - self.centre.x, 2) + math.pow(y - self.centre.y, 2))
        return distance <= self.radius
