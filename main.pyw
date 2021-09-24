from random import seed

from source.utilities.test_generator import TestGenerator

testGen = TestGenerator()
testGen.runTest(15)
# seed(5)
# testGen.runIterationTest(5, 100)
# for i in range(5):
#     seed(i)
#     print("Graph:")
#     testGen.runTest(15)
#     seed(i)
#     print("Classical:")
#     testGen.runClassicalTest(15)
#     print("")

# testGen.runSuite([7, 8], 4)