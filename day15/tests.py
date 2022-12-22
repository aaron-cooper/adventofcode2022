import p1
import unittest

class TestUnionFinder(unittest.TestCase):

    def setUp(t):
        t.sut = p1.UnionFinder()

    def sen(t, *params):
        return [p1.FlatSensor(s[0], s[1]) for s in params]

    def test_singleSensor(t):
        sensors = t.sen((5, 3))
        # ___5___
        covered = t.sut.spots_covered(sensors)
        t.assertEqual(covered, 7)

    def test_nonOverlappingSensors(t):
        sensors = t.sen((-10, 2), (0, 2), (10, 2))
        #  -1                   1
        # __0__     __0__     __0__
        covered = t.sut.spots_covered(sensors)
        t.assertEqual(covered, 15)

    def test_singleOverlap(t):
        sensors = t.sen((0, 5), (9, 5))
        covered = t.sut.spots_covered(sensors)
        # _____0_____
        #          _____9_____
        t.assertEqual(covered, 20)

    @unittest.skip('not implemented')
    def test_singleOverlapSensorsWithinOverlap(t):
        sensors = t.sen((0, 5), (3, 5))
        covered = t.sut.spots_covered(sensors)
        # _____0_____
        #   _____3_____
        t.assertEqual(covered, 14)

    @unittest.skip('not implemented')
    def test_multipleDoubleOverlaps(t):
        sensors = t.sen((0, 4), (7, 4), (14, 4))
        covered = t.sut.spots_covered(sensors)
        #____0____
        #       ____7____
        #              ___14____
        t.assertEqual(covered, 23)

    @unittest.skip('not implemented')
    def test_tripleOverlap(t):
        sensors = t.sen((0, 7), (6, 4), (12, 7))
        covered = t.sut.spots_covered(sensors)
        #_______0_______
        #         ____6____
        #            ______12_______
        t.assertEqual(covered, 7)

    @unittest.skip('not implemented')
    def test_quadOverlap(t):
        sensors = t.sen((5, 4), (7, 4), (9, 4), (11, 4))
        covered = t.sut.spots_covered(sensors)
        #____5____
        #  ____7____
        #    ____9____
        #      ___11____
        t.assertEqual(covered, 15)

    @unittest.skip('not implemented')
    def test_quintOverlap(t):
        sensors = t.sen((5, 4), (7, 4), (9, 4), (11, 4), (13, 4))
        covered = t.sut.spots_covered(sensors)
        #____5____
        #  ____7____
        #    ____9____
        #      ___11____
        #        ___13____
        t.assertEqual(covered, 17)

    @unittest.skip('not implemented')
    def test_supersetSingleOverlapLargerAfter(t):
        sensors = t.sen((0, 4), (3, 10))
        covered = t.sut.spots_covered(sensors)
        #   ____0____
        #__________3__________
        t.assertEqual(covered, 11)

    @unittest.skip('not implemented')
    def test_supersetSingleOverlapLargerBefore(t):
        sensors = t.sen((0, 10), (3, 4))
        covered = t.sut.spots_covered(sensors)
        #__________0__________
        #         ____3____
        t.assertEqual(covered, 11)

    @unittest.skip('not implemented')
    def test_supersetOfMultiple(t):
        sensors = t.sen((0, 12), (3, 2), (9, 2))
        covered = t.sut.spots_covered(sensors)
        #____________0____________
        #             __3__
        #                   __9__
        t.assertEqual(covered, 25)


    @unittest.skip('not implemented')
    def test_manyOverlapTypes(t):
        sensors = t.sen((0, 2), (0, 11), (2, 2), (4, 5), (4, 2), (5, 9))
        covered = t.sut.spots_covered(sensors)
        #    __0__
        #___________5___________
        #      __2__
        #     _____4_____
        #        __4__
        #  _________5_________
        t.assertEqual(covered, 23)

    @unittest.skip('not implemented')
    def test_sevenIdenticalBeacons(t):
        sensors = t.sen((0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2), (0, 2))
        covered = t.sut.spots_covered(sensors)
        #__0__
        #__0__
        #__0__
        #__0__
        #__0__
        #__0__
        #__0__
        t.assertEqual(covered, 5)



suite = unittest.defaultTestLoader.loadTestsFromModule(__import__(__name__))
runner = unittest.TextTestRunner()
runner.run(suite)