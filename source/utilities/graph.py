import copy

from source.dataStructures import Vector, NoOpCompare

class BranchingGraphError(Exception):
    pass

class Graph(NoOpCompare):

    def __init__(self, baseVectors):
        self.data = {}
        self.weight = 0
        self.lastChange = None
        for vector in baseVectors:
            self.__assignVector(vector)
            self.weight += vector[2]
        if len(self.data) != len(baseVectors):
            raise BranchingGraphError

    def copy(self):
        g = Graph([])
        g.data = copy.deepcopy(self.data)
        g.weight = self.weight
        return g

    def replace(self, vector):
        # for vector in vectorList:
        self.lastChange = vector
        v = self.data[vector[0]]
        self.weight += vector[2] - v[2]
        self.__assignVector(vector)

    def isValid(self):
        visited = {}
        start = next(iter(self.data))
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
