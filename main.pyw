from random import seed

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
# testGen.runIterationTest(5, 10)
# for i in range(5):
#     seed(i)
#     print("Graph:")
#     testGen.runTest(15)
#     seed(i)
#     print("Classical:")
#     testGen.runClassicalTest(15)
#     print("")
testGen.runVerificationSuite([9, 10], 5)

# myList = ['dog', 'cat', 'bird', 'cow']
# hullList = ['dog', 'cow']
# myList = list(filter(lambda x: x in hullList, myList))
# print(myList)
