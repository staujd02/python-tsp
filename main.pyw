from random import seed

from source.utilities.transformer import Transformer
from source.utilities.test_generator import TestGenerator
from source.utilities.graham_scan import GrahamScan
from source.utilities.exclusion_generator import ExclusionGenerator 
from source.utilities.matrix_builder import MatrixBuilder

size = 5
headers = []
matrix = []
points = MatrixBuilder.populateEuclideanMatrix(matrix, size)
hullList = GrahamScan.getConvexHull(points)
exclusionList = ExclusionGenerator.generateExclusionList(hullList)
print(exclusionList)

# testGen = TestGenerator()
# testGen.runTest(10)
# seed(5)
# testGen.runIterationTest(5, 10)
# for i in range(5):
#     seed(i)
#     print("Graph:")
#     testGen.runTest(15)
#     seed(i)
#     print("Classical:")
#     testGen.runClassicalTest(15)
#     print("")

# testGen.runSuite([4, 5, 6], 4)