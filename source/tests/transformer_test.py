import unittest

from source.utilities.transformer import Transformer
from source.dataStructures import Vector


class Transformer_test(unittest.TestCase):
    
    def test_transformer_can_sort_vector_lists(self):
        vectors = self.transformer.flatten(toSort=True)
        for (idx, v) in enumerate([
            Vector('A', 'E', 50), 
            Vector('E', 'A', 50), 
            Vector('A', 'D', 75),
            Vector('D', 'A', 75), 
            Vector('D', 'E', 80), 
            Vector('E', 'D', 80), 
            Vector('A', 'B', 100),
            Vector('B', 'A', 100),
            Vector('C', 'E', 125), 
            Vector('E', 'C', 125), 
            Vector('C', 'D', 150), 
            Vector('D', 'C', 150), 
            Vector('B', 'D', 175), 
            Vector('D', 'B', 175),
            Vector('B', 'E', 200), 
            Vector('E', 'B', 200),
            Vector('A', 'C', 250),
            Vector('C', 'A', 250), 
            Vector('B', 'C', 300),
            Vector('C', 'B', 300)
            ]):
            self.assertEqual(v[0], vectors[idx][0])
            self.assertEqual(v[1], vectors[idx][1])
            self.assertEqual(v[2], vectors[idx][2])
    
    def test_transformer_can_flatten(self):
        vectors = self.transformer.flatten()
        for (idx, v) in enumerate([
            Vector('A', 'E', 50), Vector('A', 'D', 75), Vector('A', 'B', 100), Vector('A', 'C', 250),
            Vector('B', 'A', 100), Vector('B', 'D', 175), Vector('B', 'E', 200), Vector('B', 'C', 300),
            Vector('C', 'E', 125), Vector('C', 'D', 150), Vector('C', 'A', 250), Vector('C', 'B', 300),
            Vector('D', 'A', 75), Vector('D', 'E', 80), Vector('D', 'C', 150), Vector('D', 'B', 175),
            Vector('E', 'A', 50), Vector('E', 'D', 80), Vector( 'E', 'C', 125), Vector('E', 'B', 200)
            ]):
            self.assertTrue(v.isEqual(vectors[idx]))

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
        for (idx, v) in enumerate([Vector('E', 'A', 50), Vector('E', 'D', 80), Vector( 'E', 'C', 125), Vector('E', 'B', 200)]):
            self.assertTrue(v.isEqual(vectors[4][idx]))

    def setUp(self):
        self.headers = ['A', 'B', 'C', 'D', 'E']
        self.test = [
            [None, 100,  250,   75,   50],
            [100,  None, 300,  175,  200],
            [250,  300,  None, 150,  125],
            [75,  175,  150,  None,  80],
            [50,  200,  125,   80,  None]
        ]
        self.transformer = Transformer(self.test, self.headers)
