#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prettytable import PrettyTable


class Tree:
    def __init__(self, data, children=None):
        """
        Construct a tree consisting of a single node with the given data,
        assumed to be a string. Children may optionally be provided as
        a list of subtrees.
        """
        self.data = data
        if children is None:
            children = []
        self.children = children

    @staticmethod
    def from_list(nodes):
        """
        Construct tree from list of form [label, child1, child2, ...].
        Brackets around terminal nodes may be omitted, similar to LISP
        S-expressions.
        """
        if not isinstance(nodes, list):
            nodes = [nodes]
        if len(nodes) < 1:
            raise ValueError("Tree level cannot be empty.")
        elif len(nodes) == 1:
            return Tree(nodes[0])
        else:
            parent = nodes.pop(0)

            return Tree(parent, [Tree.from_list(n) for n in nodes])

    def __str__(self):
        if len(self.children) > 0:
            return "{}[{}]".format(self.data, ', '.join(str(c) for c in self.children))
        else:
            return str(self.data)

    __repr__ = __str__

    def __eq__(self, other):
        return (self.data == other.data
                and len(self.children) == len(other.children)
                and all(c == d for c, d in zip(self.children, other.children)))

    # def pformat(self):
    #     if len(self.children) > 0:
    #         return str([str(self.data)] + [c.pformat() for c in self.children])
    #     else:
    #         return str(self.data)

    def add_subtree(self, subtree):
        """
        Add given subtree as the last child of this tree.
        """
        self.children.append(subtree)

    def size(self):
        """
        Return the number of nodes contained in the tree.
        """
        return 1 + sum(c.size() for c in self.children)

    def yld(self):
        """
        Return the string formed by concatenating all leaf nodes in the tree.
        """
        if len(self.children) > 0:
            return ''.join(c.yld() for c in self.children)
        else:
            return self.data

    def depth(self):
        """
        Return the depth of the tree, where a single root node has depth 0
        and each additional level adds 1 to the depth.
        """
        if len(self.children) > 0:
            return 1 + max(c.depth() for c in self.children)
        else:
            return 0

    def width(self):
        """
        Return width of the tree, defined as the largest number of children
        of any node in the tree, or 0 in the case of a single root node.
        """
        if len(self.children) > 0:
            return max(len(self.children), max(c.width() for c in self.children))
        else:
            return 0

    def get_gorn(self, addr):
        """
        Return subtree at given gorn address, given as a list of non-negative
        integers. Return None if address not found.
        """
        if len(addr) > 0:
            i = addr.pop(0)
            if i in range(len(self.children)):
                return self.children[i].get_gorn(addr)
            else:
                return None
        else:
            return self


# TESTING

a = Tree('a')      # this creates a leaf labeled 'a'
b = Tree('b')      # this creates a leaf labeled 'b'
s1 = Tree('S')     # this creates a leaf labeled 'S'
s1.add_subtree(a)  # This adds leaf a as the first (leftmost) subtree of s1.
s1.add_subtree(b)  # This adds leaf b as the second subtree of s1.


def sn(n):
    """
    Generate a tree of depth n whose yield gives a string of the language a^nb^n
    """
    previous_t = s1
    for i in range(n-1):
        t = Tree('S')
        t.add_subtree(a)
        t.add_subtree(previous_t)
        t.add_subtree(b)
        previous_t = t
    return previous_t


def test():
    """
    Test Tree class by creating trees for the a^nb^n language of various sizes.
    Print results in tabular format.
    """
    t = Tree.from_list(['a', ['b', ['c', 'd'], ['e', 'f', 'g', 'h', 'i']]])

    test_trees = [sn(1), sn(4), t]

    table = PrettyTable(["Input", "Size", "Depth", "Width", "Yield"],
                        align='l')
    for i, t in enumerate(test_trees):
        name = f"{i+1}. {t}"
        s = t.size()
        d = t.depth()
        w = t.width()
        y = t.yld()
        table.add_row([name, s, d, w, y])

    print(table)


if __name__ == "__main__":
    test()
