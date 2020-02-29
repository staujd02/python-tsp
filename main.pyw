import time
import statistics

from random import seed, random
from math import ceil, sqrt

from source.utilities.transformer import Transformer
from source.utilities.solver import Solver
from source.dataStructures import Vector
from source.utilities.graph import Graph

headers = ['A', 'B', 'C', 'D', 'E']
matrix = [
    [None, 100,  250,   75,   50],
    [100,  None, 300,  175,  200],
    [250,  300,  None, 105,  125],
    [75,  175,  150,  None,  80],
    [50,  200,  125,   80,  None]
]
min = 20
max = 1000
headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
  'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1', 'S1', 'T1', 'U1', 'V1', 'W1', 'X1', 'Y1', 'Z1',
  'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2', 'Q2', 'R2', 'S2', 'T2', 'U2', 'V2', 'W2', 'X2', 'Y2', 'Z2',
  'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3', 'K3', 'L3', 'M3', 'N3', 'O3', 'P3', 'Q3', 'R3', 'S3', 'T3', 'U3', 'V3', 'W3', 'X3', 'Y3', 'Z3']

def populateRandomMatrix(matrix, size):
    for row in range(size):
        matrix.append([])
        for column in range(size):
            if row == column:
                matrix[row].append(None)
            else:
                value = min + (random() * (max - min))
                matrix[row].append(ceil(value))

def calculateDistance(x1,y1,x2,y2):  
     dist = sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return ceil(dist)

def getRand(min, max):
    value = min + (random() * (max - min))
    return ceil(value)

def populateEuclideanMatrix(matrix, size):
    points = []
    for i in range(size):
        points.append([getRand(0, 1000), getRand(0, 1000)])
    for (idx, point1) in enumerate(points):
        row = []
        for (jdx, point2) in enumerate(points):
            if idx == jdx:
                row.append(None)
            else:
                row.append(calculateDistance(point1[0], point1[1], point2[0], point2[1]))
        matrix.append(row)


def runTest(size):
    matrix = []
    start = time.time()
    populateEuclideanMatrix(matrix, size)
    end = time.time()
    (zeroGraph, vectorList) = Transformer(matrix, headers[:size]).fetchSolvePieces()
    start = time.time()
    vectorGroups = Solver().solve(zeroGraph, vectorList)
    end = time.time()
    # print("Run Time: " + str(end - start))
    # print(vectorGroups)
    # print("")
    return end - start

def runSuite(trialList, iterations):
    print("Begining Trials...")
    print("=================")
    for x in trialList:
        print("Trial: " + str(x))
        print("=================")
        trials = []
        for i in range(iterations):
            trials.append(runTest(x))
        mean = statistics.mean(trials)
        print("Average: " + str(mean))
        print("Median: " + str(statistics.median(trials)))
        print("Variance: " + str(statistics.pvariance(trials, mean)))
        print("=================")
    print("Trials Complete.")

# runTest(10)
runSuite([4,5,6,7,8,9], 10)

# print("Weight: " + str(vectorGroups.getWeight()))

# for v in vectorGroups:
#     sum = 0
#     for vx in v:
#         sum += vx[2]
#     print("[" + str(sum)  + "]")
