#!/usr/bin/env python3

"""
Definitions of GB and Minimalist tree grammars and transducers.
"""

from tree import Tree
from treebdfa import TreeBDFA
import test_trees

#
# Simple SS-style grammar
#

qs = ['qS', 'qNP', 'qN', 'qVP', 'qV', 'qDet']
xs = ['S', 'NP', 'N', 'Det', 'VP', 'V']
fs = ['qNP', 'qVP', 'qS']
ts = [([], 'N', 'qN'),
      ([], 'V', 'qV'),
      ([], 'Det', 'qDet'),
      (['qDet', 'qN'], 'NP', 'qNP'),
      (['qV'], 'VP', 'qVP'),
      (['qV', 'qNP'], 'VP', 'qVP'),
      (['qNP', 'qVP'], 'S', 'qS')]
ss_grammar = TreeBDFA(qs, xs, fs, ts)

#
# GB-style X-bar grammar
#

qs = ["qXP"]
xs = []
fs = ["qXP"]

# Generate X-bar rules for each syntactic category
#   X' -> X
#   X' -> X YP
#   XP -> X'
#   XP -> ZP X'
# A single state "qXP" will be returned upon processing a phrase of any category.
#   In other words, subcategorization is not modeled.
ts = []
for z in "NAVPDTC":
    zbar = z + "'"
    zp = z + 'P'
    qz = 'q' + z
    qzbar = 'q' + z + "bar"
    QXP = "qXP"
    qs.extend([qz, qzbar])
    xs.extend([z, zbar, zp])
    ts.extend(
        [([], z, qz),
         ([qz], zbar, qzbar),
         ([qz, QXP], zbar, qzbar),
         ([qzbar], zp, QXP),
         ([QXP, qzbar], zp, QXP)])

gb_grammar = TreeBDFA(qs, xs, fs, ts)


#
# Minimalist-style ("bare phrase structure") X-bar grammar
#

qs = ["qXP"]
xs = []
fs = ["qXP"]

# Generate X-bar rules for each syntactic category
#   XP -> X YP
#   X' -> X YP
#   XP -> ZP X'
# A single state "qXP" will be returned upon processing a phrase of any category.
#   In other words, subcategorization is not modeled.
ts = []
for z in "NAVPDTC":
    zbar = z + "'"
    zp = z + 'P'
    qz = 'q' + z
    qzbar = 'q' + z + "bar"
    QXP = "qXP"
    qs.extend([qz, qzbar])
    xs.extend([z, zbar, zp])
    ts.extend(
        [([], zp, QXP),
         ([], z, qz),
         ([qz, QXP], zp, QXP),
         ([qz, QXP], zbar, qzbar),
         ([QXP, qzbar], zp, QXP)])

minimalist_grammar = TreeBDFA(qs, xs, fs, ts)


def test_simple():
    t1 = Tree.from_list(['S', ['NP', ['Det'], ['N']],
                         ['VP', ['V'], ['NP', ['Det'], ['N']]]])
    print(t1)
    print(ss_grammar.recognizes(t1))


def test_gb():
    # print(gb_grammar)
    t1 = test_trees.gb_np_n
    t2 = test_trees.gb_np_d_n
    t3 = test_trees.gb_simple_trans_clause
    for t in [t1, t2, t3]:
        print(t)
        print(gb_grammar.recognizes(t))


def test_minimalist():
    # print(minimalist_grammar)
    t1 = test_trees.min_dp_leaf
    t2 = test_trees.min_dp_d_n
    t3 = test_trees.min_simple_trans_clause
    for t in [t1, t2, t3]:
        print(t)
        print(minimalist_grammar.recognizes(t))


if __name__ == "__main__":
    test_gb()
    test_minimalist()
