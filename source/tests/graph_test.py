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
        "B->A": Vector('B', 'A', 0),
        "C->E": Vector('C', 'E', 0),
        "D->A": Vector('D', 'A', 0),
        "E->A": Vector('E', 'A', 0),
    }
    
    def test_a_graph_can_copy_itself(self):
        V = self.V
        graph = Graph(['A->B', 'B->D', 'C->B', 'D->A'], V)
        self.assertTrue(graph is not graph.copy())
        self.assertEqual(str(graph), str(graph.copy()))
        self.assertEqual(graph.lastChange, graph.copy().lastChange)
    
    def test_a_graph_can_translate_an_ascii_key_to_an_index(self):
        V = self.V
        graph = Graph(['A->B', 'B->D', 'C->B', 'D->A'], V)
        self.assertEqual(graph.translate('A'), 0)
        self.assertEqual(graph.translate('C'), 2)
    
    def test_a_graph_can_go_deeper(self):
        V = self.V
        graph = Graph(['A->B', 'B->D', 'C->B', 'D->A'], V)
        w = graph.getWeight()
        newWeight = graph.goDeeper(V['E->C'], w)
        self.assertEqual(newWeight, w + V['E->C'][2])
        self.assertEqual(graph.data[4], 'E->C')
        self.assertEqual(graph.lastChange, 'E->B')
    
    def test_a_graph_can_go_across(self):
        V = self.V
        vList = ['A->B', 'B->D', 'C->B', 'D->A', 'E->A']
        graph = Graph(vList, V)
        graph.replace(V['D->C'])
        newWeight = graph.goAcross(V['E->C'], V['D->C'][2])
        expectedNewWeight = V['E->C'][2]
        self.assertEqual(graph.data[4], 'E->C')
        self.assertEqual(graph.data[3], 'D->A')
        self.assertEqual(graph.lastChange, 'E->A')
        self.assertEqual(newWeight, expectedNewWeight)
    
    def test_a_graph_returns_none_when_constructed_with_duplicate_origin_vectors(self):
        V = self.V
        caughtError = False
        try:
            Graph(['A->B', 'B->D', 'B->C', 'D->A'], V)
        except BranchingGraphError:
            caughtError = True
        self.assertTrue(caughtError)
    
    def test_a_graph_can_check_for_difficult_incorrectness(self):
        V = self.V
        vList = ['A->B', 'B->A', 'C->E', 'D->C', 'E->D']
        graph = Graph(vList, V)
        self.assertEqual(graph.isValid(), False)
    
    def test_a_can_output_a_list_of_its_vectors(self):
        V = self.V
        vList = ['A->B', 'B->A', 'C->E', 'D->C', 'E->D']
        graph = Graph(vList, V)
        self.assertEqual(graph.toVectorListString(), "{<A->B:50><B->A:0><C->E:0><D->C:75><E->D:30>}")
    
    def test_a_graph_can_check_for_incorrectness(self):
        V = self.V
        vList = ['A->B', 'B->D', 'C->B', 'D->A']
        graph = Graph(vList, V)
        self.assertEqual(graph.isValid(), False)
    
    def test_a_graph_can_check_for_correctness(self):
        V = self.V
        vList = ['A->C', 'B->A', 'C->B']
        graph = Graph(vList, V)
        self.assertEqual(graph.isValid(), True)
    
    def test_graph_has_a_weight(self):
        V = self.V
        vList = ['A->B', 'B->C', 'C->A']
        graph = Graph(vList, V)
        self.assertEqual(graph.getWeight(), 375)
    
    def test_graph_can_output_a_sensible_string(self):
        V = self.V
        vList = ['A->B', 'B->C', 'C->A']
        graph = Graph(vList, V)
        self.assertEqual(str(graph), "(A->B->C->A): 230")
    
    def test_graph_tracks_its_modifications(self):
        V = self.V
        vList = ['A->B', 'B->C', 'C->E', 'D->A', 'E->D']
        graph = Graph(vList, V)
        self.assertEqual(None, graph.lastChange)
        graph.replace(V['D->C'])
        self.assertEqual('D->A', str(graph.lastChange))

    def test_integrator_can_integrate_modifications_into_a_graph(self):
        V = self.V
        vList = ['A->B', 'B->C', 'C->E', 'D->A', 'E->D']
        newList = ['A->B', 'B->A', 'C->E', 'D->C', 'E->D']
        graph = Graph(vList, V)
        graph.replace(V['D->C'])
        graph.replace(V['B->D'])
        graph.replace(V['B->A'])
        self.assertEqual(str(Graph(newList, V)), str(graph))

    def vectorCompare(self, v1, v2):
        self.assertEqual(str(v1), str(v2))