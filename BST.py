
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
        r = root node of the search tree
    """
    
    def __init__(self):
        """ Initializes an empty BST. """
        self.r = None

    def insert(self, new):
        """ Inserts a new Node into the tree. Duplicate keys are ignored. """
        node = self.r
        
        if node == None:
            self.r = new
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

        self.__checkBSTRep()

    def delete(self, node):
        """ Deteles a node from the tree. """
        if not node: return

        if node.left == None:
            self.__transplant(node,node.right)
            if node.right:
                result = node.right
            else: result = node.parent
        elif node.right == None:
            self.__transplant(node,node.left)
            result = node.left
        else:
            suc = self.__subtreeMinimum(node.right)

            if suc.right: result = suc.right
            else: result = suc
            
            if suc.parent != node:
                if suc.right:
                    result = suc.right
                else:
                    result = suc.parent
                
                self.__transplant(suc,suc.right)
                suc.right = node.right
                suc.right.parent = suc 
            self.__transplant(node,suc)
            suc.left = node.left
            suc.left.parent = suc
            
        self.__checkBSTRep()

        return result

    def search(self, key):
        """ Returns a Node with given key, or None if no such Node exists in the tree. """
        node = self.r

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
            return self.__subtreeMinimum(node.right)
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
            return self.__subtreeMaximum(node.left)
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
        self.__subtreeWalk(self.r, arr)
        return arr

    def minimum(self):
        """ Returns the Node with the minimum key in the BST. """
        return self.__subtreeMinimum(self.r)

    def maximum(self):
        """ Returns the Node with the maximum key in the BST. """
        return self.__subtreeMaximum(self.r)

    def height(self):
        """ Returns the height of the root node. Note that height of a leaf is 0. This takes O(n) to calculate in this class. """
        return self.__height(self.r)

    def __subtreeMinimum(self, node):
        """ Returns the Node with the minimum key in the subtree rooted at node. """
        while node and node.left:
            node = node.left
        return node

    def __subtreeMaximum(self, node):
        """ Returns the Node with the maximum key in the subtree rooted at node. """
        while node and node.right:
            node = node.right
        return node

    def __subtreeWalk(self, node, arr):
        """ Appends the values of the keys in the subtree rooted at node to the passed array. Modifies the array in place. """
        if not node: return
        else:
            self.__subtreeWalk(node.left, arr)
            arr.append(node.key)
            self.__subtreeWalk(node.right, arr)
    
    def __transplant(self, n1, n2):
        """ Puts Node n2 in Node n1's current spot in the tree, effectively removing n1. Used for delete. """
        p = n1.parent
        
        if p == None: self.r = n2
        elif p.left == n1: p.left = n2
        else: p.right = n2

        if n2: n2.parent = p
        
    def __height(self, node):
        """ Returns the height of a given node. Note that the height of a leaf is 0. """
        if not node: return -1
        return 1 + max(self.__height(node.left),self.__height(node.right))

    def __checkBSTRep(self):
        """ Recursively checks whether each Node meets the rep invariant (i.e. node.left.key <= node.key <= node.right.key). For debugging. """
        if False: # set to True for debugging
            self.__checkNodeRep(self.r)
        
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

    def __strHelper(self, str_arr, node, depth, max_depth, leaf_width = 4):
        """ Used recursively to create a properly formatted string with elements in correct columns. """
        if depth >= max_depth:
            return 0

        if not node:
            if depth < max_depth - 1:
                width = self.__strHelper(str_arr, None, depth+1, max_depth, leaf_width)
                curr_depth = depth + 1
                while curr_depth < max_depth:
                    str_arr[curr_depth] += " "
                    curr_depth += 1
                width += 1
                width += self.__strHelper(str_arr, None, depth+1, max_depth, leaf_width)
            else: width = leaf_width
            str_arr[depth] += ''.join([" "] * width)
            return width

        if depth < max_depth - 1:    
            width = self.__strHelper(str_arr, node.left, depth+1, max_depth, leaf_width)
            curr_depth = depth + 1
            while curr_depth < max_depth:
                str_arr[curr_depth] += " "
                curr_depth += 1
            width += 1
            width += self.__strHelper(str_arr, node.right, depth+1, max_depth, leaf_width)
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
        self.__strHelper(str_arr, self.r, 0, len(str_arr))
        output = ""
        for i, s in enumerate(str_arr):
            if i != 0:
                output += '\n'
            output += s
            
        return output
