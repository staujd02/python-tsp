from math import ceil, sqrt
from random import random
from uuid import uuid4

class MatrixBuilder(object):
    
    @staticmethod
    def populateEuclideanMatrix(matrix, size):
        points = []
        for i in range(size):
            points.append([MatrixBuilder.getRand(0, 1000), MatrixBuilder.getRand(0, 1000), uuid4()])
        for (idx, point1) in enumerate(points):
            row = []
            for (jdx, point2) in enumerate(points):
                if idx == jdx:
                    row.append(None)
                else:
                    row.append([MatrixBuilder.calculateDistance(point1[0], point1[1], point2[0], point2[1]), point1[2], point2[2]])
            matrix.append(row)
        return points 

    @staticmethod
    def populateRandomMatrix(matrix, size):
        for row in range(size):
            matrix.append([])
            for column in range(size):
                if row == column:
                    matrix[row].append(None)
                else:
                    value = min + (random() * (max - min))
                    matrix[row].append(ceil(value))

    @staticmethod
    def calculateDistance(x1,y1,x2,y2):  
        dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return ceil(dist)

    @staticmethod
    def getRand(min, max):
        value = min + (random() * (max - min))
        return ceil(value)