import math
class Tracker:
    def __init__(self, threshold: float):
        self.objects = {}
        self.accum = 0
        self.threshold = threshold
    def register(self, nobj):
        self.objects[self.accum] = nobj
        self.accum += 1
    def deregister(self, ident):
        del self.objects[ident]
    def update(self, newobjects):
        #update all existing points, deregistering if neccesary
        removed = list()
        for ident, x in self.objects.items():
            closest_point = None
            for y in newobjects:
                dist = self.distance(x, y)
                if dist<self.threshold and (closest_point is None or dist<closest_point[1]):
                    closest_point = (y, dist)
            if closest_point is None:
                removed.append(ident)
            else:
                self.objects[ident] = closest_point[0]
                newobjects.remove(closest_point[0])
        for x in removed:
            self.deregister(x)
        for x in newobjects:
            self.register(x)
    def distance(self, a, b):
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        cx=bx-ax
        cy=by-ay
        return math.sqrt(cx**2+cy**2)
