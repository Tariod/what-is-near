import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def isInside(self, rectangle):
        x = (rectangle.rightLower.x + rectangle.leftUpper.x) / 2
        y = (rectangle.leftUpper.y + rectangle.rightLower.y) / 2
        distance = math.sqrt(math.pow(x - self.centre.x, 2) + math.pow(y - self.centre.y, 2))
        return distance <= self.radius


class Rectangle:
    def __init__(self, leftUpper, rightLower):
        self.leftUpper = Point(leftUpper.x, leftUpper.y)
        self.rightLower = Point(rightLower.x, rightLower.y)

    def area(self):
        return (self.rightLower.x - self.leftUpper.x) * (self.rightLower.y - self.leftUpper.y)

    def increaseArea(self, service):
        x = min(self.rightLower.x, service.rightLower.x) - max(self.leftUpper.x, service.leftUpper.x)
        y = min(self.rightLower.y, service.rightLower.y) - max(self.leftUpper.y, service.leftUpper.y)
        if x == 0:
            return y * (self.rightLower.x - self.leftUpper.x)
        if y == 0:
            return x * (self.rightLower.x - self.leftUpper.x)
        return x * y

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


class Service(Rectangle):
    def __init__(self, coordinate, type, subtype, name, address):
        Rectangle.__init__(self, coordinate, coordinate)
        self.type = type
        self.subtype = subtype
        self.name = name
        self.address = address


class Node(Rectangle):
    def __init__(self, obj):
        Rectangle.__init__(self, obj.leftUpper, obj.rightLower)
        self.parent = None

    def updateParentBound(self):
        parent = self.parent
        if parent:
            changed = parent.resize(self)
            if changed:
                parent.updateParentBound()


class NodeInner(Node):
    def __init__(self, child):
        Node.__init__(self, child)
        child.parent = self
        self.children = [child]

    def addChild(self, child):
        self.children.append(child)
        child.parent = self
        child.updateParentBound()

    def removeChild(self, child):
        self.children.remove(child)


class NodeLeaf(Node):
    def __init__(self, service):
        Node.__init__(self, service)
        self.services = [service]

    def addService(self, service):
        self.services.append(service)
        self._updateBound(service)

    def _updateBound(self, service):
        changed = self.resize(service)
        if changed:
            self.updateParentBound()


class Rtree:
    def __init__(self, max):
        self.max = max
        self.min = math.ceil(max * 0.4)
        self.root = None

    def find(self, position, radius):
        region = Circle(position, radius)
        regionRect = Rectangle(Point(position.x - radius, position.y + radius), Point(position.x + radius, position.y - radius))
        result = self._find(self.root, regionRect)
        for service in result:
            if region.isInside(service) is False:
                result.remove(service)
            else:
                print("=====================")
                print("Name:", service.name)
                print("Type:", service.type)
                print("Subtype:", service.subtype)
                print("Address:", service.address)

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
        if self.root is None:
            self.root = NodeLeaf(obj)
        else:
            currNode = self._chooseSubtree(self.root, obj)
            if len(currNode.services) < self.max:
                currNode.addService(obj)
            else:
                self._split(currNode, obj)

    def _chooseSubtree(self, root, obj):
        if isinstance(root, NodeLeaf):
            return root
        else:
            increasesEl = [root.children[0]]
            minIncreases = root.children[0].increaseArea(obj)
            temp = 0
            for child in root.children[1:]:
                temp = child.increaseArea(obj)
                if temp < minIncreases:
                    increasesEl.clear()
                    increasesEl.append(child)
                    minIncreases = temp
                elif temp == minIncreases:
                    increasesEl.append(child)
            if len(increasesEl) > 1:
                increasesEl.sort(key=lambda child: child.area())
            curr = self._chooseSubtree(increasesEl[0], obj)
        return curr

    def _split(self, node, service):
        mid = int((self.max + 1) / 2)
        left = NodeLeaf(node.services[0])
        right = NodeLeaf(node.services[mid])
        for index in range(1, mid):
            left.addService(node.services[index])
        for index in range(mid + 1, self.max):
            right.addService(node.services[index])
        right.addService(service)
        father = node.parent
        if father is None:
            self.root = father = NodeInner(left)
        else:
            father.removeChild(node)
            father.addChild(left)
        if len(father.children) < self.max:
            father.addChild(right)
        else:
            self._splitNode(father, right)

    def _splitNode(self, father, node):
        if father.father is None:
            self.root = NodeInner(father)
            self.root.addChild(father)
            self.root.addChild(node)
        elif len(father.children) < self.max:
            father.addChild(node)
        else:
            mid = int((self.max + 1) / 2)
            left = NodeInner(node.children[0])
            right = NodeInner(node.children[mid])
            for index in range(mid):
                left.addChild(node.children[index])
            for index in range(mid, self.max):
                right.addChild(node.children[index])
            right.addChild(node)
            father.father.removeChild(father)
            father.father.addChild(left)
            self._splitNode(father.father, right)
