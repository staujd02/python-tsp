import statistics
import time

from source.utilities.transformer import Transformer
from source.utilities.solver import Solver
from source.dataStructures import Vector
from source.utilities.graph import Graph
from source.utilities.timer import Timer

from random import seed, random
from source.utilities.matrix_builder import MatrixBuilder

class TestGenerator(object):

    headers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1', 'S1', 'T1', 'U1', 'V1', 'W1', 'X1', 'Y1', 'Z1',
    'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2', 'Q2', 'R2', 'S2', 'T2', 'U2', 'V2', 'W2', 'X2', 'Y2', 'Z2',
    'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'J3', 'K3', 'L3', 'M3', 'N3', 'O3', 'P3', 'Q3', 'R3', 'S3', 'T3', 'U3', 'V3', 'W3', 'X3', 'Y3', 'Z3']

    def runTest(self, size):
        matrix = []
        MatrixBuilder.populateEuclideanMatrix(matrix, size)
        (zeroGraph, vectorList) = Transformer(matrix, self.headers[:size]).fetchSolvePieces()
        (vList, runTime) = Timer.time("Run Time: ", lambda: Solver().solve(zeroGraph, vectorList), True)
        print(vList)
        return runTime

    def runSuite(self, trialList, iterations):
        print("Begining Trials...")
        print("=================")
        for x in trialList:
            print("Trial: " + str(x))
            print("=================")
            trials = []
            for i in range(iterations):
                trials.append(self.runTest(x))
            mean = statistics.mean(trials)
            print("Average: " + str(mean))
            print("Median: " + str(statistics.median(trials)))
            print("Variance: " + str(statistics.pvariance(trials, mean)))
            print("=================")
        print("Trials Complete.")

    def runClassicalTest(self, size):
        matrix = []
        MatrixBuilder.populateEuclideanMatrix(matrix, size)
        (zeroGraph, vectorList) = Transformer(matrix, self.headers[:size]).fetchSolvePieces()
        print(Timer.time("Run Time: ", lambda: Solver().oldSolve(zeroGraph, vectorList)))
    
    def runIterationTest(self, size, depth):
        matrix = []
        MatrixBuilder.populateEuclideanMatrix(matrix, size)
        (zeroGraph, vectorList) = Transformer(matrix, self.headers[:size]).fetchSolvePieces()
        for x in Solver().safe_createAugmentList(zeroGraph, vectorList, depth):
            w = 0
            s = '['
            for v in x:
                w += v[2]
                s += str(v)
            print(s + ']: ' + str(w))