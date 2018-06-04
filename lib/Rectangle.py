from Point import Point


class Rectangle:
    def __init__(self, leftUpper, rightLower):
        self.leftUpper = Point(leftUpper.x, leftUpper.y)
        self.rightLower = Point(rightLower.x, rightLower.y)

    def area(self):
        return (self.rightLower.x - self.leftUpper.x) * (self.rightLower.y - self.leftUpper.y)

    def increaseArea(self, service):
        x = max(self.rightLower.x, service.rightLower.x) - min(self.leftUpper.x, service.leftUpper.x)
        y = max(self.rightLower.y, service.rightLower.y) - min(self.leftUpper.y, service.leftUpper.y)
        return x * y - self.area()

    def overlapArea(self, service):
        x = min(self.rightLower.x, service.rightLower.x) - max(self.leftUpper.x, service.leftUpper.x)
        y = min(self.rightLower.y, service.rightLower.y) - max(self.leftUpper.y, service.leftUpper.y)
        if x <= 0 or y <= 0:
            x, y = 0, 0
        return self.area() - x * y

    def resize(self, obj):
        changed = False
        if self.leftUpper.x > obj.leftUpper.x:
            self.leftUpper.x = obj.leftUpper.x
            changed = True
        if self.rightLower.x < obj.rightLower.x:
            self.rightLower.x = obj.rightLower.x
            changed = True
        if self.leftUpper.y < obj.leftUpper.y:
            self.leftUpper.y = obj.leftUpper.y
            changed = True
        if self.rightLower.y > obj.rightLower.y:
            self.rightLower.y = obj.rightLower.y
            changed = True
        return changed

    def _isInside(self, obj):
        return self.leftUpper.x <= obj.x <= self.rightLower.x and self.rightLower.y <= obj.y <= self.leftUpper.y

    def isOverlaps(self, obj):
        if self._isInside(obj.leftUpper) or self._isInside(obj.rightLower):
            return True
        leftLowerObj = Point(obj.leftUpper.x, obj.rightLower.y)
        if self._isInside(leftLowerObj):
            return True
        rightUpperObj = Point(obj.rightLower.x, obj.leftUpper.y)
        if self._isInside(rightUpperObj):
            return True
        return False
