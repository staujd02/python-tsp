import copy

from source.dataStructures import Vector, NoOpCompare

class BranchingGraphError(Exception):
    pass

class Graph(NoOpCompare):

    def __init__(self, baseVectors):
        self.data = {}
        self.weight = 0
        self.lastChange = None
        self.graphLength = len(baseVectors)
        for vector in baseVectors:
            self.__assignVector(vector)
            self.weight += vector[2]
        if len(self.data) != len(baseVectors):
            raise BranchingGraphError

    def copy(self):
        g = Graph([])
        g.data = copy.deepcopy(self.data)
        g.weight = self.weight
        g.lastChange = self.lastChange
        g.graphLength = self.graphLength
        return g
    
    def goAcross(self, vector, weight):
        oldWeight = self.lastChange[2]
        self.swapOutLastChange()
        self.replace(vector)
        return  weight - oldWeight + vector[2]
    
    def swapOutLastChange(self):
        self.replace(self.lastChange)

    def goDeeper(self, vector, weight):
        self.replace(vector)
        return weight + vector[2]

    def replace(self, vector):
        v = self.data[vector[0]]
        self.lastChange = v
        self.weight += vector[2] - v[2]
        self.__assignVector(vector)

    def isValid(self):
        visited = {}
        start = next(iter(self.data))
        if len(self.data) != self.graphLength:
            return False
        while True:
            if visited.get(start[0], False):
                break
            visited[start[0]] = True
            start = self.data[start][1]
        return len(visited) == len(self.data)

    def getWeight(self):
        return self.weight

    def toVectorListString(self):
        s = "{"
        for v in iter(self.data):
            s += str(self.data[v])
        return s + "}"

    def __assignVector(self, vector):
        self.data[vector[0]] = vector

    def __str__(self):
        visited = {}
        start = next(iter(self.data))
        literal = "(" + start
        while True:
            if visited.get(start[0], False):
                break
            literal += "->"
            visited[start[0]] = True
            start = self.data[start][1]
            literal += start
        return literal + "): " + str(self.weight)

    def __unicode__(self):
        return u"" + self.__str__()
