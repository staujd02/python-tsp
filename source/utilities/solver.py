from queue import PriorityQueue

from source.dataStructures import Vector, Step, GraphStep
from source.utilities.graph import Graph

class Solver(object):
    
    def solve(self, zeroGraph, vectors):
        queue = PriorityQueue()
        queue.put((vectors[0][2], Step([vectors[0]], 1)))
        i = 0
        runningWeight = vectors[0][2]
        while not queue.empty():
            i += 1
            (weight, pop) = queue.get()
            g = self.check(zeroGraph, pop.list)
            if g.isValid():
                zeroGraph.replace(pop.list)
                return zeroGraph
            if pop.idx < len(vectors):
                v = vectors[pop.idx]
                self.goAcross(v, pop, weight, queue)
                if g.getWeight() >= runningWeight:
                    runningWeight = g.getWeight()
                    self.goDeep(v, pop, weight, queue)
        return None
    
    def check(self, zeroGraph, alterList):
        g = zeroGraph.copy()
        g.replace(alterList)
        return g
    
    def safe_createAugmentList(self, zeroGraph, vectors, stop):
        masterList = []
        queue = PriorityQueue()
        high = vectors[0][2]
        queue.put((high, Step([vectors[0]], 1)))
        while not queue.empty():
            (weight, pop) = queue.get()
            masterList.append(pop.list)
            if len(masterList) == stop:
                break
            if pop.idx < len(vectors):
                v = vectors[pop.idx]
                self.goAcross(v, pop, weight, queue)
                self.goDeep(v, pop, weight, queue)
        return masterList

    def createAugmentList(self, zeroGraph, vectors):
        masterList = []
        queue = PriorityQueue()
        high = vectors[0][2]
        queue.put((high, Step([vectors[0]], 1)))
        while not queue.empty():
            (weight, pop) = queue.get()
            masterList.append(pop.list)
            if pop.idx < len(vectors):
                v = vectors[pop.idx]
                self.goAcross(v, pop, weight, queue)
                self.goDeep(v, pop, weight, queue)
        return masterList
    
    def goAcross(self, v, pop, weight, queue):
        l = list(pop.list)
        oldVector = l.pop()
        l.append(v)
        newWeight = weight - oldVector[2] + v[2]
        queue.put((newWeight, Step(l, pop.idx + 1)))
    
    def goDeep(self, v, pop, weight, queue):
        newWeight = weight + v[2]
        l = list(pop.list)
        l.append(v)
        queue.put((newWeight, Step(l, pop.idx + 1)))