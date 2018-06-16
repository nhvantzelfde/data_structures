
class Node(object):
    """ Node class, for use in binary search trees.

    Nodes hold a key value and contain pointers to connected nodes (parent, children).
    All Node pointers and attributes must be maintained by the tree itself.

    Attributes:
        key = the key contained in this node
        parent = the node's parent
        left = the node's left child
        right = the node's right child
        height = the node's height in the tree, where leaf.height = 0; for use in AVL trees
    """
    
    def __init__(self, k = None):
        """ Initializes a new Node, with optional key k. """
        self.key = k
        self.parent = None
        self.left = None
        self.right = None
        self.height = None

    def children(self):
        """ Returns the number of children of this Node. """
        children = 0
        if self.left: children += 1
        if self.right: children += 1
        return children
        
    def __str__(self):
        """ Returns a string representation of this Node. """
        return "node: key = " + str(self.key) + ", # of children = " + str(self.children())

class BST(object):
    """ Binary search tree.

    Builds and maintains a tree of Nodes from given keys. This class is not self-balancing but subclasses can be.
    Representation invariant is that, for all nodes, key of the left child <= node's key <= key of the right child.

    Attributes:
        _r = root node of the search tree
    """
    
    def __init__(self):
        """ Initializes an empty BST. """
        self._r = None

    def insert(self, new):
        """ Inserts a new Node into the tree. Duplicate keys are ignored. """
        node = self._r
        
        if node == None:
            self._r = new
            new.parent = None
            return
        
        while True:
            if new.key < node.key:
                if node.left == None:
                    node.left = new
                    new.parent = node
                    break
                else: node = node.left
            elif new.key > node.key:
                if node.right == None:
                    node.right = new
                    new.parent = node
                    break
                else: node = node.right
            else:
                break # duplicate key, do nothing

        self.__checkRep()

    def delete(self, node):
        """ Deteles a node from the tree. """
        if not node: return

        if node.left == None:
            self._transplant(node,node.right)
            if node.right:
                result = node.right
            else: result = node.parent
        elif node.right == None:
            self._transplant(node,node.left)
            result = node.left
        else:
            suc = self._subtreeMinimum(node.right)

            if suc.right: result = suc.right
            else: result = suc
            
            if suc.parent != node:
                if suc.right:
                    result = suc.right
                else:
                    result = suc.parent
                
                self._transplant(suc,suc.right)
                suc.right = node.right
                suc.right.parent = suc 
            self._transplant(node,suc)
            suc.left = node.left
            suc.left.parent = suc
            
        self.__checkRep()

        return result

    def search(self, key):
        """ Returns a Node with given key, or None if no such Node exists in the tree. """
        node = self._r

        while node:
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return node
            
    def successor(self, node):
        """ Returns the Node with the next largest key to the given node, or None if no such Node exists. """
        if not node: return None
        if node.right:
            return self._subtreeMinimum(node.right)
        else:
            p = node.parent
            while p:
                if p.left == node:
                    return p
                node, p = p, p.parent
            return p

    def predecessor(self, node):
        """ Returns the Node with the next smallest key to the given node, or None if no such Node exists. """
        if not node: return None
        if node.left:
            return self._subtreeMaximum(node.left)
        else:
            p = node.parent
            while p:
                if p.right == node:
                    return p
                node, p = p, p.parent
            return p

    def inorderWalk(self):
        """ Returns an (sorted) array of elements from an in-order walk of the BST. """
        arr = []
        self._subtreeWalk(self._r, arr)
        return arr

    def minimum(self):
        """ Returns the Node with the minimum key in the BST. """
        return self._subtreeMinimum(self._r)

    def maximum(self):
        """ Returns the Node with the maximum key in the BST. """
        return self._subtreeMaximum(self._r)

    def height(self):
        """ Returns the height of the root node. Note that height of a leaf is 0. This takes O(n) to calculate in this class. """
        return self._height(self._r)

    def _subtreeMinimum(self, node):
        """ Returns the Node with the minimum key in the subtree rooted at node. """
        while node and node.left:
            node = node.left
        return node

    def _subtreeMaximum(self, node):
        """ Returns the Node with the maximum key in the subtree rooted at node. """
        while node and node.right:
            node = node.right
        return node

    def _subtreeWalk(self, node, arr):
        """ Appends the values of the keys in the subtree rooted at node to the passed array. Modifies the array in place. """
        if not node: return
        else:
            self._subtreeWalk(node.left, arr)
            arr.append(node.key)
            self._subtreeWalk(node.right, arr)
    
    def _transplant(self, n1, n2):
        """ Puts Node n2 in Node n1's current spot in the tree, effectively removing n1. Used for delete. """
        p = n1.parent
        
        if p == None: self._r = n2
        elif p.left == n1: p.left = n2
        else: p.right = n2

        if n2: n2.parent = p
        
    def _height(self, node):
        """ Returns the height of a given node. Note that the height of a leaf is 0. """
        if not node: return -1
        return 1 + max(self._height(node.left),self._height(node.right))

    def _strHelper(self, str_arr, node, depth, max_depth, leaf_width = 4):
        """ Used recursively to create a properly formatted string with elements in correct columns. """
        if depth >= max_depth:
            return 0

        if not node:
            if depth < max_depth - 1:
                width = self._strHelper(str_arr, None, depth+1, max_depth, leaf_width)
                curr_depth = depth + 1
                while curr_depth < max_depth:
                    str_arr[curr_depth] += " "
                    curr_depth += 1
                width += 1
                width += self._strHelper(str_arr, None, depth+1, max_depth, leaf_width)
            else: width = leaf_width
            str_arr[depth] += ''.join([" "] * width)
            return width

        if depth < max_depth - 1:    
            width = self._strHelper(str_arr, node.left, depth+1, max_depth, leaf_width)
            curr_depth = depth + 1
            while curr_depth < max_depth:
                str_arr[curr_depth] += " "
                curr_depth += 1
            width += 1
            width += self._strHelper(str_arr, node.right, depth+1, max_depth, leaf_width)
        else: width = leaf_width

        curr_str = str(node.key)

        while len(curr_str) <= width - 2:
            curr_str = " " + curr_str + " "
        if len(curr_str) < width:
            curr_str += " "

        str_arr[depth] += curr_str
        return width
        
    def __str__(self):
        """ Returns a string representation of the BST. """
        str_arr = [""] * (self.height() + 1)
        self._strHelper(str_arr, self._r, 0, len(str_arr))
        output = ""
        for i, s in enumerate(str_arr):
            if i != 0:
                output += '\n'
            output += s
            
        return output

    def __checkRep(self):
        """ Recursively checks whether each Node meets the rep invariant (i.e. node.left.key <= node.key <= node.right.key). For debugging. """
        if False: # set to True for debugging
            self.__checkNodeRep(self._r)
        
    def __checkNodeRep(self, node):
        """ Checks whether each and its children meet the rep invariant. For debugging. """
        if not node: return

        if node.left and node.left.parent != node:
            print "Rep error: parent pointers"
        if node.right and node.right.parent != node:
            print "Rep error: parent pointers"

        if node.left and node.left.key >= node.key:
            print "Rep error: left subtree key"
        if node.right and node.right.key <= node.key:
            print "Rep error: right subtree key"

        self.__checkNodeRep(node.left)
        self.__checkNodeRep(node.right)
