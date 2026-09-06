import statistics
import time
import string
from copy import deepcopy

from source.benchmarks.numpy_solver import solve_opttour
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
        (vList, runTime) = Timer.get_timed_result("Run Time: ", lambda: Solver().solve(zeroGraph, vectorList))
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
        return self.createTest(matrix, points, lambda pts: ExclusionGenerator.generateExclusionDictionary(
            GrahamScan.getConvexHull(pts)))

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
        print(Timer.time_execution("Run Time: ", lambda: Solver().oldSolve(zeroGraph, vectorList)))

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
        print("Preparing Trials...")
        trials = []
        for size_of_matrix in trialList:
            matrices_with_points = []
            for _ in range(iterations):
                matrix = []
                points = MatrixBuilder.populateEuclideanMatrix(matrix, size_of_matrix)
                matrices_with_points.append([matrix, points])
                solve_opttour(matrix, size_of_matrix)
            trials.append([matrices_with_points, size_of_matrix])
        print("Running Trials...")
        for [matrix, n] in trials:
            # self.runTrialWithPrepopulatedMatrix("Trial With No Hull Elimination: ", matrix, n, self.runTest)
            self.runTrialWithPrepopulatedMatrix("Trial With No Hull Elimination: ", matrix, n, self.runTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Outside Hull Elimination: ", matrix, n,
            #                                     self.runTestBasicExclusionTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Inner Rings Hull Elimination: ", t, n,
            #                                     self.runTestInnerRingsExclusionTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Deep Elimination: ", t, n, self.runDeepCutTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Deep Web Elimination: ", t, n, self.runDeepWebCutTest)
            # self.runTrialWithPrepopulatedMatrix("Trial With Deep Web Window Elimination: ", t, n,
            #                                     self.runDeepWebCutTestWithWindows)
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
