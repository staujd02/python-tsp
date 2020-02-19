import unittest

from source.utilities.transformer import Transformer
from source.dataStructures import Vector

class Transformer_test(unittest.TestCase):

    def test_transformer_can_sort_and_reduce(self):
        vectors = self.transformer.getColumnVectors()
        for (idx, v) in enumerate([Vector('A', 'E', 50), Vector('A', 'D', 75), Vector('A', 'B', 100), Vector('A', 'C', 250)]):
            v.isEqual(vectors[0][idx])
        self.assertEqual([ ['A', 'E', 50], ['A', 'D', 75], ['A', 'B', 100], ['A', 'C', 250]], vectors[0])
        self.assertEqual([ ['B', 'A', 100], ['B', 'D', 175], ['B', 'E', 200], ['B', 'C', 300]], vectors[1])
        self.assertEqual([ ['C', 'E', 125], ['C', 'D', 150], ['C', 'A', 250], ['C', 'B', 300]], vectors[2])
        self.assertEqual([ ['D', 'A', 75], ['D', 'E', 80], ['D', 'C', 150], ['D', 'B', 175]], vectors[3])
        self.assertEqual([ ['E', 'A', 50], ['E', 'D', 80], ['E', 'C', 125], ['E', 'B', 200]], vectors[4])

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
