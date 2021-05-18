#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for Tree, TreeBDFA, TreeBDFT, GB and Minimalist grammars,
GB to Minimalist transducer.
"""

import unittest

from tree import Tree
from treebdfa import TreeBDFA
from grammars import gb_grammar, minimalist_grammar
from transducer_v1 import gb_to_min as gb_to_min_v1
from transducer_v2 import gb_to_min as gb_to_min_v2
import test_trees as tts

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


class GBToMinGramTransTest(unittest.TestCase):

    def test_gb_grammar(self):
        self.assertTrue(gb_grammar.recognizes(tts.gb_np_n))
        self.assertTrue(gb_grammar.recognizes(tts.gb_np_d_n))
        self.assertTrue(gb_grammar.recognizes(tts.gb_simple_trans_clause))
        self.assertTrue(gb_grammar.recognizes(tts.gb_pp_comp_cp_comp))

    def test_min_grammar(self):
        self.assertTrue(minimalist_grammar.recognizes(tts.min_dp_d))
        self.assertTrue(minimalist_grammar.recognizes(tts.min_dp_d_n))
        self.assertTrue(minimalist_grammar.recognizes(tts.min_simple_trans_clause))
        self.assertTrue(minimalist_grammar.recognizes(tts.min_pp_comp_cp_comp))

    def test_gb_to_min_v1(self):
        self.assertEqual(gb_to_min_v1.transform(tts.gb_np_n),
                         tts.min_dp_d_n)
        self.assertEqual(gb_to_min_v1.transform(tts.gb_np_d_n),
                         tts.min_dp_d_n)
        self.assertEqual(gb_to_min_v1.transform(tts.gb_simple_trans_clause),
                         tts.min_simple_trans_clause)

    def test_gb_to_min_v2(self):
        self.assertEqual(gb_to_min_v2.transform(tts.gb_np_n),
                         tts.min_dp_d_n)
        self.assertEqual(gb_to_min_v2.transform(tts.gb_np_d_n),
                         tts.min_dp_d_n)
        self.assertEqual(gb_to_min_v2.transform(tts.gb_simple_trans_clause),
                         tts.min_simple_trans_clause)
        self.assertEqual(gb_to_min_v2.transform(tts.gb_pp_comp_cp_comp),
                         tts.min_pp_comp_cp_comp)


if __name__ == '__main__':
    unittest.main()
