import unittest

from source.utilities.transformer import Transformer
from source.dataStructures import Vector

class Transformer_test(unittest.TestCase):

    def vectorCompare(self, v1, v2):
        self.assertEqual(str(v1), str(v2))
    
    def vectorKeyCompare(self, vKey, vVal):
        self.assertEqual(vKey, vVal[0] + '->' + vVal[1])

    V = {
        'A->E': Vector('A', 'E', 0),
        'B->A': Vector('B', 'A', 0),
        'C->E': Vector('C', 'E', 0),
        'D->A': Vector('D', 'A', 0), 
        'E->A': Vector('E', 'A', 0)
    }
    
    def test_transformer_prepare_matrix_for_solving(self):
        (zeroVectors, remaining) = self.transformer.fetchSolvePieces()
        for (idx, v) in enumerate([Vector('A', 'E', 0), Vector('B', 'A', 0), Vector('C', 'E', 0), Vector('D', 'A', 0), Vector('E', 'A', 0)]):
            self.vectorKeyCompare(zeroVectors.graphData[idx], v)
        for (idx, v) in enumerate([
            Vector('D','E', 5),
            Vector('C','D', 25),
            Vector('A','D', 25),
            Vector('E','D', 30),
            Vector('A','B', 50),
            Vector('E','C', 75),
            Vector('D','C', 75),
            Vector('B','D', 75),
            Vector('D','B', 100),
            Vector('B','E', 100),
            Vector('C','A', 125),
            Vector('E','B', 150),
            Vector('C','B', 175),
            Vector('B', 'C', 200),
            Vector('A', 'C', 200)
        ]):
            self.vectorCompare(v, remaining[idx])

    def test_transformer_can_strip_zero_vectors(self):
        columnVectors = self.transformer.flatten(scaleDown=True,toSort=True)
        (zeroVectors, remaining) = self.transformer.stripZeroElements(columnVectors)
        for (idx, v) in enumerate([Vector('A', 'E', 0), Vector('B', 'A', 0), Vector('C', 'E', 0), Vector('D', 'A', 0), Vector('E', 'A', 0)]):
            self.vectorCompare(v, zeroVectors[idx])
        for (idx, v) in enumerate([
            Vector('D','E', 5),
            Vector('A','D', 25),
            Vector('C','D', 25),
            Vector('E','D', 30),
            Vector('A','B', 50),
            Vector('B','D', 75),
            Vector('D','C', 75),
            Vector('E','C', 75),
            Vector('B','E', 100),
            Vector('D','B', 100),
            Vector('C','A', 125),
            Vector('E','B', 150),
            Vector('C','B', 175),
            Vector('A', 'C', 200),
            Vector('B', 'C', 200)
        ]):
            self.vectorCompare(v, remaining[idx])

    def test_transformer_can_strip_first_indices_off_of_vector_groups(self):
        columnVectors = self.transformer.getColumnVectors(zero=True)
        vectors = self.transformer.stripFirstElements(columnVectors)
        for (idx, v) in enumerate([Vector('A', 'E', 0), Vector('B', 'A', 0), Vector('C', 'E', 0), Vector('D', 'A', 0), Vector('E', 'A', 0)]):
            self.vectorCompare(v, vectors[idx])

    def test_transformer_can_sort_vector_lists(self):
        vectors = self.transformer.flatten(toSort=True)
        for (idx, v) in enumerate([
            Vector('A', 'E', 50), Vector('E', 'A', 50), Vector(
                'A', 'D', 75), Vector('D', 'A', 75), Vector('D', 'E', 80),
            Vector('E', 'D', 80), Vector('A', 'B', 100), Vector(
                'B', 'A', 100), Vector('C', 'E', 125), Vector('E', 'C', 125),
            Vector('C', 'D', 150), Vector('D', 'C', 150), Vector(
                'B', 'D', 175), Vector('D', 'B', 175), Vector('B', 'E', 200),
            Vector('E', 'B', 200), Vector('A', 'C', 250), Vector(
                'C', 'A', 250), Vector('B', 'C', 300), Vector('C', 'B', 300)
        ]):
            self.vectorCompare(v, vectors[idx])

    def test_transformer_can_flatten(self):
        vectors = self.transformer.flatten()
        for (idx, v) in enumerate([
            Vector('A', 'E', 50), Vector('A', 'D', 75), Vector(
                'A', 'B', 100), Vector('A', 'C', 250),
            Vector('B', 'A', 100), Vector('B', 'D', 175), Vector(
                'B', 'E', 200), Vector('B', 'C', 300),
            Vector('C', 'E', 125), Vector('C', 'D', 150), Vector(
                'C', 'A', 250), Vector('C', 'B', 300),
            Vector('D', 'A', 75), Vector('D', 'E', 80), Vector(
                'D', 'C', 150), Vector('D', 'B', 175),
            Vector('E', 'A', 50), Vector('E', 'D', 80), Vector(
                'E', 'C', 125), Vector('E', 'B', 200)
        ]):
            self.assertTrue(v.isEqual(vectors[idx]))

    def test_transformer_can_zero_out_columns(self):
        vectors = self.transformer.getColumnVectors(zero=True)
        for (idx, v) in enumerate([Vector('A', 'E', 0), Vector('A', 'D', 25), Vector('A', 'B', 50), Vector('A', 'C', 200)]):
            self.vectorCompare(v, vectors[0][idx])
        for (idx, v) in enumerate([Vector('B', 'A', 0), Vector('B', 'D', 75), Vector('B', 'E', 100), Vector('B', 'C', 200)]):
            self.vectorCompare(v, vectors[1][idx])
        for (idx, v) in enumerate([Vector('C', 'E', 0), Vector('C', 'D', 25), Vector('C', 'A', 125), Vector('C', 'B', 175)]):
            self.vectorCompare(v, vectors[2][idx])
        for (idx, v) in enumerate([Vector('D', 'A', 0), Vector('D', 'E', 5), Vector('D', 'C', 75), Vector('D', 'B', 100)]):
            self.vectorCompare(v, vectors[3][idx])
        for (idx, v) in enumerate([Vector('E', 'A', 0), Vector('E', 'D', 30), Vector('E', 'C', 75), Vector('E', 'B', 150)]):
            self.vectorCompare(v, vectors[4][idx])

    def test_transformer_can_sort_and_reduce(self):
        vectors = self.transformer.getColumnVectors()
        for (idx, v) in enumerate([Vector('A', 'E', 50), Vector('A', 'D', 75), Vector('A', 'B', 100), Vector('A', 'C', 250)]):
            self.assertTrue(v.isEqual(vectors[0][idx]))
        for (idx, v) in enumerate([Vector('B', 'A', 100), Vector('B', 'D', 175), Vector('B', 'E', 200), Vector('B', 'C', 300)]):
            self.assertTrue(v.isEqual(vectors[1][idx]))
        for (idx, v) in enumerate([Vector('C', 'E', 125), Vector('C', 'D', 150), Vector('C', 'A', 250), Vector('C', 'B', 300)]):
            self.assertTrue(v.isEqual(vectors[2][idx]))
        for (idx, v) in enumerate([Vector('D', 'A', 75), Vector('D', 'E', 80), Vector('D', 'C', 150), Vector('D', 'B', 175)]):
            self.assertTrue(v.isEqual(vectors[3][idx]))
        for (idx, v) in enumerate([Vector('E', 'A', 50), Vector('E', 'D', 80), Vector('E', 'C', 125), Vector('E', 'B', 200)]):
            self.assertTrue(v.isEqual(vectors[4][idx]))

    def setUp(self):
        self.headers = ['A', 'B', 'C', 'D', 'E']
        self.test = [
            [['A', 'A', None], ['A', 'B',  100], ['A', 'C',  250], ['A', 'D',   75],  ['A', 'E',   50]],
            [['B', 'A',  100], ['B', 'B', None], ['B', 'C',  300], ['B', 'D',  175],  ['B', 'E',  200]],
            [['C', 'A',  250], ['C', 'B',  300], ['C', 'C', None], ['C', 'D',  150],  ['C', 'E',  125]],
            [['D', 'A',   75], ['D', 'B',  175], ['D', 'C',  150], ['D', 'D', None],  ['D', 'E',   80]],
            [['E', 'A',   50], ['E', 'B',  200], ['E', 'C',  125], ['E', 'D',   80],  ['E', 'E', None]]
        ]
        # This lambda needs fixed:
        self.test = list(map(lambda t: list(map(lambda r: None if r == None else [r, 'Ignore'], t)), self.test))
        self.transformer = Transformer(self.test, self.headers, {'Ignore': []})
