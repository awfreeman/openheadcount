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

    def distance(self, a, b): 
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        cx=bx-ax
        cy=by-ay
        return math.sqrt(cx**2+cy**2)