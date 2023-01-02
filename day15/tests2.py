import unittest
from . import p2
import sys

class TestPerimeterToIntConverter(unittest.TestCase):
    def setUp(t):
        t.diamond = p2.Diamond
        t.converter = p2.PerimeterPointToIntConverter

    def test_convertsCorrectlyWithZeroRadiusDiamond(t):
        d = t.diamond(99, 100, 0)
        sut = t.converter(d)
        with t.subTest("to"):
            t.assertEqual(sut((99, 100)), 0)
        with t.subTest("from"):
            t.assertEqual(sut.back(0), (99, 100))

    def test_convertsCorrectlyWithRadiusOneDiamond(t):
        d = t.diamond(5, 8, 1)
        sut = t.converter(d)
        cases = [
            [(4, 8), 0],
            [(5, 9), 1],
            [(6, 8), 2],
            [(5, 7), 3]
        ]

        for val, converted in cases:
            with t.subTest(f'converting {val}, expecting {converted}'):
                t.assertEqual(sut(val), converted)

        for converted, val in cases:
            with t.subTest(f'converting {val}, expecting {converted}'):
                t.assertEqual(sut.back(val), converted)

    def test_convertsCorrectlyWithNominalRadiusDiamond(t):
        d = t.diamond(5, 5, 3)
        sut = t.converter(d)
        cases = [
            [(2, 5), 0],
            [(3, 6), 1],
            [(4, 7), 2],
            [(5, 8), 3],
            [(6, 7), 4],
            [(7, 6), 5],
            [(8, 5), 6],
            [(7, 4), 7],
            [(6, 3), 8],
            [(5, 2), 9],
            [(4, 3), 10],
            [(3, 4), 11]
        ]

        for val, converted in cases:
            with t.subTest(f'converting {val}, expecting {converted}'):
                t.assertEqual(sut(val), converted)

        for converted, val in cases:
            with t.subTest(f'converting {val}, expecting {converted}'):
                t.assertEqual(sut.back(val), converted)

class TestDiamond(unittest.TestCase):
    def setUp(t):
        t.diamond = p2.Diamond

    def test_fully_contains_trueWhenOtherDiamondIsFullyContained(t):
        cases = [
            [(0, 0, 5), (0, 0, 4)],
            [(0, 0, 5), (0, 0, 5)],
            [(0, 0, 5), (-3, 0, 2)],
            [(0, 0, 5), (-2, 1, 2)]
        ]
        for i, (d1, d2) in enumerate(cases):
            with t.subTest(f"case {i}: {cases[i]}"):
                t.assertTrue(t.diamond(*d1).fully_contains(t.diamond(*d2)))

    def test_fully_contains_falseWhenOtherDiamondIsNotFullyContained(t):
        cases = [
            [(0, 0, 5), (0, 0, 6)],
            [(0, 0, 5), (-4, 0, 2)],
            [(0, 0, 5), (-2, 2, 2)]
        ]
        for i, (d1, d2) in enumerate(cases):
            with t.subTest(f"case {i}: {cases[i]}"):
                t.assertFalse(t.diamond(*d1).fully_contains(t.diamond(*d2)))

class TestPerimeteredDiamond(unittest.TestCase):
    def setUp(t):
        t.pdiamond = p2.PerimeteredDiamond
        t.diamond = p2.Diamond
        t.square = p2.Square

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

    def test_constrain_perimeter(t):
        cases = [
            # diamond,   constraint,      expected perimeter
            # diamond is completely within bounds
            [(5, 5, 3), ((1, 1), (9, 9)), [(0, 11)]],
            # diamond is kissing the bound on all sides
            [(5, 5, 3), ((2, 2), (8, 8)), [(1, 2), (4, 5), (7, 8), (10, 11)]],
            # diamond is kissing the bound on the left
            [(5, 5, 3), ((2, 0), (10, 10)), [(1, 11)]],
            # diamond is out of bound on the left
            [(5, 5, 3), ((3, 0), (10, 10)), [(2, 10)]],
            # most of the diamond is in bounds, but the corners are out of bounds
            [(4, 5, 5), ((0, 1), (8, 8)), [(2, 2), (8, 8), (12, 13), (17, 18)]],
            # diamond to top-left of bound, bound's corner is inside diamond
            [(2, 8, 4), ((3, 3), (10, 7)), [(10, 10)]],
            # top-right of bound
            [(9, 9, 4), ((2, 2), (8, 8)), [(14, 14)]],
            # bottom-right of bound
            [(9, 2, 4), ((2, 2), (8, 8)), [(1, 2)]],
            # bottom-left of bound
            [(2, 2, 4), ((2, 2), (8, 8)), [(5, 7)]]
        ]

        for i, (diamond, constraint, expected) in enumerate(cases):
            diamond = t.pdiamond(*diamond)
            with t.subTest(f"case {i}: {cases[i]}"):
                diamond.constrain_perimeter(t.square(*constraint))
                t.assertEqual(diamond.perimeter, expected)

    def test_remove_from_perimeter(t):
        # test that empty intervals discarded properly
        cases = [
            # [(<diamond x y r>), [intervals...], [expected...]]
            [(5, 5, 4), [((2, 4), (2, 6))], [(2, 14)]],
            [(5, 5, 4), [((7, 3), (7, 7))], [(7, 9)]],
            [(5, 5, 4), [((1, 5), (1, 5))], [(1, 15)]],
            [(5, 5, 4), [((3, 7), (7, 7))], [(0, 1), (7, 15)]],
            [(5, 5, 4), [((3, 7), (3, 3))], [(0, 1), (15, 15)]],
            [(5, 5, 4), [((7, 7), (7, 3))], [(0, 5), (11, 15)]],
            [(5, 5, 4), [((7, 3), (3, 3))], [(0, 9), (15, 15)]],
            [(5, 5, 4), [((2, 4), (6, 8))], [(6, 14)]],
            [(5, 5, 4), [((6, 8), (2, 4))], [(0, 4)]],
            [(5, 5, 4), [((7, 3), (3, 3)), ((7, 3), (3, 3))], [(0, 9), (15, 15)]],
            [(5, 5, 4), [((1, 5), (6, 8)), ((8, 6), (1, 5))], [(6, 6)]],
            [(5, 5, 4), [((1, 5), (6, 8)), ((8, 6), (1, 5)), ((7, 7), (7, 7))], []]
        ]
        for i, (diamond, removals, expected) in enumerate(cases):
            with t.subTest(f"case {i}: {cases[i]}"):
                diamond = t.pdiamond(*diamond)
                for interval in removals:
                    diamond.remove_from_perimeter(interval)
                t.assertEqual(diamond.perimeter, expected)

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
                actual = sut(left, right)
                t.assertEqual(actual, expected)


if tname := '':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromName(tname, sys.modules[__name__]))
else:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
runner = unittest.TextTestRunner()
runner.run(suite)
