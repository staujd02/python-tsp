from random import seed

from source.utilities.test_generator import TestGenerator

testGen = TestGenerator()

for i in range(5):
    seed(i)
    testGen.runTest(9)
    print("")
# runSuite([7], 1)

# print("Weight: " + str(vectorGroups.getWeight()))

# for v in vectorGroups:
#     sum = 0
#     for vx in v:
#         sum += vx[2]
#     print("[" + str(sum)  + "]")
