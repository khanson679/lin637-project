#!/usr/bin/env python3

"""
Definitions of GB and Minimalist tree grammars and transducers.
"""

from tree import Tree
from treebdfa import TreeBDFA

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
mini_grammar = TreeBDFA(qs, xs, fs, ts)

qs = ["qXP"]
xs = []
fs = ["qXP"]
# ts = [([], 'N', 'qN'),
#       (["qN"], "N'", "qNbar"),
#       (["qN", "qXP"], "N'", "qNbar"),
#       (["qNbar"], "NP", "qXP"),
#       (["qXP", "qNbar"], "NP", "qXP"),
#       ([], 'D', 'qD'),
#       (["qD"], "D'", "qDbar"),
#       (["qD", "qXP"], "D'", "qDbar"),
#       (["qDbar"], "DP", "qXP"),
#       (["qDbar", "qXP"], "DP", "qXP")]
ts = []
for z in "NAVPDT":
    zbar = z + "'"
    zp = z + 'P'
    qz = 'q' + z
    qzbar = 'q' + z + "bar"
    qs.extend([qz, qzbar])
    xs.extend([z, zbar, zp])
    ts.extend(
        [([], z, qz),
         ([qz], zbar, qzbar),
         ([qz, "qXP"], zbar, qzbar),
         ([qzbar], zp, "qXP"),
         (["qXP", qzbar], zp, "qXP")])

gb_grammar = TreeBDFA(qs, xs, fs, ts)


def test_mini():
    t1 = Tree.from_list(['S', ['NP', ['Det'], ['N']],
                         ['VP', ['V'], ['NP', ['Det'], ['N']]]])
    print(t1)
    print(mini_grammar.recognizes(t1))


def test_gb():
    t1 = Tree.from_list(["NP", ["N'", "N"]])
    t2 = Tree.from_list(["NP",
                         ["DP", ["D'", "D"]],
                         ["N'", "N"]])
    t3 = Tree.from_list(
        ["TP",
            ["NP",
                ["DP", ["D'", "D"]],
                ["N'", "N"]],
            ["T'",
                ["T"],
                ["VP",
                    ["V'",
                        ["V"],
                        ["NP",
                            ["DP", ["D'", "D"]],
                            ["N'", "N"]]]]]])
    for t in [t1, t2, t3]:
        print(gb_grammar)
        print(t)
        print(gb_grammar.recognizes(t, debug=True))


if __name__ == "__main__":
    test_gb()
