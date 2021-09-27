from source.dataStructures import Vector
from source.utilities.graph import Graph

import heapq

class Transformer(object):

    def __init__(self, matrix, matrixHeaders, exclusionList):
        self.matrix = matrix
        self.headers = matrixHeaders
        self.exclusionList = exclusionList 

    def __excluded(self, val):
        return False
        # if val[1] in self.exclusionList.keys():
        #     return val[2] in self.exclusionList[val[1]]
        # elif val[2] in self.exclusionList.keys():
        #     return val[1] in self.exclusionList[val[2]]
        # else:
        #     False

    def fetchSolvePieces(self):
        zeroVectors = []
        vectorHeap = []
        vectorDict = {}
        heapq.heapify(vectorHeap)
        for (idx, header) in enumerate(self.headers):
            column = []
            for rowIdx in range(0, len(self.matrix)):
                val = self.matrix[rowIdx][idx]
                if val is not None and not self.__excluded(val):
                    column.append(Vector(header, self.headers[rowIdx], val[0]))
            column.sort(key=self.sortThird)
            v = column.pop(0)
            scale = v[2]
            v[2] = 0
            key = self.getKey(v)
            zeroVectors.append(key)
            self.pushVectorIntoDict(vectorDict, key, v)
            for c in column:
                c.data[2] = c.data[2] - scale
                heapq.heappush(vectorHeap, c)
                key = self.getKey(c)
                self.pushVectorIntoDict(vectorDict, key, c)
        vectorList = []
        try:
            while True:
                v = heapq.heappop(vectorHeap)
                vectorList.append(v)        
        except:
            pass
        return (Graph(zeroVectors, vectorDict), vectorList)

    def pushVectorIntoDict(self, dict, key, v):
        dict[key] = v

    def getKey(self, v):
        return v[0] + '->' + v[1]
    
    def stripZeroElements(self, vectors):
        zero = []
        i = 0
        for vector in vectors:
            if vector[2] == 0:
                zero.append(vector)
                i += 1
            else:
                break
        return (zero, vectors[i:]) 

    def stripFirstElements(self, zeroedBuckets):
        l = []
        for vectorList in zeroedBuckets:
            l.append(vectorList[0])
        return l

    def getColumnVectors(self, zero=False):
        buckets = []
        for (idx, header) in enumerate(self.headers):
            buckets.append(self.__createVector(idx, header))
        return self.__zero(buckets, zero)
    
    def __zero(self, buckets, zero):
        if zero is True:
            self.__scaleVectors(buckets)
        return buckets
    
    def __scaleVectors(self, buckets):
        for row in buckets:
            subtraction = int(row[0][2])
            for vector in row:
                vector[2] = vector[2] - subtraction
    
    def flatten(self, toSort=False, scaleDown=False):
        masterList = []
        for row in self.getColumnVectors(zero=scaleDown):
            for item in row:
                masterList.append(item)
        return self.__sort(masterList, toSort)
    
    def __sort(self, masterList, toSort):
        if toSort is True:
            masterList.sort(key=self.sortThird)
        return masterList
        
    def __createVector(self, columnIdx, header):
        vector = []
        self.__invert(vector, columnIdx, header)
        vector.sort(key=self.sortThird)
        return vector
    
    def __invert(self, vector, columnIdx, header):
            for rowIdx in range(0, len(self.matrix)):
                val = self.matrix[rowIdx][columnIdx]
                if val is not None:
                    vector.append(Vector(header, self.headers[rowIdx], val[0]))
    
    @staticmethod
    def sortThird(val): 
        return val[2] 

