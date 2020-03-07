from queue import PriorityQueue

from source.dataStructures import Vector, Step, GraphStep
from source.utilities.graph import Graph

from time import time

class Solver(object):
    
    def solve(self, zeroGraph, vectors):
        queue = PriorityQueue()
        graph = zeroGraph.copy()
        graph.replace(vectors[0])
        queue.put((graph.getWeight(), GraphStep(graph, 1)))
        runningWeight = graph.getWeight()
        timeSpentGoingAcross = 0
        timeSpentGoingDeeper = 0
        timeSpentVerifying = 0
        while not queue.empty():
            (weight, pop) = queue.get()
            # TIME BLOCK
            start = time()
            isValid = pop.graph.isValid()
            timeSpentVerifying += time() - start
            # TIME BLOCK
            if isValid:
                print("Run Time of Across: " + str(timeSpentGoingAcross))
                print("Run Time of Deeper: " + str(timeSpentGoingDeeper))
                print("Run Time of Verifying: " + str(timeSpentVerifying))
                return pop.graph
            if pop.idx < len(vectors):
                v = vectors[pop.idx]
                if pop.graph.getWeight() >= runningWeight:
                    runningWeight = pop.graph.getWeight()
                    # TIME BLOCK
                    start = time()
                    self.goGraphDeep(v, pop, weight, queue)
                    timeSpentGoingDeeper += time() - start
                    # TIME BLOCK
                # TIME BLOCK
                start = time()
                self.goGraphAcross(v, pop, weight, queue)
                timeSpentGoingAcross += time() - start
                # TIME BLOCK
        return None

    def check(self, zeroGraph, alterList):
        g = zeroGraph.copy()
        g.replace(alterList)
        if g.getWeight() == 80:
            print(g)
        return g.isValid()
    
    def goGraphAcross(self, v, pop, weight, queue):
        newWeight = pop.graph.goAcross(v, weight)
        queue.put((newWeight, GraphStep(pop.graph, pop.idx + 1)))
    
    def goGraphDeep(self, v, pop, weight, queue):
        graph = pop.graph.copy()
        newWeight = graph.goDeeper(v, weight)
        queue.put((newWeight, GraphStep(graph, pop.idx + 1)))

    def oldSolve(self, zeroGraph, vectors):
        queue = PriorityQueue()
        queue.put((vectors[0][2], Step([vectors[0]], 1)))
        i = 0
        while not queue.empty():
            i += 1
            (weight, pop) = queue.get()
            if self.check(zeroGraph, pop.list):
                zeroGraph.replace(pop.list)
                return zeroGraph
            if pop.idx < len(vectors):
                v = vectors[pop.idx]
                self.goAcross(v, pop, weight, queue)
                self.goDeep(v, pop, weight, queue)
        return None

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