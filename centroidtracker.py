import math
from matplotlib.path import Path
from scipy.spatial import ConvexHull

class Tracker:
    def __init__(self, threshold: float, max_ttl: int, vertexes):
        self.objects = list()
        self.max_ttl = max_ttl
        self.threshold = threshold
        self.accum = 0
        self.hull = ConvexHull(vertexes)
        self.hull_path = Path(vertexes[self.hull.vertices])
        self.count = 0

    def update(self, detections):
        #find the closest point to each point 
        for index, x in enumerate(self.objects):
            closest_point = None
            closest_point_dist = None
            for y in detections:
                dist = self.distance(x[0], y)
                if (closest_point_dist is not None and dist < closest_point_dist) or dist < self.threshold*1.3*(x[1]+1):
                    closest_point_dist = dist
                    closest_point = y 
            #add the closest point and remove from the list of detections
            if closest_point is not None:
                self.objects[index] = [closest_point, 0, x[2], x[3]]
                detections.remove(closest_point)
        
        #add new detections
        for x in detections:
            self.objects.append([x, 0, self.accum, None])
            self.accum += 1
        
        #check if max ttl has been exceeded
        i = 0
        while i < len(self.objects):
            
            if self.objects[i][1] == self.max_ttl:
                del self.objects[i]
            else:
                self.objects[i][1] += 1
                i += 1 
        
        #check positions and update counter accordingly
        i = 0
        while i < len(self.objects):
            if self.hull_path.contains_point(self.objects[i][0]):
                if self.objects[i][3] == False:
                    self.count += 1
                self.objects[i][3] = True
            else:
                if self.objects[i][3] == True:
                    self.count -= 1
                self.objects[i][3] = False
            i += 1
        
    def distance(self, a, b): 
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]
        cx=bx-ax
        cy=by-ay
        return math.sqrt(cx**2+cy**2)