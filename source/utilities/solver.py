from source.dataStructures import Vector

class Solver(object):

    def createAugmentList(self, zeroGraph, vectors):
        masterList = []
        masterList.append(vectors[0])
        self.iterate(masterList, zeroGraph, vectors)

    def iterate(self, masterList, zeroGraph, vectors):
        high = 0
        for (idx, vector) in enumerate(vectors[1:-1]):
            index = idx + 1 # Cus we subtracted off the 1st element, remember?
            masterList.append(vector)
            high = vectors[index+1][2]
            previousVectors = vectors[:index]
            self.lookBack(masterList, vector, previousVectors, high)
        masterList.append(vectors[-1])
        return masterList
            
    def lookBack(self, masterList, currentVector, previousVectors, high):
        low = currentVector[2]
        for vector in previousVectors:
            if not self.lookForward(masterList, vector, previousVectors, vector[2], low, high, [currentVector]):
                break

    def lookForward(self, masterList, currentVector, forwardVectors, runningWeight, low, high, solution):
        if currentVector[2] + runningWeight > high:
            self.handleBreak(solution, masterList, low, runningWeight)
            return False
        if currentVector[2] + runningWeight == high:
            solution.append(currentVector)
            masterList.append(solution)
            if len(forwardVectors) == 0:
                return False
            return forwardVectors[1][2] > currentVector[2]
        else:
            if len(forwardVectors) == 0:
                # self.handleBreak(solution, masterList)
                raise Exception("You just hit the end of the list?")
            solution.append(currentVector)
            trimmedForwardVectors = forwardVectors[1:]
            newRunningWeight = currentVector[2] + runningWeight
            for vector in trimmedForwardVectors:
                if not self.lookForward(masterList, vector, trimmedForwardVectors, newRunningWeight, low, high, solution):
                    break
            return True

    def handleBreak(self, solution, masterList, low, runningWeight):
        if len(solution) != 1 and low > runningWeight:
            masterList.append(solution)
    

