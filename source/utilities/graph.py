
from source.utilities.graphStringMuxer import GraphStringMuxer
from source.utilities.trajectoryCounts import TrajectoryCounts
from typing import List
from source.dataStructures import NoOpCompare, Vector

class BranchingGraphError(Exception):
    pass

class Graph(NoOpCompare):

    def __init__(self, graphVectors: List[Vector], vectorList: List[Vector], skipSpinUp=False):
        if skipSpinUp:
            return
        self.graphData = []
        self.weight = 0
        self.offendingIndex = 0
        self.lastChange = None
        self.vectorList = vectorList
        # self.trajectoryRegister = TrajectoryCounts.fillRegister(graphVectors)
        charList = ''
        for v in graphVectors:
            vector = vectorList[v]
            self.graphData.append(self.toKey(vector))
            self.weight += vector[2]
            if charList.find(vector[0]) == -1:
                charList += vector[0] 
            else:
                raise BranchingGraphError

    def copy(self):
        g = Graph([], [], skipSpinUp=True)
        g.graphData = list(self.graphData)
        g.weight = self.weight
        g.lastChange = self.lastChange
        g.vectorList = self.vectorList
        # g.trajectoryRegister = self.trajectoryRegister
        g.offendingIndex = self.offendingIndex
        return g
    
    def goAcross(self, vector: Vector, weight: int) -> int:
        i = GraphStringMuxer.translate(self.lastChange[0])
        oldWeight = self.vectorList[self.graphData[i]][2]
        self.swapOutLastChange()
        self.replace(vector)
        return  weight - oldWeight + vector[2]
    
    def swapOutLastChange(self) -> None:
        self.replace(self.vectorList[self.lastChange])

    def goDeeper(self, vector, weight) -> int:
        self.replace(vector)
        return weight + vector[2]

    def replace(self, vector) -> None:
        i = GraphStringMuxer.translate(vector[0])
        v = self.graphData[i]
        self.lastChange = v
        self.weight += vector[2] - self.vectorList[v][2]
        # self.trajectoryRegister = TrajectoryCounts.createDeltaRegister(self.trajectoryRegister, v, vector)
        self.__assignVector(vector)

    def isValid(self) -> bool:
        # [consistent, offendingIndex] = TrajectoryCounts.demonstratesConsistency(self.trajectoryRegister)
        # self.offendingIndex = offendingIndex
        # if not consistent:
        #     return False
        visited = {}
        start = self.graphData[0][0]
        beginning = start
        while True:
            if visited.get(start, False):
                break
            visited[start] = True
            i = GraphStringMuxer.translate(start)
            start = self.graphData[i][3]
        return len(visited) == len(self.graphData) and start == beginning

    def getWeight(self):
        return self.weight

    def toVectorListString(self):
        s = "{"
        for v in self.graphData:
            s += str(self.vectorList[v])
        return s + "}"

    def __assignVector(self, vector):
        i = GraphStringMuxer.translate(vector[0])
        self.graphData[i] = self.toKey(vector)

    def __str__(self):
        visited = {}
        start = self.graphData[0][0]
        literal = "(" + start
        while True:
            if visited.get(start, False):
                break
            literal += GraphStringMuxer.arrowString
            visited[start] = True
            i = GraphStringMuxer.translate(start)
            start = self.destintationAt(i)
            literal += start
        return literal + "): " + str(self.weight)

    def __unicode__(self):
        return u"" + self.__str__()

    def toKey(self, v: Vector) -> str:
        return v[0] + GraphStringMuxer.arrowString + v[1]

    def destintationAt(self, i: int) -> str:
        return GraphStringMuxer.destintationCharacter(self.graphData[i])