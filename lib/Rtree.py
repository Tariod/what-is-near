from math import ceil
from Point import Point
from Circle import Circle
from Rectangle import Rectangle
from Node import NodeLeaf, NodeInner


class Rtree:
    def __init__(self, max):
        self.max = max
        self.min = ceil(max * 0.4)
        self.root = None

    def find(self, position, radius):
        position.mercator()
        region = Circle(position, radius)
        regionRect = Rectangle(
            Point(position.x - radius, position.y + radius),
            Point(position.x + radius, position.y - radius)
        )
        servicesInRect = self._find(self.root, regionRect)
        for service in servicesInRect:
          distance = region.isInside(service)
          if distance > radius:
            servicesInRect.remove(service)
        return servicesInRect

    def findType(self, position, radius, typeR):
        correctServices = []
        
        position.mercator()
        region = Circle(position, radius)
        regionRect = Rectangle(
            Point(position.x - radius, position.y + radius),
            Point(position.x + radius, position.y - radius)
        )
        if radius < 250:
          servicesInRect = self._find(self.root, regionRect)
          for service in servicesInRect:
            distance = region.isInside(service)
            if service.type == typeR and distance < radius:
              correctServices.append(service)
        else:
          for r in range(250, radius, 250):
            servicesInRect = self._find(self.root, regionRect)
            for service in servicesInRect:
              distance = region.isInside(service)
              if service.type == typeR and distance < r:
                correctServices.append(service)
            if len(correctServices) > 0:
              break
        return correctServices

    def _find(self, root, region):
        res = []
        if isinstance(root, NodeLeaf):
            for service in root.services:
                if region.isOverlaps(service):
                    res.append(service)
        else:
            for child in root.children:
                if child.isOverlaps(region) or region.isOverlaps(child):
                    res.extend(self._find(child, region))
        return res

    def insert(self, obj):
        obj.leftUpper.mercator()
        obj.rightLower.mercator()
        if self.root is None:
            self.root = NodeLeaf(obj)
        else:
            leaf = self._chooseSubtree(self.root, obj)
            if len(leaf.services) < self.max:
                leaf.addService(obj)
            else:
                self._split(leaf, obj)

    def _chooseSubtree(self, root, obj):
        if isinstance(root, NodeLeaf):
            return root
        else:
            minEl = [root.children[0]]
            minOverlap = root.children[0].overlapArea(obj)
            temp = 0
            children = root.children[1:]
            for child in children:
                temp = child.overlapArea(obj)
                if temp < minOverlap:
                    minEl.clear()
                    minEl.append(child)
                    minOverlap = temp
                elif temp == minOverlap:
                    minEl.append(child)
            if len(minEl) > 1:
                children = minEl[:]
                minEl.clear()
                minIncreases = children[0].increaseArea(obj)
                minEl.append(children[0])
                for child in children[1:]:
                    temp = child.increaseArea(obj)
                    if temp < minIncreases:
                        minEl.clear()
                        minEl.append(child)
                        minIncreases = temp
                    elif temp == minIncreases:
                        minEl.append(child)
                if len(minEl) > 1:
                    minEl.sort(key=lambda child: child.area())
            return self._chooseSubtree(minEl[0], obj)

    def _split(self, leaf, service):
        mid = int((self.max + 1) / 2)
        leaf.services.sort(key=lambda service: service.leftUpper.x)
        left = NodeLeaf(leaf.services[0])
        right = NodeLeaf(leaf.services[mid])
        for index in range(1, mid):
            left.addService(leaf.services[index])
        for index in range(mid + 1, self.max):
            right.addService(leaf.services[index])
        if right.services[0].leftUpper.x < service.leftUpper.x:
            right.addService(service)
        else:
            left.addService(service)
        father = leaf.parent
        if father is None:
            self.root = father = NodeInner(left)
        else:
            father.removeChild(leaf)
            father.addChild(left)
            father.updateBound()
        if len(father.children) < self.max:
            father.addChild(right)
            father.updateBound()
        else:
            self._splitNode(father, right)

    def _splitNode(self, father, node):
        if father.parent is None:
            self.root = NodeInner(father)
            self.root.addChild(node)
            self.root.updateBound()
        elif len(father.children) < self.max:
            father.addChild(node)
            father.updateBound()
        else:
            mid = int((self.max + 1) / 2)
            father.children.sort(key=lambda child: child.leftUpper.x)
            left = NodeInner(father.children[0])
            right = NodeInner(father.children[mid])
            for index in range(1, mid):
                left.addChild(father.children[index])
            for index in range(mid + 1, self.max):
                right.addChild(father.children[index])
            if right.children[0].leftUpper.x < node.leftUpper.x:
                right.addChild(node)
            else:
                left.addChild(node)
            left.updateBound()
            right.updateBound()
            father.parent.removeChild(father)
            father.parent.addChild(left)
            father.updateBound()
            self._splitNode(father.parent, right)
