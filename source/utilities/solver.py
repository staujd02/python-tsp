from queue import PriorityQueue

from source.dataStructures import Vector, Step, GraphStep
from source.utilities.graph import Graph

class Solver(object):
    
    def solve(self, zeroGraph, vectors):
        queue = PriorityQueue()
        graph = zeroGraph.copy()
        graph.replace(vectors[0])
        queue.put((graph.getWeight(), GraphStep(graph, 1)))
        runningWeight = graph.getWeight()
        while not queue.empty():
            (weight, pop) = queue.get()
            if pop.graph.isValid():
                return pop.graph
            if pop.idx < len(vectors):
                v = vectors[pop.idx]
                self.goGraphAcross(v, pop, weight, queue)
                if pop.graph.getWeight() >= runningWeight:
                    runningWeight = pop.graph.getWeight()
                    self.goGraphDeep(v, pop, weight, queue)
        return None
    
    def goGraphAcross(self, v, pop, weight, queue):
        graph = pop.graph.copy()
        newWeight = graph.goAcross(v, weight)
        queue.put((newWeight, GraphStep(graph, pop.idx + 1)))
    
    def goGraphDeep(self, v, pop, weight, queue):
        newWeight = pop.graph.goDeeper(v, weight)
        queue.put((newWeight, GraphStep(pop.graph, pop.idx + 1)))
    
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