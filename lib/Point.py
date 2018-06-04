import math


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def mercator(self):
        maxLat = 89.5
        rMajor = 6378137.0
        rMinor = 6356752.3142
        if self.y > maxLat:
            self.y = maxLat
        if self.y < -maxLat:
            self.y = -maxLat
        radLong = math.radians(self.x)
        radLat = math.radians(self.y)
        f = rMinor / rMajor
        e = math.sqrt(1 - f ** 2) * 0.5
        self.x = rMajor * radLong
        self.y = (-1)*rMajor*math.log(math.tan(math.pi/4-radLat/2)/((1-e*math.sin(radLat))/(1+e*math.sin(radLat)))**e)

    def mercatorSph(self):
        maxLat = 89.5
        rMajor = 6378137.0
        if self.y > maxLat:
            y = maxLat
        if self.y < -maxLat:
            y = -maxLat
        radLong = math.radians(self.x)
        radLat = math.radians(self.y)
        self.x = rMajor * radLong
        self.y = math.log(math.tan(math.pi/4+radLat/2))*rMajor
