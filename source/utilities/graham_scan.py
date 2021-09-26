from queue import LifoQueue
from copy import deepcopy

# Based on: https://gist.github.com/lvngd/54a26a748c073d35e269f90419c0f629
class GrahamScan(object):
   
   @staticmethod
   def getConvexHull(plotList):
        hull = []
        points = deepcopy(plotList)
        points.sort(key=lambda x:[x[0],x[1]])
        start = points.pop(0)
        hull.append(start)
        points.sort(key=lambda p: (GrahamScan.__getSlope(p, start), -p[1], p[0]))
        for pt in points:
            hull.append(pt)
            while len(hull) > 2 and GrahamScan.__getCrossProduct(hull[-3], hull[-2], hull[-1]) < 0:
                hull.pop(-2)
        return hull

   @staticmethod
   def __getCrossProduct(p1, p2, p3):
        return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))

   @staticmethod
   def __getSlope(p1, p2):
        if p1[0] == p2[0]:
            return float('inf')
        else:
            return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])