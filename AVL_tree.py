from BST import BST
from BST import Node
from BST import randomTest
# from BST import compare
import math
import random

class AVL(BST):
    def insert(self, new):
        # insert into BST
        super(AVL, self).insert(new)
        self.__updateHeight(new)

        # restore AVL property, working up the tree
        self.__fixAVL(new.parent)

        self.__checkAVLRep()
    
    def delete(self, node):
        if not node: return

        #print "delete, node=", node
        #print "tree before"
        #print self
        
        # insert into BST
        suc = super(AVL, self).delete(node)

        #print "successor =", suc
        #print "tree after"
        #print self
        
        # restore AVL property, working up the tree
        
        self.__fixAVL(suc)

        #print "tree fixed"
        #print self

        self.__checkAVLRep()

    def __fixAVL(self, node):
        while node:
            if abs(self.__height(node.left) - self.__height(node.right)) <= 1:
                # AVL property is met; no rotates needed
                self.__updateHeight(node)
            elif self.__height(node.left) > self.__height(node.right):
                # left-heavy tree
                l_child = node.left
                if l_child and self.__height(l_child.right) > self.__height(l_child.left):
                    # left child is right-heavy
                    self.__rotateLeft(l_child)
                self.__rotateRight(node)
            else:
                # right-heavy tree
                r_child = node.right
                if r_child and self.__height(r_child.left) > self.__height(r_child.right):
                    # right child is left-heavy, first rotate that right
                    self.__rotateRight(r_child)
                self.__rotateLeft(node)

            node = node.parent
        
    def __rotateLeft(self, node):
        # new parent of node
        new_p = node.right

        # update parent
        new_p.parent = node.parent
        if not new_p.parent:
            self.r = new_p
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
        self.__updateHeight(node)
        self.__updateHeight(new_p)

    def __rotateRight(self, node):
        # new parent of node
        new_p = node.left

        # update parent
        new_p.parent = node.parent
        if not new_p.parent:
            self.r = new_p
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
        self.__updateHeight(node)
        self.__updateHeight(new_p)
 
    def __height(self, node):
        if not node:
            return -1
        else:
            return node.height
        
    def __updateHeight(self, node):
        if not node: return
        else:
            node.height = 1 + max(self.__height(node.left), self.__height(node.right))

    def __checkAVLRep(self):
        if True: # set to True for debugging
            self.__checkHeightRep(self.r)
        
    def __checkHeightRep(self, node):
        if not node: return

        if self.__height(node) != 1 + max(self.__height(node.left), self.__height(node.right)):
            print "Rep error: height not equal to [max(children) + 1]; node =", node

        if abs(self.__height(node.left) - self.__height(node.right)) > 1:
            print "Rep error: height of children differs by more than 1; node =", node

        self.__checkHeightRep(node.left)
        self.__checkHeightRep(node.right)

        

def main():
    for i in range(30):
        tree = AVL()
        passed = randomTest(tree, 1000)
        
        if passed:
            height = tree.height()
            arr = tree.inorderWalk()
            max_height = 1.44 * math.log(len(arr),2) - 1
            if height > max_height:
                s = "but height exceeded expectations: "
            else:
                s = "and height within expectations: "
            s += "actual " + str(height) + " vs. expected " + str(max_height)
            print "Passed test", i+1, s
    
    tree = AVL()
    ar = []
    for i in range(16):
        v = random.randint(-99,99)
        if v not in ar:
            tree.insert(Node(v))
            ar.append(v)
    ar.sort()

    print "Height =", tree.height()
    print "Max. expected height =", 1.44 * math.log(len(ar)+1,2) - 1
    print "Minimum =", tree.minimum()
    print "Maximum =", tree.maximum()
    print "In-order Walk =", tree.inorderWalk()
    print "Array =", ar
    print "Tree ="
    print tree

    for i in range(3):
        index = random.randint(0,len(ar)-1)
        v = ar[index]
        tree.delete(tree.search(v))
        ar.remove(v)

    print "Height =", tree.height()
    print "Max. expected height =", 1.44 * math.log(len(ar)+1,2) - 1
    print "Minimum =", tree.minimum()
    print "Maximum =", tree.maximum()
    print "In-order Walk =", tree.inorderWalk()
    print "Array =", ar
    print "Tree ="
    print tree

  

if __name__ == "__main__":
    main()
