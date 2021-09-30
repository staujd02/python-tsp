from source.dataStructures import Vector
from source.utilities.trajectoryCounts import TrajectoryCounts
import unittest
import array

class Trajectory_Counts_test(unittest.TestCase):

    def test_if_a_trajectory_register_demonstrates_consistency(self):
        zeroRegister = array.array('i', [0] * 5)
        self.assertEqual([False, 0], TrajectoryCounts.demonstratesConsistency(zeroRegister))
        misMatchRegister = array.array('i', [0, 1, 0])
        self.assertEqual([False, 0], TrajectoryCounts.demonstratesConsistency(misMatchRegister))
        onesRegister = array.array('i', [1] * 4)
        self.assertEqual([True, 0], TrajectoryCounts.demonstratesConsistency(onesRegister))
        register = array.array('i', [1, 1, 1])
        self.assertEqual([True, 0], TrajectoryCounts.demonstratesConsistency(register, 0))
        self.assertEqual([True, 1], TrajectoryCounts.demonstratesConsistency(register, 1))
        self.assertEqual([True, 2], TrajectoryCounts.demonstratesConsistency(register, 2))
        register = array.array('i', [1, 2, 1])
        self.assertEqual([False, 1], TrajectoryCounts.demonstratesConsistency(register, 2))
        register = array.array('i', [1, 4, 1, 4, 1, 1, 1])
        self.assertEqual([False, 1], TrajectoryCounts.demonstratesConsistency(register, 4))
    
    def test_if_a_register_can_be_filled_from_graph_data(self):
        register = TrajectoryCounts.fillRegister(['A->B', 'B->A', 'C->A'])
        self.assertEqual(register, array.array('i', [2, 1, 0]))
        register = TrajectoryCounts.fillRegister(['A->B', 'B->C', 'C->A'])
        self.assertEqual(register, array.array('i', [1, 1, 1]))
        register = TrajectoryCounts.fillRegister(['A->C', 'B->A', 'C->B'])
        self.assertEqual(register, array.array('i', [1, 1, 1]))
    
    def test_if_a_delta_register_can_be_created(self):
        register = array.array('i', [1, 2, 0])
        delta = TrajectoryCounts.createDeltaRegister(register, 'A->B', Vector('A', 'C', 3))
        self.assertEqual(delta, array.array('i', [1, 1, 1]))
        
        newDelta = TrajectoryCounts.createDeltaRegister(delta, 'B->C', Vector('B', 'A', 3))
        self.assertEqual(newDelta, array.array('i', [2, 1, 0]))