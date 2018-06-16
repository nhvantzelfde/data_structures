from BST import BST, Node

class AVL(BST):
    """ AVL self-balancing tree. Inherits from BST.

    AVL rep. invariant is that, for every node, height of left child and right child differ by no more than 1.
    Guarantees the height is no more than ~1.44 * lg n, so all major operations function in O(lg n).
    Augments Nodes to maintain their heights, so that __height and height work in O(1) time.
    Rotates nodes after insertions and deletions as necessary to maintain the AVL rep. invariant.

    Attributes:
        none, apart from parent
    """

    def insert(self, new):
        """ Inserts a given Node into the tree. """
        # insert into BST
        super(AVL, self).insert(new)
        self._updateHeight(new)

        # restore AVL property, working up the tree
        self._fixAVL(new.parent)

        self.__checkRep()
    
    def delete(self, node):
        """ Deletes a given Node from the tree. """
        if not node: return

        # insert into BST
        suc = super(AVL, self).delete(node)

        # restore AVL property, working up the tree
        self._fixAVL(suc)

        self.__checkRep()

    def _fixAVL(self, node):
        """ Fixes the AVL property of the tree, updating node heights and making rotations as necessary. """
        while node:
            if abs(self._height(node.left) - self._height(node.right)) <= 1:
                # AVL property is met; no rotates needed
                self._updateHeight(node)
            elif self._height(node.left) > self._height(node.right):
                # left-heavy tree
                l_child = node.left
                if l_child and self._height(l_child.right) > self._height(l_child.left):
                    # left child is right-heavy
                    self._rotateLeft(l_child)
                self._rotateRight(node)
            else:
                # right-heavy tree
                r_child = node.right
                if r_child and self._height(r_child.left) > self._height(r_child.right):
                    # right child is left-heavy, first rotate that right
                    self._rotateRight(r_child)
                self._rotateLeft(node)

            node = node.parent
        
    def _rotateLeft(self, node):
        """ Rotates the given node to the left, fixing subtrees as required. """
        # new parent of node
        new_p = node.right

        # update parent
        new_p.parent = node.parent
        if not new_p.parent:
            self._r = new_p
        else:
            if new_p.parent.left == node:
                new_p.parent.left = new_p
            else:
                new_p.parent.right = new_p

        # move new_p's left to node's right
        node.right = new_p.left
        if node.right:
            node.right.parent = node

        # set node as new_p's left
        new_p.left = node
        node.parent = new_p

        # update heights
        self._updateHeight(node)
        self._updateHeight(new_p)

    def _rotateRight(self, node):
        """ Rotates the given node to the right, fixing subtrees as required. """
        # new parent of node
        new_p = node.left

        # update parent
        new_p.parent = node.parent
        if not new_p.parent:
            self._r = new_p
        else:
            if new_p.parent.left == node:
                new_p.parent.left = new_p
            else:
                new_p.parent.right = new_p

        # move new_p's right to node's left
        node.left = new_p.right
        if node.left:
            node.left.parent = node

        # set node as new_p's right
        new_p.right = node
        node.parent = new_p

        # update heights
        self._updateHeight(node)
        self._updateHeight(new_p)

    def height(self):
        """ Returns the height of the tree. Note that the height of a leaf is 0. This takes O(1) time. """
        return self._height(self._r)
        
    def _height(self, node):
        """ Returns the height of a given Node. Note that the height of a leaf is 0. """
        if not node:
            return -1
        else:
            return node.height
        
    def _updateHeight(self, node):
        """ Updates the height of a given Node, using children's heights. """
        if not node: return
        else:
            node.height = 1 + max(self._height(node.left), self._height(node.right))

    def __checkRep(self):
        """ Recursively checks whether each node meets the AVL rep. invariant (|left.height - right-height| <= 1). """
        if False: # set to True for debugging
            self.__checkHeightRep(self._r)
        
    def __checkHeightRep(self, node):
        """ Checks whether a Node and its children meet the AVL rep. invariant. For debugging purposes. """
        if not node: return

        if self._height(node) != 1 + max(self._height(node.left), self._height(node.right)):
            print "Rep error: height not equal to [max(children) + 1]; node =", node

        if abs(self._height(node.left) - self._height(node.right)) > 1:
            print "Rep error: height of children differs by more than 1; node =", node

        self.__checkHeightRep(node.left)
        self.__checkHeightRep(node.right)
