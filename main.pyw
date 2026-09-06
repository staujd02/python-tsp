from copy import deepcopy
from random import seed
from uuid import uuid4

from source.utilities.transformer import Transformer
from source.utilities.test_generator import TestGenerator
from source.utilities.graham_scan import GrahamScan
from source.utilities.exclusion_generator import ExclusionGenerator
from source.utilities.matrix_builder import MatrixBuilder

# size = 5
# headers = []
# matrix = []
# points = MatrixBuilder.populateEuclideanMatrix(matrix, size)
# print(matrix)

# thing to beat O(1.9^{n})

# Found Issue..?
# Weights are different but the solution is the same?
# ... maybe the zero graph is different
# seed(2153649) => 2 Trial in 10 Suite

seed(2553649)

# testGen.runVerificationSuite([7, 8, 9, 10], 5)

testGen = TestGenerator()
testGen.runVerificationSuite([12], 1)
# testGen.runVerificationSuite([9, 10], 10)
# testGen.runVerificationSuite([8], 100)

# testGen.runSuite([4, 5, 6, 7, 8, 9], 15)
# testGen.runIterationTest(5, 10)
# for i in range(5):
#     seed(i)
#     print("Graph:")
#     testGen.runTest(15)
#     seed(i)
#     print("Classical:")
#     testGen.runClassicalTest(15)
#     print("")


# points = [
#     [2,10,'A'],
#     [7,11,'B'],
#     [10,10,'C'],
#     [9,7,'D'],
#     [10,2,'E'],
#     [5,8,'F'],
#     [7,4,'G'],
#     [3,4,'H'],
# ]
# matrix = []
# points = MatrixBuilder.populateEuclideanMatrixFromPoints(matrix, points)
# exclusion = ExclusionGenerator.generateExclusionDictionaryDeepWebCutWithWindows(deepcopy(points))
# print(exclusion)
# testGen.runTrialWithPrepopulatedMatrix("Test Run - Size: ", [[matrix, points]], 8, testGen.runDeepWebCutTestWithWindows)
# myList = ['dog', 'cat', 'bird', 'cow']
# hullList = ['dog', 'cow']
# myList = list(filter(lambda x: x in hullList, myList))
# print(myList)
# A =  (908, 31)
# B = (968, 369)
# C = (24, 470)
# D = (16, 304)
# E = (620, 498)
# F = (703, 542)
# G = (901, 14)
# H = (662, 403)
# I = (556, 440)
 
 
# A->G->H->I->D->C->E->F->B->A

# # Bad Sol. 2
#  908, 31 
#  901, 14
#  662, 403
#  556, 440
#  16, 304
#  24, 470
#  620, 498
#  703, 542
#  968, 369 
#  908, 31 

#  {
#  'D': ['A', 'B', 'F', 'E'],
#  'G': ['B', 'F', 'C', 'E'],
#  'A': ['F', 'C', 'D', 'I', 'E'],
#  'B': ['C', 'D', 'G', 'I', 'E'],
#  'F': ['D', 'G', 'A', 'I', 'H'],
#  'C': ['G', 'A', 'B', 'H'],
#  'H': ['C', 'E', 'F'],
#  'E': ['D', 'G', 'A', 'H', 'B'],
#  'I': ['A', 'B', 'F']
#  }

#  # Right Sol. 1
#  A->G->D->C->I->E->F->H->B->A

#  908, 31 
#  901, 14
#  16, 304
#  24, 470
#  556, 440
#  620, 498
#  703, 542
#  662, 403
#  968, 369 