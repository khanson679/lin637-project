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
    ((), 'V'): ('qV', Tree('')),
    (('qV',), "V'"): ('qV', Tree('')),
    (('qV',), 'VP'): ('qXP', Tree('VP')),
    (('qV', 'qXP'), "V'"): ('qVbar', Tree(1)),
    (('qVbar',), 'VP'): ('qXP', Tree.from_list(['VP', 'V', 0])),
    (('qXP', 'qVbar'), "VP"): ('qXP', Tree.from_list(['VP', 0, ["V'", 'V', 1]])),
    ((), 'D'): ('qD', Tree('')),
    (('qD',), "D'"): ('qDbar', Tree('')),
    (('qDbar',), 'DP'): ('qXP', Tree('D')),
    ((), 'I'): ('qI', Tree('')),
    (('qI',), "I'"): ('qI', Tree('')),
    (('qI',), 'IP'): ('qXP', Tree('TP')),
    (('qI', 'qXP'), "I'"): ('qIbar', Tree(1)),
    (('qIbar',), 'IP'): ('qXP', Tree.from_list(['TP', 'T', 0])),
    (('qXP', 'qIbar'), "IP"): ('qXP', Tree.from_list(['TP', 0, ["T'", 'T', 1]]))}
gb_to_min = TreeBDFT(states, alph, finals, trans)

if __name__ == '__main__':
    print(gb_to_min)
    print()
    print(gb_to_min.transform(test_trees.gb_np_n))
    print(gb_to_min.transform(test_trees.gb_np_d_n))
    print(gb_to_min.transform(test_trees.gb_simple_trans_clause, debug=True))
