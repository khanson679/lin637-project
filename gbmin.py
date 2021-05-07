#!/usr/bin/env python3

"""
Definitions of GB and Minimalist tree grammars and transducers.
"""

from tree import Tree
from treebdfa import TreeBDFA

qs = ['qS', 'qNP', 'qN', 'qVP', 'qV', 'qDet']
xs = ['S', 'NP', 'N', 'Det', 'VP', 'V']
fs = ['qS']
ts = [([], 'N', 'qN'),
      ([], 'V', 'qV'),
      ([], 'Det', 'qDet'),
      (['qDet', 'qN'], 'NP', 'qNP'),
      (['qV'], 'VP', 'qVP'),
      (['qV', 'qNP'], 'VP', 'qVP'),
      (['qNP', 'qVP'], 'S', 'qS')]

mini_grammar = TreeBDFA(qs, xs, fs, ts)
t = Tree.from_list(['S', ['NP', ['Det'], ['N']],
                    ['VP', ['V'], ['NP', ['Det'], ['N']]]])

print(t)
print(mini_grammar.recognizes(t))
