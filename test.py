#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for Tree and TreeBDFA.
"""

import unittest

from tree import Tree
from treebdfa import TreeBDFA


class TreeTest(unittest.TestCase):

    def test_basic(self):
        t = Tree.from_list(['a', ['b', ['c', ['d']], ['e', ['f'], ['g'], ['h'], ['i']]]])
        self.assertEqual(t.size(), 9)
        self.assertEqual(t.depth(), 3)
        self.assertEqual(t.width(), 4)
        self.assertEqual(t.yld(), "dfghi")

    def test_gorn(self):
        T = Tree
        t = T("a", [T("b", [T("d"), T("e", [T("f"), T("g")])]), T("c")])
        st1 = T("b", [T("d"), T("e", [T("f"), T("g")])])
        st2 = T("e", [T("f"), T("g")])
        st3 = T("g")
        self.assertEqual(t.get_gorn([]), t)
        self.assertEqual(t.get_gorn([0]), st1)
        self.assertIsNone(t.get_gorn([2]))
        self.assertEqual(t.get_gorn([0, 1]), st2)
        self.assertEqual(t.get_gorn([0, 1, 1]), st3)
        self.assertIsNone(t.get_gorn([0, 1, 1, 0]))


class TreeBDFATest(unittest.TestCase):

    def test(self):
        # test tree BDFA
        qs = ['qa', 'qb', 'qS']
        xs = ['a', 'b', 'S']
        fs = ['qS']
        ts = [([], 'a', 'qa'),
              ([], 'b', 'qb'),
              (['qa', 'qb'], 'S', 'qS'),
              (['qa', 'qS', 'qb'], 'S', 'qS')]

        anbn = TreeBDFA(qs, xs, fs, ts)

        # test trees
        ta = Tree('a')
        tb = Tree('b')
        t1 = Tree('S', [ta, tb])
        t2 = Tree('S', [ta, t1, tb])
        t3 = Tree('S', [ta, t2, tb])
        t3x = Tree('S', [ta, tb, t2])

        self.assertTrue(anbn.is_valid())
        self.assertFalse(anbn.recognizes(ta))
        self.assertFalse(anbn.recognizes(tb))
        self.assertTrue(anbn.recognizes(t1))
        self.assertTrue(anbn.recognizes(t2))
        self.assertTrue(anbn.recognizes(t3))
        self.assertFalse(anbn.recognizes(t3x))


if __name__ == '__main__':
    unittest.main()
