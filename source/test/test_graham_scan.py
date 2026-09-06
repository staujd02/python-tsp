import unittest

from source.utilities.graham_scan import GrahamScan

class GrahamScan_test(unittest.TestCase):
    
    def test_scanner_can_find_a_hull_list(self):
        hullList = GrahamScan.getConvexHull(self.hull_points + self.interior_points)
        labels = list(map(lambda pt: pt[2], hullList))
        self.assertEqual(6, len(labels))
        self.assertEqual('A', labels[0])
        self.assertEqual('F', labels[1])
        self.assertEqual('E', labels[2])
        self.assertEqual('D', labels[3])
        self.assertEqual('C', labels[4])
        self.assertEqual('B', labels[5])

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
