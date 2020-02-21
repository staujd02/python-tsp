from source.utilities.transformer import Transformer

headers = ['A', 'B', 'C', 'D', 'E']
matrix = [
    [None, 100,  250,   75,   50],
    [100,  None, 300,  175,  200],
    [250,  300,  None, 105,  125],
    [ 75,  175,  150,  None,  80],
    [ 50,  200,  125,   80,  None]
]

transformer = Transformer(matrix, headers)

vectorList = transformer.flatten(scaleDown=True, toSort=True)
# vectors = transformer.stripZeroColumnVectors(vectorList)
# columnVectors = transformer.getColumnVectors(zero=True)
# vectors = transformer.stripFirstElements(columnVectors)

for v in vectorList:
    print(str(v))
