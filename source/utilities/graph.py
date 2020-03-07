import copy

from source.dataStructures import Vector, NoOpCompare

class BranchingGraphError(Exception):
    pass

class Graph(NoOpCompare):

    def __init__(self, baseVectors, vectorList, skipSpinUp=False):
        if skipSpinUp:
            return
        self.data = []
        self.weight = 0
        self.lastChange = None
        self.vectorList = vectorList
        charList = ''
        for v in baseVectors:
            vector = vectorList[v]
            self.data.append(vector[0] + '->' + vector[1])
            self.weight += vector[2]
            if charList.find(vector[0]) == -1:
                charList += vector[0] 
            else:
                raise BranchingGraphError

    def translate(self, key):
        return ord(key) - 65

    def copy(self):
        g = Graph([], [], skipSpinUp=True)
        g.data = list(self.data)
        g.weight = self.weight
        g.lastChange = self.lastChange
        g.vectorList = self.vectorList
        return g
    
    def goAcross(self, vector, weight):
        i = self.translate(self.lastChange[0])
        oldWeight = self.vectorList[self.data[i]][2]
        self.swapOutLastChange()
        self.replace(vector)
        return  weight - oldWeight + vector[2]
    
    def swapOutLastChange(self):
        self.replace(self.vectorList[self.lastChange])

    def goDeeper(self, vector, weight):
        self.replace(vector)
        return weight + vector[2]

    def replace(self, vector):
        i = self.translate(vector[0])
        v = self.data[i]
        self.lastChange = v
        self.weight += vector[2] - self.vectorList[v][2]
        self.__assignVector(vector)

    def isValid(self):
        visited = {}
        start = self.data[0][0]
        beginning = start
        while True:
            if visited.get(start, False):
                break
            visited[start] = True
            i = self.translate(start)
            start = self.data[i][3]
        return len(visited) == len(self.data) and start == beginning

    def getWeight(self):
        return self.weight

    def toVectorListString(self):
        s = "{"
        for v in self.data:
            s += str(self.vectorList[v])
        return s + "}"

    def __assignVector(self, vector):
        i = self.translate(vector[0])
        self.data[i] = vector[0] + '->' + vector[1]

    def __str__(self):
        visited = {}
        start = self.data[0][0]
        literal = "(" + start
        while True:
            if visited.get(start, False):
                break
            literal += "->"
            visited[start] = True
            i = self.translate(start)
            start = self.data[i][3]
            literal += start
        return literal + "): " + str(self.weight)

    def __unicode__(self):
        return u"" + self.__str__()
