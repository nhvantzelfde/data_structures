import random

class Node(object):
    def __init__(self, k = None):
        self.key = k
        self.parent = None
        self.left = None
        self.right = None
        self.height = None # for use in AVL trees, not used in BST implementation

    def children(self):
        children = 0
        if self.left: children += 1
        if self.right: children += 1
        return children
        
    def __str__(self):
        return "node: key = " + str(self.key) + ", # of children = " + str(self.children())

class BST(object):
    def __init__(self, root = None):
        self.r = root

    def insert(self, new):
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
                # duplicate key, do nothing
                break

        self.__checkRep(self.r)

    def delete(self, node):
        if not node: return

        if node.left == None: self.__transplant(node,node.right)
        elif node.right == None: self.__transplant(node,node.left)
        else:
            suc = self.__subtreeMinimum(node.right)
            if suc.parent != node:
                self.__transplant(suc,suc.right)
                suc.right = node.right
                suc.right.parent = suc
            self.__transplant(node,suc)
            suc.left = node.left
            suc.left.parent = suc

        self.__checkRep(self.r)

    def search(self, key):
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
        arr = []
        self.__subtreeWalk(self.r, arr)
        return arr

    def minimum(self):
        return self.__subtreeMinimum(self.r)

    def maximum(self):
        return self.__subtreeMaximum(self.r)

    def height(self):
        return self.__nodeHeight(self.r)

    def __subtreeMinimum(self, node):
        while node and node.left:
            node = node.left
        return node

    def __subtreeMaximum(self, node):
        while node and node.right:
            node = node.right
        return node

    def __subtreeWalk(self, node, arr):
        if not node: return
        else:
            self.__subtreeWalk(node.left, arr)
            arr.append(node.key)
            self.__subtreeWalk(node.right, arr)
    
    def __transplant(self, n1, n2):
        p = n1.parent
        
        if p == None: self.r = n2
        elif p.left == n1: p.left = n2
        else: p.right = n2

        if n2: n2.parent = p

    def __nodeHeight(self, node):
        if not node: return -1
        return 1 + max(self.__nodeHeight(node.left),self.__nodeHeight(node.right))
        
    def __checkRep(self, node):
        if False: # set to True for debugging
            if not node: return

            if node.left and node.left.parent != node:
                print "Rep error: parent pointers"
            if node.right and node.right.parent != node:
                print "Rep error: parent pointers"

            if node.left and node.left.key >= node.key:
                print "Rep error: left subtree key"
            if node.right and node.right.key <= node.key:
                print "Rep error: right subtree key"

            self.__checkRep(node.left)
            self.__checkRep(node.right)

    def __strHelper(self, str_arr, node, depth, max_depth, leaf_width = 4):
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
        str_arr = [""] * (self.height() + 1)
        self.__strHelper(str_arr, self.r, 0, len(str_arr))
        output = ""
        for i, s in enumerate(str_arr):
            if i != 0:
                output += '\n'
            output += s
            
        return output
                                 
def treeFromArray(arr):
    """ Creates a BST from the keys in a given array.
    type arr: List[]
    rtype: BST
    """
    tree = BST()
    for k in arr:
        tree.insert(Node(k))
    return tree

def randomTest(count):
    passed = True
    arr = []
    tree = BST()

    i = 0
    while i < count:
        v = random.randint(-999,999)
        if v not in arr:
            arr.append(v)
            tree.insert(Node(v))
            i += 1
            
    arr.sort()
    if not compare(tree, arr):
        printErrorMessage(tree, arr, ", after insertions")
        passed = False

    for i in range(len(arr)//2):
        v = arr[i]
        arr.remove(v)
        n = tree.search(v)
        tree.delete(n)
    
    if not compare(tree, arr):
        printErrorMessage(tree, arr, ", after known deletions")
        passed = False

    for i in range(count//2):
        v = random.randint(-1000,1000)
        if v in arr:
            arr.remove(v)
        n = tree.search(v)
        tree.delete(n)

    if not compare(tree, arr):
        printErrorMessage(tree, arr, ", after random deletions")
        passed = False

    for i in range(count//4):
        v = random.randint(-1000,1000)
        if v not in arr:
            arr.append(v)
            tree.insert(Node(v))
    arr.sort()
    if not compare(tree, arr):
        printErrorMessage(tree, arr, ", after second insertions")
        passed = False

    return passed  
    
def compare(tree, arr):
    arr1 = tree.inorderWalk()
    if len(arr) != len(arr1): return False
    for i in range(len(arr)):
        if arr[i] != arr1[i]: return False
    return True

def printErrorMessage(tree, arr, str = ""):
    print "Failed comparison tests" + str
    print "Tree:"
    print tree
    print "In order walk:"
    print tree.inorderWalk()
    print "Array:"
    print arr
    
def main():
    for i in range(20):
        passed = randomTest(100)
        if passed:
            print "Passed random test", i+1

    tree = BST()
    for i in range(20):
        v = random.randint(-99, 99)
        tree.insert(Node(v))

    print "Height =", tree.height()
    print "Minimum =", tree.minimum()
    print "Maximum =", tree.maximum()
    print "In-order Walk =", tree.inorderWalk()
    print "Tree ="
    print tree

    arr = [21, 45, 1, 34, 8, -1, 99, -54, 60, 2]
    tree = treeFromArray(arr)
    print("Tree:")
    print(tree)
    print("Root:")
    print(tree.r)
    print("In order walk:")
    print(tree.inorderWalk())
    print("Min, max:")
    print(str(tree.minimum()),str(tree.maximum()))

    print("Height = ",tree.height())
    
    print("Successor of 34:")
    n = tree.search(34)
    s = tree.successor(n)
    print(s)

    print("Successor of 100:")
    n = tree.search(100)
    s = tree.successor(n)
    print(s)

    print("Predecessor of 34:")
    n = tree.search(34)
    s = tree.predecessor(n)
    print(s)

    print("Predecessor of -54:")
    n = tree.search(-54)
    s = tree.predecessor(n)
    print(s)
    
    print("Find and delete 34:")
    n = tree.search(34)
    print(n)
    tree.delete(n)
    print(tree.inorderWalk())

    print("Find and delete 21:")
    n = tree.search(21)
    s = tree.successor(n)
    print(n)
    print(s)
    tree.delete(n)
    print(tree.inorderWalk())
    print(tree.r)
    print(tree.r.right)
    print(tree.r.right.parent)

if __name__ == "__main__":
    main()
    
        
    
        


        
