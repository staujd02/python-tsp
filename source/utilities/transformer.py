from source.dataStructures import Vector

class Transformer(object):

    def __init__(self, matrix, matrixHeaders):
        self.matrix = matrix
        self.headers = matrixHeaders

    def getColumnVectors(self):
        buckets = []
        for (idx, header) in enumerate(self.headers):
            buckets.append(self.__createVector(idx, header))
        return buckets
        
    @staticmethod
    def sortThird(val): 
        return val[2] 

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
