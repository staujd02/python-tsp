from queue import PriorityQueue

from source.dataStructures import Vector, Step

class Solver(object):
    
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

    # def iterate(self, masterList, queue, zeroGraph, vectors):
    #     nextQueue = PriorityQueue()
    #     for (idx, vector) in enumerate(vectors):
    #         high = vector[2]
    #         queue.put((high, Step([vector], idx + 1)))
    #         while not queue.empty():
    #             (weight, pop) = queue.get()
    #             if weight <= high:
    #                 masterList.append(pop.list)
    #                 for (i, v) in enumerate(vectors[pop.idx:]):
    #                     newWeight = weight + v[2]
    #                     if newWeight <= high:
    #                         l = list(pop.list)
    #                         l.append(v)
    #                         queue.put((newWeight, Step(l, pop.idx + i + 1)))
    #                     else:
    #                         if len(pop.list) != 1:
    #                             l = list(pop.list)
    #                             poppedV = l.pop()
    #                             nextQueue.put(
    #                                 (weight, Step(l, pop.idx + 1)))
    #                         l = list(pop.list)
    #                         l.append(v)
    #                         nextQueue.put(
    #                             (newWeight, Step(l, pop.idx + i + 1)))
    #                         break
    #                 nextQueue.put((weight, Step(pop.list, pop.idx + i + 2)))
    #             else:
    #                 nextQueue.put((weight, pop))
    #         queue = nextQueue
    #         nextQueue = PriorityQueue()
    #     return masterList

    # def lookBack(self, masterList, currentVector, previousVectors, high):
    #     low = currentVector[2]
    #     solutionList = []
    #     for vector in previousVectors:
    #         if not self.lookForward(solutionList, vector, previousVectors, vector[2], 0, high, [currentVector]):
    #             break # don't add to solution list here, it's been accounted
    #     for vector in previousVectors:
    #         if not self.lookForward(solutionList, vector, previousVectors, 0, low, high, []):
    #             break # dont' add to solution list here, it's been accounted
    #     # sort solution list
    #     # push to master

    # def lookForward(self, masterList, currentVector, forwardVectors, runningWeight, low, high, solution):
    #     if currentVector[2] + runningWeight > high:
    #         self.handleBreak(solution, masterList, low, runningWeight)
    #         return False
    #     if currentVector[2] + runningWeight == high:
    #         solution.append(currentVector)
    #         masterList.append(solution)
    #         if len(forwardVectors) == 0:
    #             return False
    #         return forwardVectors[1][2] > currentVector[2]
    #     else:
    #         if len(forwardVectors) == 0:
    #             # self.handleBreak(solution, masterList)
    #             raise Exception("You just hit the end of the list?")
    #         solution.append(currentVector)
    #         trimmedForwardVectors = forwardVectors[1:]
    #         newRunningWeight = currentVector[2] + runningWeight
    #         for vector in trimmedForwardVectors:
    #             if not self.lookForward(masterList, vector, trimmedForwardVectors, newRunningWeight, low, high, solution):
    #                 break
    #         return True

    # def handleBreak(self, solution, masterList, low, runningWeight):
    #     if len(solution) != 1 and low > runningWeight:
    #         masterList.append(solution)
