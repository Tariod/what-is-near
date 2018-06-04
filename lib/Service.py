from Rectangle import Rectangle


class Service(Rectangle):
    def __init__(self, coordinate, type, subtype, name, address):
        Rectangle.__init__(self, coordinate, coordinate)
        self.type = type
        self.subtype = subtype
        self.name = name
        self.address = address
