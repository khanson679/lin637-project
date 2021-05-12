#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pprint import pformat

from tree import Tree


class TreeBDFA:
    """Bottom Up Deterministic Finite-state Acceptors for Trees.

    A simple implementation of bottom-up DFAs over trees.

    Parameters
    ----------
    states: set of states
    alphabet: set of symbols
    finals: set of final states
    transitions: dictionary of the form
      {(children_state_list, parent_symbol): parent_state}

    All sets may be alternatively provided as lists, in which case they will
    be converted automatically. The transition dictionary may likewise be
    provided as a set or list of tuples.
    """

    def __init__(self, states, alphabet, finals, transitions):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.finals = set(finals)

        if type(transitions) in (set, list):
            self.transitions = self._delta_dict(transitions)
        elif type(transitions) == dict:
            self.transitions = transitions

    def __str__(self):
        return ("<TreeBDFA>\n"
                f"states: {self.states}\n"
                f"alphabet: {self.alphabet}\n"
                f"finals: {self.finals}\n"
                f"transitions:\n{pformat(self.transitions)}")

    def _delta_dict(self, transitions):
        """Convert transition list of form (state_list, symbol, nextstate)
        to dictionary of form {(state_list, symbol): nextstate}."""
        return {(tuple(state_list), symbol): nextstate
                for (state_list, symbol, nextstate) in transitions}

    def is_valid(self):
        """Return True if every state and symbol in every transition
        exists in the states and alphabet, False otherwise."""
        return all(all(state in self.states for state in state_list)
                   and symbol in self.alphabet
                   and nextstate in self.states
                   for (state_list, symbol), nextstate in self.transitions.items())

    def _process(self, subtree, debug=False):
        """Return the state reached by processing the given tree, if any,
        None otherwise."""
        if len(subtree.children) == 0:
            statelist = ()
        else:
            statelist = tuple(self._process(c, debug=debug) for c in subtree.children)
        if debug:
            print(statelist)
        return self.transitions.get((statelist, subtree.data), None)

    def recognizes(self, tree, debug=False):
        """Processes a tree and returns True if a final state is reached,
        False otherwise."""
        return self._process(tree, debug) in self.finals


def test():
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

    test_trees = [t1, t2, t3, t3x]

    # print results

    print(f"anbn:\n{anbn}")
    print()

    for t in test_trees:
        print(t)
    print()

    print(f"anbn is valid: {anbn.is_valid()}")
    print()
    print(f"anbn recognizes t1: {anbn.recognizes(t1)}")
    print(f"anbn recognizes t2: {anbn.recognizes(t2)}")
    print(f"anbn recognizes t3: {anbn.recognizes(t3)}")
    print(f"anbn recognizes t3x: {anbn.recognizes(t3x)}")
    print()


if __name__ == "__main__":
    test()
