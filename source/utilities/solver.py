from queue import PriorityQueue

from source.dataStructures import Vector, Step


class Solver(object):

    def createAugmentList(self, zeroGraph, vectors):
        masterList = []
        queue = PriorityQueue()
        return self.iterate(masterList, queue, zeroGraph, vectors)

    def iterate(self, masterList, queue, zeroGraph, vectors):
        nextQueue = PriorityQueue()
        for (idx, vector) in enumerate(vectors):
            high = vector[2]
            queue.put((high, Step([vector], idx + 1)))
            while not queue.empty():
                (weight, pop) = queue.get()
                if weight <= high:
                    masterList.append(pop.list)
                    for (i, v) in enumerate(vectors[pop.idx:]):
                        newWeight = weight + v[2]
                        if newWeight <= high:
                            l = list(pop.list)
                            l.append(v)
                            queue.put((newWeight, Step(l, pop.idx + i + 1)))
                        else:
                            l = list(pop.list)
                            l.append(v)
                            nextQueue.put(
                                (newWeight, Step(l, pop.idx + i + 1)))
                            break
                else:
                    nextQueue.put((weight, pop))
            queue = nextQueue
            nextQueue = PriorityQueue()
        return masterList

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
