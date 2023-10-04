# import binarytree

# Binary tree node for Tree sort algorithm


class Node:

    def __init__(self, value=None) -> None:
        self.value = value
        self.left, self.right = None, None

# return root node of binary tree


def root() -> Node:
    return Node()
