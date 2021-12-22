import math
class Tracker:
    def __init__(self, threshold: float, historyamt: int):
        self.objecthistory = list()
        self.threshold = threshold
        self.accum = 0 
        self.historyamt = historyamt
    def register(self, nobj):
        pass
    def deregister(self, ident):
        pass
    def update(self, newobjects):
        current = {}
        for x in newobjects.copy():
            closest_point = self.get_closest(x)
            if closest_point is not None:
                current[closest_point[0]] = x
                newobjects.remove(x)
        for x in newobjects:
            current[self.accum] = x
            self.accum += 1
        if len(self.objecthistory) >= self.historyamt:
            del self.objecthistory[self.historyamt-1:]
        self.objecthistory.insert(0, current)
    def distance(self, a, b): 
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        cx=bx-ax
        cy=by-ay
        return math.sqrt(cx**2+cy**2)
    def get_closest(self, grid):
        closest_point = None
        for index, objects in enumerate(self.objecthistory):
            for ident, x in objects.items():
                dist=self.distance(x,grid)
                if (closest_point is None or dist < closest_point[2]) and dist < self.threshold*(1+(index*1.3)):
                    closest_point=(ident, x, dist)
            if closest_point is not None:
                break
        return closest_point
