#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pformat
from tree import Tree


class TreeBDFT:
    """Bottom-up deterministic finite-state transducer for trees.

    Parameters
    ----------
    states: set of states
    alphabet: set of symbols
    finals: set of final states
    transitions: dictionary of the form
      {(children_state_list, parent_symbol): (parent_state, var_leafed_tree)}
    """

    def __init__(self,
                 states,
                 alphabet,
                 finals,
                 transitions):
        self.states = states
        self.alph = alphabet
        self.finals = finals

        if type(transitions) in (set, list):
            self.transitions = self._delta_dict(transitions)
        elif type(transitions) == dict:
            self.transitions = transitions

    def __str__(self):
        return ("<TreeBDFT>\n"
                f"states: {self.states}\n"
                f"alphabet: {self.alph}\n"
                f"finals: {self.finals}\n"
                f"transitions:\n{pformat(self.transitions)}")

    def _delta_dict(self, transitions):
        """Convert transition list of form (state_list, symbol, nextstate)
        to dictionary of form {(state_list, symbol): nextstate}."""
        return {(tuple(statelist), symbol): (nextstate, varleaftree)
                for (statelist, symbol, nextstate, varleaftree) in transitions}

    @staticmethod
    def _sub_variables(varleaftree, trees):
        """Replace variables in variably leafed tree with trees with the
        output subtrees of a node's children."""
        if isinstance(varleaftree.data, int):
            return trees[varleaftree.data]
        elif varleaftree.depth() == 0:
            return varleaftree
        else:
            return Tree(varleaftree.data,
                        [TreeBDFT._sub_variables(c, trees)
                         for c in varleaftree.children])

    def _process(self, intree, debug=False):
        """Return the current state and output tree for the given input tree,
        if any, else None."""
        if intree.depth == 0:
            child_states = ()
            child_trees = ()
        else:
            child_states_trees = [self._process(c, debug=debug) for c in intree.children]
            child_states = tuple(state for state, tree in child_states_trees)
            child_trees = tuple(tree for state, tree in child_states_trees)

        if debug:
            print(child_states, intree.data)

        try:
            next_state, varleaftree = self.transitions[(child_states, intree.data)]
        except KeyError:
            return None, None

        outtree = self._sub_variables(varleaftree, child_trees)
        return next_state, outtree

    def transform(self, intree, debug=False):
        """Return the resulting value of processing an input tree if the
        resulting state is a valid final state, else None."""
        state, outtree = self._process(intree, debug)
        return outtree if state in self.finals else None


def test():
    """
    Test TreeBDFA that reverses the a^n b^n tree set.
    """
    test_alph = {'a', 'b', 'S'}
    test_states = {'qa', 'qb', 'qS'}
    test_finals = {'qS'}
    test_trans = {
        ((), 'a'): ('qa', Tree('a')),
        ((), 'b'): ('qb', Tree('b')),
        (('qa', 'qb'), 'S'): ('qS', Tree.from_list(['S', 1, 0])),
        (('qa', 'qS', 'qb'), 'S'): ('qS', Tree.from_list(['S', 2, 1, 0]))}
    test_tbdft = TreeBDFT(test_states, test_alph, test_finals, test_trans)

    ta = Tree('a')
    tb = Tree('b')
    t1 = Tree('S', [ta, tb])
    t2 = Tree('S', [ta, t1, tb])
    t3 = Tree('S', [ta, t2, tb])
    t3x = Tree('S', [ta, tb, t2])

    for t in [ta, tb, t1, t2, t3, t3x]:
        print(test_tbdft.transform(t))


if __name__ == "__main__":
    test()
