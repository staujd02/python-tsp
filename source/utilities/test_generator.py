import statistics
import time
import string
from copy import deepcopy

from source.utilities.transformer import Transformer
from source.utilities.solver import Solver
from source.dataStructures import Vector
from source.utilities.graph import Graph
from source.utilities.timer import Timer
from source.utilities.graham_scan import GrahamScan
from source.utilities.exclusion_generator import ExclusionGenerator

from random import seed, random
from source.utilities.matrix_builder import MatrixBuilder

class TestGenerator(object):
    runningExclusion = False
    runningTestExclusion = False

    def runTest(self, size, matrix, points):
        if self.runningExclusion:
            if self.runningTestExclusion:
                exclusionList = ExclusionGenerator.generateExclusionDictionaryTrials(points)
            else:
                hullList = GrahamScan.getConvexHull(points)
                exclusionList = ExclusionGenerator.generateExclusionDictionary(hullList)
        else:
            exclusionList = {}
        (zeroGraph, vectorList) = Transformer(matrix, self.getHeaders(size), exclusionList).fetchSolvePieces()
        (vList, runTime) = Timer.time("Run Time: ", lambda: Solver().solve(zeroGraph, vectorList), True)
        # print(vList)
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
    
    def runSuite(self, trialList, iterations):
        print("Begining Trials...")
        print("=================")
        for x in trialList:
            print("Trial: " + str(x))
            print("=================")
            trials = []
            for i in range(iterations):
                matrix = []
                points = MatrixBuilder.populateEuclideanMatrix(matrix, x)
                trials.append(self.runTest(x, matrix, points))
            self.printStats(trials)
            print("=================")
        print("Trials Complete.")

    def runVerificationSuite(self, trialList, iterations):
        print("Begining Trials...")
        for x in trialList:
            matrixesWithPoints = []
            for i in range(iterations):
                matrix = []
                points = MatrixBuilder.populateEuclideanMatrix(matrix, x)
                matrixesWithPoints.append([matrix, points])

            self.runningExclusion = True
            self.runningTestExclusion = False
            self.runTrialWithPrepopulatedMatrix("Trial With Outer Hull Elimination: ", matrixesWithPoints, x)

            self.runningExclusion = True
            self.runningTestExclusion = True
            self.runTrialWithPrepopulatedMatrix("Trial With Expansive Hull Elimination: ", matrixesWithPoints, x)
           
            self.runningExclusion = False
            self.runTrialWithPrepopulatedMatrix("Trial With No Hull Elimination: ", matrixesWithPoints, x)
        print("=================")
        print("Trials Complete.")

    def runTrialWithPrepopulatedMatrix(self, title, matrixesWithPoints, size):
        print("=================")
        print(title + str(size))
        print("=================")
        trials = []
        for [matrix, points] in matrixesWithPoints:
            trials.append(self.runTest(size, matrix, points))
        self.printStats(trials)
        
    def printStats(self, trials):
        mean = statistics.mean(trials)
        print("Average: " + str(mean))
        print("Median: " + str(statistics.median(trials)))
        print("Variance: " + str(statistics.pvariance(trials, mean)))
    