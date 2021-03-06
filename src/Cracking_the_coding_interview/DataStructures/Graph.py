from .Queue import Queue


class Node:

    def __init__(self, value=None, children=[]):
        self.value = value
        self.children = {c for c in children}

    def __str__(self):
        return 'Node({}){}'.format(self.value, [c.value for c in self.children])

    def __repr__(self):
        return str(self)


class Graph:

    def __init__(self, nodes=[]):
        self.nodes = {n for n in nodes}


class Tree:

    def __init__(self, value=None, lchild=None, rchild=None, parent=None):
        self.value = value
        self.lchild = lchild
        self.rchild = rchild
        self.parent = parent

    def children(self):
        return self.lchild, self.rchild

    def __repr__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.children():
            if child is not None:
                ret += child.__repr__(level+1)
        return ret


class BST(Tree):

    def __init__(self, arr=None, value=None, lchild=None, rchild=None):
        if arr is not None:
            tree = self.create_minimal_bst(arr)
            self.value = tree.value
            self.lchild = tree.lchild
            self.rchild = tree.rchild
        else:
            self.value = value
            self.lchild = lchild
            self.rchild = rchild

    def insert(self, value):
        if value > self.value:
            if self.rchild is None:
                self.rchild = BST(value=value)
            else:
                return self.rchild.insert(value)
        elif value < self.value:
            if self.lchild is None:
                self.lchild = BST(value=value)
            else:
                return self.lchild.insert(value)
        else:
            print("Warning, value {} is already in tree".format(value))

    def delete(self, value):
        parent = self.find_parent(value)
        if parent.lchild is not None and parent.lchild.value == value:
            node, attr = parent.lchild, 'lchild'
        elif parent.rchild is not None and parent.rchild.value == value:
            node, attr = parent.rchild, 'rchild'
        else:
            print('Warning: value {} does not exist in Tree'.format(value))
            return

        if node.lchild is None:
            if node.rchild is None:
                setattr(parent, attr, None)
            else:
                setattr(parent, attr, node.rchild)
        else:
            new_value = node.lchild.find_max()
            node.lchild.delete(new_value)
            node.value = new_value

    def find_max(self):
        if self.rchild is None:
            return self.value
        return self.rchild.find_max()

    def find(self, value):
        if self.value == value:
            return self
        if (value < self.value or self.rchild is None) and self.lchild is not None:
            return self.lchild.find(value)
        elif (value > self.value or self.lchild is None) and self.rchild is not None:
            return self.rchild.find(value)
        else:
            return None

    def find_parent(self, value):
        if self.lchild is not None and self.lchild.value == value:
            return self
        elif self.rchild is not None and self.rchild.value == value:
            return self
        elif self.lchild is not None and value < self.value:
            return self.lchild.find_parent(value)
        elif self.rchild is not None and value > self.value:
            return self.rchild.find_parent(value)
        return None

    def create_minimal_bst(self, arr, l_child_size=None):
        """
        Space: O(n)
        Time: O(n)
        :param arr: sorted array
        :param l_child_size: pre-calculated child sizes to squeeze some very minor optimisation
        :return: minimal depth binary search tree
        """

        if len(arr) == 0:
            return None
        if len(arr) == 1:
            return BST(value=arr[0])

        if l_child_size is None:
            l_child_size, n = 0, 0
            while l_child_size < len(arr):
                n += 1
                l_child_size = 2 ** (n + 1) - 1
            l_child_size = 2 ** n - 1
        else:
            l_child_size = (l_child_size + 1) // 2 - 1

        if len(arr) > l_child_size + 1:
            rchild = self.create_minimal_bst(arr[l_child_size + 1:])
        else:
            rchild = None

        return BST(value=arr[l_child_size],
                    lchild=self.create_minimal_bst(arr[:l_child_size], l_child_size=l_child_size),
                    rchild=rchild)

