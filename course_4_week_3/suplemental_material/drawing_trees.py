"""
Python definition of basic Tree class

IMPORTANT:  Some class methods assume that instances of the Tree class
always have a single parent (or no parent for the root). See problem #8
on homework #3 for more details.
"""


class Tree:
    """
    Recursive definition for trees plus various tree methods
    """

    def __init__(self, value, children):
        """
        Create a tree whose root has specific value (a string)
        Children is a list of references to the roots of the subtrees.  
        """

        self._value = value
        self._children = children

    def __str__(self):
        """
        Generate a string representation of the tree
        Use an pre-order traversal of the tree
        """

        ans = "["
        ans += str(self._value)

        for child in self._children:
            ans += ", "
            ans += str(child)
        return ans + "]"

    def get_box_size(self, tree):
        """
        Recursive function to compute height and width
        of the bounding box for a tree
        """
        current_subtree_widths = 0
        tree_height = 0
        for child in tree.children():
            child_width, child_height = self.get_box_size(child)
            current_subtree_widths += child_width
            tree_height = max(tree_height, child_height)
        subtree_width = max(NODE_WIDTH, current_subtree_widths)
        tree_height = NODE_HEIGHT + tree_height
        return subtree_width, tree_height

    def get_value(self):
        """
        Getter for node's value
        """
        return self._value

    def children(self):
        """
        Generator to return children
        """
        for child in self._children:
            yield child

    def num_nodes(self):
        """
        Compute number of nodes in the tree
        """
        ans = 1
        for child in self._children:
            ans += child.num_nodes()
        return ans

    def num_leaves(self):
        """
        Count number of leaves in tree
        """
        if len(self._children) == 0:
            return 1

        ans = 0
        for child in self._children:
            ans += child.num_leaves()
        return ans

    def height(self):
        """
        Compute height of a tree rooted by self
        """
        height = 0
        for child in self._children:
            height = max(height, child.height() + 1)
        return height


def run_examples():
    """
    Create some trees and apply various methods to these trees
    """
    tree_a = Tree("a", [])
    tree_b = Tree("b", [])
    print "Tree consisting of single leaf node labelled 'a'", tree_a
    print "Tree consisting of single leaf node labelled 'b'", tree_b

    tree_cab = Tree("c", [tree_a, tree_b])
    print "Tree consisting of three node", tree_cab

    tree_dcabe = Tree("d", [tree_cab, Tree("e", [])])
    print "Tree consisting of five nodes", tree_dcabe
    print

    my_tree = Tree("a", [Tree("b", [Tree("c", []), Tree("d", [])]),
                         Tree("e", [Tree("f", [Tree("g", [])]), Tree("h", []), Tree("i", [])])])
    print "Tree with nine nodes", my_tree

    print "The tree has", my_tree.num_nodes(), "nodes,",
    print my_tree.num_leaves(), "leaves and height",
    print my_tree.height()

    #import poc_draw_tree
    # poc_draw_tree.TreeDisplay(my_tree)


# run_examples()
