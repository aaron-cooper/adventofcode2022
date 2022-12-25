from . import p1
from .p1 import UnionFinder
import unittest
import sys

class TestUnionFinder(unittest.TestCase):

    def sen(t, *params):
        return [p1.FlatSensor(s[0], s[1]) for s in params]

    def test_singleSensor(t):
        t.sut = UnionFinder(t.sen((5, 3)))
        # ___5___
        covered = t.sut.spots_covered()
        t.assertEqual(covered, 7)

    def test_nonOverlappingSensors(t):
        t.sut = UnionFinder(t.sen((-10, 2), (0, 2), (10, 2)))
        #  -1                   1
        # __0__     __0__     __0__
        covered = t.sut.spots_covered()
        t.assertEqual(covered, 15)

    def test_singleOverlap(t):
        t.sut = UnionFinder(t.sen((0, 5), (9, 5)))
        covered = t.sut.spots_covered()
        # _____0_____
        #          _____9_____
        t.assertEqual(covered, 20)

    def test_singleOverlapSensorsWithinOverlap(t):
        t.sut = UnionFinder(t.sen((0, 5), (3, 5)))
        covered = t.sut.spots_covered()
        # _____0_____
        #   _____3_____
        t.assertEqual(covered, 14)

    def test_multipleDoubleOverlaps(t):
        t.sut = UnionFinder(t.sen((0, 4), (7, 4), (14, 4)))
        covered = t.sut.spots_covered()
        #____0____
        #       ____7____
        #              ___14____
        t.assertEqual(covered, 23)

    def test_supersetSingleOverlapLargerAfter(t):
        t.sut = UnionFinder(t.sen((0, 4), (3, 10)))
        covered = t.sut.spots_covered()
        #   ____0____
        #__________3__________
        t.assertEqual(covered, 21)


    def test_supersetSingleOverlapLargerBefore(t):
        t.sut = UnionFinder(t.sen((0, 10), (3, 4)))
        covered = t.sut.spots_covered()
        #__________0__________
        #         ____3____
        t.assertEqual(covered, 21)

    def test_supersetOfMultiple(t):
        t.sut = UnionFinder(t.sen((0, 12), (3, 2), (9, 2)))
        covered = t.sut.spots_covered()
        #____________0____________
        #             __3__
        #                   __9__
        t.assertEqual(covered, 25)

    def test_tripleOverlap(t):
        t.sut = UnionFinder(t.sen((0, 7), (6, 4), (12, 7)))
        covered = t.sut.spots_covered()
        #_______0_______
        #         ____6____ 
        #            ______12_______
        t.assertEqual(covered, 27)

    def test_quadOverlap(t):
        t.sut = UnionFinder(t.sen((5, 4), (7, 4), (9, 4), (11, 4)))
        covered = t.sut.spots_covered()
        #____5____
        #  ____7____
        #    ____9____
        #      ___11____
        t.assertEqual(covered, 15)

    def test_quintOverlap(t):
        t.sut = UnionFinder(t.sen((5, 4), (7, 4), (9, 4), (11, 4), (13, 4)))
        covered = t.sut.spots_covered()
        #____5____
        #  ____7____
        #    ____9____
        #      ___11____
        #        ___13____
        t.assertEqual(covered, 17)

    def test_manyOverlapTypes(t):
        t.sut = UnionFinder(t.sen((0, 2), (5, 11), (2, 2), (4, 5), (4, 2), (5, 9)))
        covered = t.sut.spots_covered()
        #    __0__
        #___________5___________
        #      __2__
        #     _____4_____
        #        __4__
        #  _________5_________
        t.assertEqual(covered, 23)

    def test_sevenIdenticalBeacons(t):
        t.sut = UnionFinder(t.sen((0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2)))
        covered = t.sut.spots_covered()
        #__0__
        #__0__
        #__0__
        #__0__
        #__0__
        #__0__
        #__0__
        t.assertEqual(covered, 5)

    def test_brokenCase(t):
        t.sut = UnionFinder(t.sen((393374, 568808), (909141, 607858), (2746023, 363372), (277094, 1372867)))
        covered = t.sut.spots_covered()
        t.assertEqual(covered, 3472480)

if tname := '':
    suite = unittest.TestSuite()
    suite.addTest(TestUnionFinder(tname))
else:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
runner = unittest.TextTestRunner()
runner.run(suite)