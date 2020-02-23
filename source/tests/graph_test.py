import unittest

from source.utilities.solver import Solver
from source.utilities.graph import Graph
from source.utilities.graph import BranchingGraphError

from source.dataStructures import Vector

class Graph_test(unittest.TestCase):

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
    
    def test_a_graph_returns_none_when_constructed_with_duplicate_origin_vectors(self):
        V = self.V
        caughtError = False
        try:
            Graph([V['D->E'], V['E->B'], V['B->D'], V['B->C']])
        except BranchingGraphError as error:
            caughtError = True
        self.assertTrue(caughtError)
    
    def test_a_graph_can_check_for_incorrectness(self):
        V = self.V
        vList = [V['D->E'], V['E->B'], V['B->D'], V['C->B']]
        graph = Graph(vList)
        self.assertEqual(graph.isValid(), False)
    
    def test_a_graph_can_check_for_correctness(self):
        V = self.V
        vList = [V['D->E'], V['E->B'], V['B->D']]
        graph = Graph(vList)
        self.assertEqual(graph.isValid(), True)
    
    def test_graph_has_a_weight(self):
        V = self.V
        vList = [V['D->E'], V['E->B'], V['B->D']]
        graph = Graph(vList)
        self.assertEqual(graph.getWeight(), 230)
    
    def test_graph_can_output_a_sensible_string(self):
        V = self.V
        vList = [V['D->E'], V['E->B'], V['B->D']]
        graph = Graph(vList)
        self.assertEqual(str(graph), "(D->E->B->D): 230")

    def test_integrator_can_integrate_modifications_into_a_graph(self):
        V = self.V
        vList = [V['D->E'], V['E->B'], V['B->D']]
        newList = [V['D->E'], V['E->B'], V['B->C']]
        graph = Graph(vList)
        graph.replace([V['B->C']])
        self.assertEqual(str(Graph(newList)), str(graph))

    def vectorCompare(self, v1, v2):
        self.assertEqual(str(v1), str(v2))

    # def setUp(self):
    #     self.graph = Integrator()