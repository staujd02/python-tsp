from source.dataStructures import Vector

class Transformer(object):

    def __init__(self, matrix, matrixHeaders):
        self.matrix = matrix
        self.headers = matrixHeaders

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
    
    def flatten(self, toSort=False):
        masterList = []
        for row in self.getColumnVectors():
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
                    vector.append(Vector(header, self.headers[rowIdx], val))
    
    @staticmethod
    def sortThird(val): 
        return val[2] 

