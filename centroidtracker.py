import math
class Tracker:
    def __init__(self, threshold: float, max_ttl: int):
        self.objects = list()
        self.max_ttl = max_ttl
        self.threshold = threshold
        self.accum = 0
    def update(self, detections):
        for index, x in enumerate(self.objects):
            closest_point = None
            closest_point_dist = None
            for y in detections:
                dist = self.distance(x[0], y)
                if (closest_point_dist is not None and dist < closest_point_dist) or dist < self.threshold*1.3*(x[1]+1):
                    closest_point_dist = dist
                    closest_point = y 
            if closest_point is not None:
                self.objects[index] = [closest_point, 0, x[2]]
                detections.remove(closest_point)
        for x in detections:
            self.objects.append([x, 0, self.accum])
            self.accum += 1
        i = 0
        while i < len(self.objects):
            
            if self.objects[i][1] == self.max_ttl:
                del self.objects[i]
            else:
                self.objects[i][1] += 1
                i += 1 
        
    """
    def __init__(self, threshold: float, historyamt: int):
        self.objecthistory = list()
        self.threshold = threshold
        self.accum = 0 
        self.historyamt = historyamt
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
    """
    def distance(self, a, b): 
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        cx=bx-ax
        cy=by-ay
        return math.sqrt(cx**2+cy**2)
    """
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
    """