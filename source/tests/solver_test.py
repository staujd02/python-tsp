import unittest

from source.utilities.transformer import Transformer
from source.utilities.graph import Graph
from source.utilities.solver import Solver

from source.dataStructures import Vector

class Solver_test(unittest.TestCase):

    V = {
        "D->E": Vector('D', 'E', 5),
        "A->D": Vector('A', 'D', 25),
        "C->D": Vector('C', 'D', 25),
        "E->D": Vector('E', 'D', 30),
        "A->B": Vector('A', 'B', 50),
        "B->D": Vector('B', 'D', 75),
        "D->C": Vector('D', 'C', 75),
        "E->C": Vector('E', 'C', 75),
        "B->E": Vector('B', 'E', 100),
        "D->B": Vector('D', 'B', 100),
        "C->A": Vector('C', 'A', 125),
        "A->C": Vector('A', 'C', 150),
        "E->B": Vector('E', 'B', 150),
        "C->B": Vector('C', 'B', 175),
        "B->C": Vector('B', 'C', 200),
    }

    def test_solver_can_produce_augment_list(self):
        vectorGroups = self.solver.createAugmentList(
            self.zeroGraph, self.vectorList)
        for (i, vectors) in enumerate(self.solution):
            for (idx, v) in enumerate(vectors):
                self.vectorCompare(v, vectorGroups[i][idx])

    solution = [
        [V['D->E']],
        [V['A->D']],
        [V['C->D']],
        [
            V['D->E'],
            V['A->D'],
        ],
        [V['E->D']],
        [
            V['D->E'],
            V['C->D'],
        ],
        [
            V['E->D'],
            V['D->E'],
        ],
        [
            V['A->D'],
            V['C->D'],
        ],
        [V['A->B']]
    ]

    def vectorCompare(self, v1, v2):
        self.assertEqual(str(v1), str(v2))

    def setUp(self):
        self.headers = ['A', 'B', 'C', 'D', 'E']
        self.test = [
            [None, 100,  250,   75,   50],
            [100,  None, 300,  175,  200],
            [250,  300,  None, 150,  125],
            [75,  175,  150,  None,  80],
            [50,  200,  125,   80,  None]
        ]
        transformer = Transformer(self.test, self.headers)
        vectors = transformer.flatten(scaleDown=True, toSort=True)
        (zeroVectors, self.vectorList) = transformer.stripZeroElements(vectors)
        self.zeroGraph = Graph(zeroVectors)
        self.solver = Solver()
