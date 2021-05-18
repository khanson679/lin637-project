#!/usr/bin/env python3

"""
Definitions of GB and Minimalist tree grammars and transducers.
"""

from tree import Tree
from treebdft import TreeBDFT
import test_trees as tts

# data to intialize TreeBDFT
# transitions added later will replace conflicting transitions added earlier
#  when the list is converted to a dictionary
states = []
alph = []
finals = []
trans = []

#
# basic X-bar transitions
#
# we do not handle c-selection, so we can greatly decrease the number of
#  transitions by using a single state "qXP" to represent a phrase of any category
#

states.append("qXP")
finals.append("qXP")

for z in "XYZNAVPDIC":
    zbar = z + "'"
    zp = z + 'P'
    qz = 'q' + z
    qzbar = 'q' + z + "bar"
    QXP = "qXP"
    UNK = "?"
    UNKBAR = "?'"
    UNKP = "?P"
    states.extend([qz, qzbar])
    alph.extend([z, zbar, zp])
    trans.extend([
        ([], z, qz, Tree('')),
        ([qz], zbar, qz, Tree('')),
        ([qz], zp, QXP, Tree(zp)),
        ([qz, QXP], zbar, qzbar, Tree(1)),
        ([qzbar], zp, QXP, Tree.from_list([zp, z, 0])),
        ([QXP, qzbar], zp, QXP, Tree.from_list([zp, 0, [zbar, z, 1]])),
        ([QXP, qz], zp, QXP, Tree.from_list([UNKP, 0, [UNKBAR, UNK, zp]]))
    ])


#
# transitions for NP -> DP conversion
#
# Allows a singleton DP in the specifier of NP in the GB tree to become the
#   head of DP in the Minimalist tree.
# If there is no DP spec, or it is not a singleton DP, a null D will
#   be inserted.
#

n = "N"
nbar = "N'"
np = "NP"
d = "D"
dbar = "D'"
dp = "DP"

qn = "qN"
qnbar = "qNbar"
qd = "qD"
qdbar = "qDbar"
qdp = "qDP"
QXP = "qXP"

states.extend([qd, qdbar, qdp])
trans.extend([
    ([], d, qd, Tree('')),
    ([qd], dbar, qd, Tree('')),
    ([qd], dp, qdp, Tree('')),
    ([], n, qn, Tree('')),
    ([qn], nbar, qn, Tree('')),
    ([qn], np, QXP, Tree.from_list([dp, d, np])),
    ([qdp, qn], np, QXP, Tree.from_list([dp, d, np])),
    ([qdp, qnbar], np, QXP, Tree.from_list([dp, d, [np, n, 1]])),
    ([QXP, qn], np, QXP, Tree.from_list([dp, 0, [dbar, d, np]])),
    ([QXP, qnbar], np, QXP, Tree.from_list([dp, 0, [dbar, d, [np, n, 1]]]))
])

#
# transitions for IP -> TP conversion
#
# Essentatially the same as the basic transitions, but also relabels
#   I/I'/IP -> T/T'/TP
#

i = "I"
ibar = "I'"
ip = "IP"
t = "T"
tbar = "T'"
tp = "TP"

qi = "qI"
qibar = "qIbar"
QXP = "qXP"

trans.extend([
    ([], i, qi, Tree('')),
    ([qi], ibar, qi, Tree('')),
    ([qi], ip, QXP, Tree(tp)),
    ([qi, QXP], ibar, qibar, Tree(1)),
    ([qibar], ip, QXP, Tree.from_list([tp, t, 0])),
    ([QXP, qibar], ip, QXP, Tree.from_list([tp, 0, [tbar, t, 1]])),
    ([QXP, qi], ip, QXP, Tree.from_list([UNKP, 0, [UNKBAR, UNK, [tbar, t]]]))])

gb_to_min = TreeBDFT(states, alph, finals, trans)


#
# testing
#

if __name__ == '__main__':
    for t in [tts.gb_xp_singleton,
              tts.gb_xp_w_comp,
              tts.gb_xp_w_comp_spec,
              tts.gb_xp_w_spec_no_comp,
              tts.gb_np_n,
              tts.gb_np_d_n,
              tts.gb_simple_trans_clause,
              tts.gb_pp_comp_cp_comp]:
        print(gb_to_min.transform(t, debug=True))
