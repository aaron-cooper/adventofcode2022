import unittest
from . import p2
import sys


class TestPerimeterPoint(unittest.TestCase):
    def setUp(t):
        t.point = p2.PerimeterPoint

    def test_lessThan_returnsFalseWhenPointsEqual(t):
        cases = [
            t.point((1, 8), (5, 8)),
            t.point((2, 9), (5, 8)),
            t.point((5, 10), (5, 8)),
            t.point((5, 9), (5, 8)),
            t.point((6, 7), (5, 8)),
            t.point((4, 8), (5, 8))
        ]
        for c in cases:
            with t.subTest(c=c):
                t.assertFalse(c < c)

    def test_lessThan_returnsTrueWhenLeftIsLess(t):
        cases = [
            (t.point((-2, 0), (0, 0)), t.point((2, 0), (0, 0))),
            (t.point((0, 2), (0, 0)), t.point((0, -2), (0, 0))),
            (t.point((-2, 0), (0, 0)), t.point((0, 2), (0, 0))),
            (t.point((-2, 0), (0, 0)), t.point((0, -2), (0, 0))),
            (t.point((1, 1), (0, 0)), t.point((-1, -1), (0, 0))),
            (t.point((-2, 0), (0, 0)), t.point((-1, -1), (0, 0)))
        ]
        for left, right in cases:
            with t.subTest(left=left, right=right):
                t.assertTrue(left < right)

    def test_lessThan_returnsFalseWhenLeftIsMore(t):
        cases = [
            (t.point((2, 0), (0, 0)), t.point((-2, 0), (0, 0))),
            (t.point((0, -2), (0, 0)), t.point((0, 2), (0, 0))),
            (t.point((0, 2), (0, 0)), t.point((-2, 0), (0, 0))),
            (t.point((0, -2), (0, 0)), t.point((-2, 0), (0, 0))),
            (t.point((-1, -1), (0, 0)), t.point((1, 1), (0, 0))),
            (t.point((-1, -1), (0, 0)), t.point((-2, 0), (0, 0)))
        ]
        for left, right in cases:
            with t.subTest(left=left, right=right):
                t.assertFalse(left < right)

class TestSensor(unittest.TestCase):
    def setUp(t):
        t.pdiamond = p2.PerimeteredDiamond
        t.diamond = p2.Diamond

    def test_overlaps_returnsFalseWhenNoOverlap(t):
        cases = [
            (t.pdiamond(0, 0, 0), t.diamond(0, 1, 0)),
            (t.pdiamond(5, 5, 3), t.diamond(9, 8, 3)),
            (t.pdiamond(9, 8, 3), t.diamond(5, 5, 3))
        ]
        for left, right in cases:
            with t.subTest(left=left, right=right):
                t.assertFalse(left.overlaps(right))

    def test_overlaps_returnsTrueWhenOverlap(t):
        cases = [
            (t.pdiamond(5, 5, 3), t.diamond(8, 8, 3)),
            (t.pdiamond(8, 8, 3), t.diamond(5, 5, 3)),
            (t.pdiamond(5, 5, 3), t.diamond(8, 8, 4)),
            (t.pdiamond(8, 8, 4), t.diamond(5, 5, 3)),
            (t.pdiamond(3, 3, 3), t.diamond(3, 6, 3)),
            (t.pdiamond(3, 6, 3), t.diamond(3, 3, 3)),
            (t.pdiamond(3, 3, 3), t.diamond(3, 5, 3)),
            (t.pdiamond(3, 5, 3), t.diamond(3, 3, 3)),
            (t.pdiamond(0, 0, 3), t.diamond(1, 1, 6)),
            (t.pdiamond(1, 1, 6), t.diamond(0, 0, 3))
        ]
        for left, right in cases:
            with t.subTest(left=left, right=right):
                t.assertTrue(left.overlaps(right))


class TestDiamondIntersectFinder(unittest.TestCase):
    def setUp(t):
        t.diamond = p2.Diamond
        t.ifinder = p2.DiamondIntersectionFinder

    def test_valid_returnsCorrectValidPoints(t):
        sut = t.ifinder()
        left = t.diamond(8, 8, 4)
        cases = [
            #1 corner, 2 intersects on adj. edges
            # ceil/floor required
            (t.diamond(4, 8, 3), ((5, 7), (5, 9))),
            (t.diamond(8, 12, 3), ((7, 11), (9, 11))),
            (t.diamond(12, 8, 3), ((11, 9), (11, 7))),
            (t.diamond(8, 4, 3), ((9, 5), (7, 5))),
            # not required
            (t.diamond(3, 8, 3), ((5, 7), (5, 9))),
            (t.diamond(8, 13, 3), ((7, 11), (9, 11))),
            (t.diamond(13, 8, 3), ((11, 9), (11, 7))),
            (t.diamond(8, 3, 3), ((9, 5), (7, 5))),
            # 1 corners, an intersect lands on a corner
            (t.diamond(5, 9, 3), ((5, 7), (6, 10))),
            (t.diamond(7, 11, 3), ((6, 10), (9, 11))),
            (t.diamond(9, 11, 3), ((7, 11), (10, 10))),
            (t.diamond(11, 9, 3), ((10, 10), (11, 7))),
            (t.diamond(11, 7, 3), ((11, 9), (10, 6))),
            (t.diamond(9, 5, 3), ((10, 6), (7, 5))),
            (t.diamond(7, 5, 3), ((9, 5), (6, 6))),
            (t.diamond(5, 7, 3), ((6, 6), (5, 9))),
            # 0 corners, intersects on opposite edges
            (t.diamond(6, 10, 5), ((6, 6), (10, 10))),
            (t.diamond(10, 6, 5), ((10, 10), (6, 6))),
            (t.diamond(6, 6, 5), ((10, 6), (6, 10))),
            (t.diamond(10, 10, 5), ((6, 10), (10, 6))),
            # 1 intersect = a corner
            (t.diamond(1, 8, 3), ((4, 8), (4, 8))),
            (t.diamond(8, 15, 3), ((8, 12), (8, 12))),
            (t.diamond(15, 8, 3), ((12, 8), (12, 8))),
            (t.diamond(8, 1, 3), ((8, 4), (8, 4)))
        ]
        for right, expected in cases:
            with t.subTest(left=left, right=right, expected=expected):
                actual = sut.intersects(left, right)
                t.assertEqual(actual, expected)


suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
runner = unittest.TextTestRunner()
runner.run(suite)
