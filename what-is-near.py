import sys
sys.path.append('./lib/')
from Rtree import Rtree
from Point import Point
from Service import Service


def parse(fileNme):
    with open(fileNme) as file:
        data = file.read().split('\n')
        data = [field.split(';') for field in data[:-1]]
    return data


rtree = Rtree(5)
data = parse('./data/ukraine.csv')
for service in data:
    rtree.insert(Service(Point(float(service[0]), float(service[1])), service[2], service[3], service[4], service[5]))
print('Rtree built')
res = rtree.find(Point(50.448000, 30.451600), 200)
for service in res:
    print('=====================')
    print('Name:', service.name)
    print('Type:', service.type)
    print('Subtype:', service.subtype)
    print('Address:', service.address)
