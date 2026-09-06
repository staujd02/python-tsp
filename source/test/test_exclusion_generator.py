import unittest

from source.utilities.graham_scan import GrahamScan
from source.utilities.exclusion_generator import ExclusionGenerator

class ExclusionGenerator_test(unittest.TestCase):
    
    def test_exclusion_generator_can_produce_the_excluded_list(self):
        hullList = GrahamScan.getConvexHull(self.hull_points + self.interior_points)
        self.exclusion_list = ExclusionGenerator.generateExclusionDictionary(hullList)
        self.assertEqual({
            'A': ['E', 'D', 'C'],
            'B': ['F', 'E', 'D'],
            'C': ['A', 'F', 'E'],
            'D': ['B', 'A', 'F'],
            'E': ['C', 'B', 'A'],
            'F': ['D', 'C', 'B'],
        }, self.exclusion_list)

    def matches(self, expected, idx):
        self.assertEqual(expected, self.exclusion_list[idx])

    def setUp(self):
        self.hull_points = [
            [2,2,'A'],
            [2,6,'B'],
            [3,7,'C'],
            [7,6,'D'],
            [7,3,'E'],
            [5,1,'F']
        ]
        self.interior_points = [
            [3,2,'1'],
            [3,5,'2'],
            [3,6,'3'],
            [5,6,'4'],
            [6,3,'5'],
            [5,2,'6']
        ]
