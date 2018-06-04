from Rectangle import Rectangle


class Node(Rectangle):
    def __init__(self, obj):
        Rectangle.__init__(self, obj.leftUpper, obj.rightLower)
        self.parent = None


class NodeInner(Node):
    def __init__(self, child):
        Node.__init__(self, child)
        child.parent = self
        self.children = [child]

    def updateBound(self):
        changed = False
        for child in self.children:
            if self.resize(child):
                changed = True
        if changed and self.parent is not None:
            self.parent.updateBound()

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

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
        if changed and self.parent is not None:
            self.parent.updateBound()
