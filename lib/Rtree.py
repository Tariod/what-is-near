import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Service:
    def __init__(self, coordinate, type, subtype, name, address):
        self.coordinate = coordinate
        self.type = type
        self.subtype = subtype
        self.name = name
        self.address = address


class Node:
    def __init__(self):
        self.leftUpper
        self.rightLower
        self.parent
        self.children = []
        self.services = []
        self.isLeaf


class Rtree:
    def __init__(self, max):
        self.max = max
        self.min = math.ceil(max * 0.4)
        self.root
        self.height

    def insert(self):


    def search(self):


    def _chooseSubtree(self):


    def _split(self):


    def _chooseSplitAxis(self):


    def _chooseSplitIndex(self):


