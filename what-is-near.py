import io
import sys
import argparse

sys.path.append('./lib/')
from Rtree import Rtree
from Point import Point
from Service import Service


parser = argparse.ArgumentParser()
parser.add_argument("db", help="database file to get map info from", type=str)
parser.add_argument("lat", help="latitude of a place", type=float)
parser.add_argument("long", help="longitude of a place", type=float)
parser.add_argument("size", help="size of a sector to search in", type=float)
args = parser.parse_args()


def parse(fileNme):
    with io.open(fileNme, encoding='utf-8') as file:
        data = file.read().split('\n')
        data = [field.split(';') for field in data[:-1]]
    return data


rtree = Rtree(5)
data = parse('./data/' + args.db)
for service in data:
    rtree.insert(Service(Point(float(service[0]), float(service[1])), service[2], service[3], service[4], service[5]))
print('Rtree built')
res = rtree.find(Point(args.lat, args.long), args.size)
for service in res:
    print('=====================')
    print('Name:', service.name)
    print('Type:', service.type)
    print('Subtype:', service.subtype)
    print('Address:', service.address)
