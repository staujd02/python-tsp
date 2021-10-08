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
    
    def createTest(self, matrix, points, exclusionGenerator):
        exclusionList = exclusionGenerator(points)
        (zeroGraph, vectorList) = Transformer(matrix, self.getHeaders(len(points)), exclusionList).fetchSolvePieces()
        (vList, runTime) = Timer.time("Run Time: ", lambda: Solver().solve(zeroGraph, vectorList), True)
        print(vList)
        return runTime
    
    def runDeepWebCutTestWithWindows(self, matrix, points):
        return self.createTest(matrix, points, ExclusionGenerator.generateExclusionDictionaryDeepWebCutWithWindows)
    
    def runDeepWebCutTest(self, matrix, points):
        return self.createTest(matrix, points, ExclusionGenerator.generateExclusionDictionaryDeepWebCut)
    
    def runDeepCutTest(self, matrix, points):
        return self.createTest(matrix, points, ExclusionGenerator.generateExclusionsWithDeepCutsAroundHullRings)

    def runTestInnerRingsExclusionTest(self, matrix, points):
        return self.createTest(matrix, points, ExclusionGenerator.generateExclusionsByHullRings)
    
    def runTestBasicExclusionTest(self, matrix, points):
        return self.createTest(matrix, points, lambda pts: ExclusionGenerator.generateExclusionDictionary(GrahamScan.getConvexHull(pts)))
    
    def runTest(self, matrix, points):
        return self.createTest(matrix, points, lambda _: {})

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
                trials.append(self.runDeepCutTest(x, matrix, points))
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
            # self.runTrialWithPrepopulatedMatrix("Trial With No Hull Elimination: ", matrixesWithPoints, x, self.runTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Outside Hull Elimination: ", matrixesWithPoints, x, self.runTestBasicExclusionTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Inner Rings Hull Elimination: ", matrixesWithPoints, x, self.runTestInnerRingsExclusionTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Deep Elimination: ", matrixesWithPoints, x, self.runDeepCutTest)
            self.runTrialWithPrepopulatedMatrix("Trial With Deep Web Elimination: ", matrixesWithPoints, x, self.runDeepWebCutTest)
            self.runTrialWithPrepopulatedMatrix("Trial With Deep Web Window Elimination: ", matrixesWithPoints, x, self.runDeepWebCutTestWithWindows)
        print("=================")
        print("Trials Complete.")

    def runTrialWithPrepopulatedMatrix(self, title, matrixesWithPoints, size, test):
        print("=================")
        print(title + str(size))
        print("=================")
        trials = []
        for [matrix, points] in matrixesWithPoints:
            trials.append(test(matrix, points))
        self.printStats(trials)
        
    def printStats(self, trials):
        mean = statistics.mean(trials)
        print("Average: " + str(mean))
        print("Median: " + str(statistics.median(trials)))
        print("Variance: " + str(statistics.pvariance(trials, mean)))
    