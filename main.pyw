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

seed(5)
testGen = TestGenerator()
# testGen.runTest(10)
testGen.runSuite([8,9], 5)
# testGen.runIterationTest(5, 10)
# for i in range(5):
#     seed(i)
#     print("Graph:")
#     testGen.runTest(15)
#     seed(i)
#     print("Classical:")
#     testGen.runClassicalTest(15)
#     print("")
# testGen.runVerificationSuite([9, 10], 5)


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
# testGen.runTrialWithPrepopulatedMatrix("Test Run - Size: ", [[matrix, points]], 8)
# myList = ['dog', 'cat', 'bird', 'cow']
# hullList = ['dog', 'cow']
# myList = list(filter(lambda x: x in hullList, myList))
# print(myList)
