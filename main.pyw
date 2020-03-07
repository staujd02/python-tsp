from random import seed

from source.utilities.test_generator import TestGenerator

testGen = TestGenerator()

# seed(5)
# testGen.runIterationTest(5, 100)
# for i in range(5):
#     seed(i)
#     print("Graph:")
#     testGen.runTest(9)
#     seed(i)
#     print("Classical:")
#     testGen.runClassicalTest(9)
#     print("")

testGen.runSuite([7, 8], 4)