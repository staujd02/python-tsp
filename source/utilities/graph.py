import copy

from source.dataStructures import Vector, NoOpCompare

class BranchingGraphError(Exception):
   pass

class Graph(NoOpCompare):

    def __init__(self, baseVectors):
        self.data = {}
        self.weight = 0
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
    
    def replace(self, vectorList):
        for vector in vectorList:
            v = self.data[vector[0]]
            self.weight += vector[2] - v[2]
            self.__assignVector(vector)

    def isValid(self):
        destinaton = {}
        for check in iter(self.data):
            destinaton[self.data[check][1]] = True
        return len(destinaton) == len(self.data)

    def getWeight(self):
        return self.weight
        
    def __assignVector(self, vector):
        self.data[vector[0]] = vector
    
    def __str__(self):
        literal = "("
        for vector in iter(self.data):
            v = self.data[vector]
            literal += v[0] + "->"
            lastV = v
        return  literal + lastV[1] + "): " + str(self.weight)

    def __unicode__(self):
        return  u"" + self.__str__()