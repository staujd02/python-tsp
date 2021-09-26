import statistics
import time
import string

from source.utilities.transformer import Transformer
from source.utilities.solver import Solver
from source.dataStructures import Vector
from source.utilities.graph import Graph
from source.utilities.timer import Timer
from source.utilities.graham_scan import GrahamScan

from random import seed, random
from source.utilities.matrix_builder import MatrixBuilder

class TestGenerator(object):

    def runTest(self, size):
        matrix = []
        points = MatrixBuilder.populateEuclideanMatrix(matrix, size)
        hullList = GrahamScan.getConvexHull(points)
        (zeroGraph, vectorList) = Transformer(matrix, self.getHeaders(size), hullList).fetchSolvePieces()
        (vList, runTime) = Timer.time("Run Time: ", lambda: Solver().solve(zeroGraph, vectorList), True)
        print(vList)
        return runTime
    
    @staticmethod
    def getHeaders(size):
        headers = []
        alphabet = list(string.ascii_uppercase)
        lastIndex = len(alphabet)
        for (idx, value) in enumerate(range(1, size + 1)):
            if value <= lastIndex:
                headers.append(alphabet[idx])
            else:
                headers.append(alphabet[idx % lastIndex] + str(idx // lastIndex))
        return headers

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