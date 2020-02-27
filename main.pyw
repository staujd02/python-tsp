from source.utilities.transformer import Transformer
from source.utilities.solver import Solver
from source.dataStructures import Vector
from source.utilities.graph import Graph

headers = ['A', 'B', 'C', 'D', 'E']
matrix = [
    [None, 100,  250,   75,   50],
    [100,  None, 300,  175,  200],
    [250,  300,  None, 105,  125],
    [75,  175,  150,  None,  80],
    [50,  200,  125,   80,  None]
]

transformer = Transformer(matrix, headers)

vectors = transformer.flatten(scaleDown=True, toSort=True)
# vectors = transformer.stripZeroColumnVectors(vectorList)
# columnVectors = transformer.getColumnVectors(zero=True)
# vectors = transformer.stripFirstElements(columnVectors)

(zeroVectors, vectorList) = transformer.stripZeroElements(vectors)
zeroGraph = Graph(zeroVectors)
# for v in vectorList:
#     print(str(v))

vectorGroups = Solver().solve(zeroGraph, vectorList)

for v in vectorGroups.data:
    print(vectorGroups.data[v])

print("")
print("Weight: " + str(vectorGroups.getWeight()))

# for v in vectorGroups:
#     sum = 0
#     for vx in v:
#         sum += vx[2]
#     print("[" + str(sum)  + "]")
