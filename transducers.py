#!/usr/bin/env python3

"""
Definitions of GB and Minimalist tree grammars and transducers.
"""

from tree import Tree
from treebdft import TreeBDFT
import test_trees

alph = {'N', "N'", 'NP'}
states = {'qXP', 'qN', 'qNbar', 'qNP'}
finals = {'qXP'}
trans = {
    ((), 'N'): ('qN', Tree('')),
    (('qN',), "N'"): ('qNbar', Tree('NP')),
    (('qNbar',), 'NP'): ('qXP', Tree.from_list(['DP', 'D', 0])),
    (('qN', 'qXP'), "N'"): ('qNbar', Tree.from_list(['NP', 'N', 0])),
    (('qXP', 'qNbar'), "NP"): ('qXP', Tree.from_list(['DP', 0, 1])),
    ((), 'D'): ('qD', Tree('')),
    (('qD',), "D'"): ('qDbar', Tree('')),
    (('qDbar',), 'DP'): ('qXP', Tree('D'))}
gb_to_min = TreeBDFT(states, alph, finals, trans)

print(gb_to_min)
print()
print(gb_to_min.transform(test_trees.gb_np_n))
print(gb_to_min.transform(test_trees.gb_np_d_n))