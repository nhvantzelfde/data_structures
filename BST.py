
class Node(object):
    def __init__(self, k = None):
        self.key = k
        self.parent = None
        self.left = None
        self.right = None

    def children(self):
        children = 0
        if self.left: children += 1
        if self.right: children += 1
        return children
        
    def __str__(self):
        return "Node: key = " + str(self.key) + ", # of children = " + str(self.children())

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
        return self.__subtreeWalk(self.r)

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

    def __subtreeWalk(self, node):
        if node == None: return []
        return self.__subtreeWalk(node.left) + [node.key] + self.__subtreeWalk(node.right)
    
    def __transplant(self, n1, n2):
        p = n1.parent
        
        if p == None: self.r = n2
        elif p.left == n1: p.left = n2
        else: p.right = n2

        if n2: n2.parent = p

    def __nodeHeight(self, node):
        if node == None: return -1
        return 1 + max(self.__nodeHeight(node.left),self.__nodeHeight(node.right))
        
    def __checkRep(self, node):
        if True:
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

    def __depthArray(self, node, depth, arr):
        if len(arr) <= depth:
            arr.append([])
        if not node:
            arr[depth].append(None)
        else:
            arr[depth].append(node.key)
            self.__depthArray(node.left, depth+1, arr)
            self.__depthArray(node.right, depth+1, arr)

        
    def __str__(self):
        arr = []
        self.__depthArray(self.r, 0, arr)
        return str(arr)

    
def treeFromArray(arr):
    """ Creates a BST from the keys in a given array.
    type arr: List[]
    rtype: BST
    """
    tree = BST()
    for k in arr:
        tree.insert(Node(k))
    return tree
    
def main():
    arr = [21, 45, 1, 34, 8, -1, 100, -54, 60, 2]
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
    # print(tree.r.right.right.left)

if __name__ == "__main__":
    main()
    
        
    
        


        
