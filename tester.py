from heap import Heap, MinHeap, MaxHeap
from sorted_array import SortedArray
from hash_table import HashFunction, HashTable
from BST import BST, Node
import random
import datetime

def heapCompare(heap, ar1):
    """
    Compares all elements of a heap with the elements of an array.
    Returns True if identical and False otherwise.
    """
    if len(ar1) != len(heap): return False

    ar1.sort()
    ar2 = heap.keys[:]
    ar2.sort()

    for i in range(len(ar1)):
        if ar1[i] != ar2[i]: return False

    return True
    
def heapRandomTest(size, min_heap):
    """
    Creates a heap of a random size and tests elements versus array with same data.
    Returns True if the heap meets all tests.
    For debugging the Heap class.
    """
    heap = Heap(min_heap)
    ar = []

    # insertions
    for i in range(size):
        k = random.randint(-9999,9999)
        heap.insert(k)
        ar.append(k)   

    if not heapCompare(heap, ar):
        print "Error after insertions: heap =",heap," ar=",ar
        return False
    
    # deletions
    for i in range(size//4):
        index = random.randint(0,len(ar)-1)
        k = ar[index]
        heap.delete(k)
        ar.remove(k)

    if not heapCompare(heap, ar):
        print "Error after deletions: heap =",heap," ar=",ar
        return False
    
    # pops
    ar.sort()
    if heap.isMinHeap():
        ar = ar[::-1]
    for i in range(size//4):
        heap.extract()
        ar.pop()

    if not heapCompare(heap, ar):
        print "Error after pop/extract: heap =",heap," ar=",ar
        return False
    
    # random deletions
    for i in range(size//4):
        k = random.randint(-9999,9999)
        if k in ar:
            ar.remove(k)
        heap.delete(k)
    
    if not heapCompare(heap, ar):
        print "Error after random deletions: heap =",heap," ar=",ar
        return False
    
    # further insertions
    for i in range(size//4):
        k = random.randint(-9999,9999)
        heap.insert(k)
        ar.append(k)
        
    if not heapCompare(heap, ar):
        print "Error after further insertions: heap =",heap," ar=",ar
        return False
    
    return True

def heapRandomSort(size, min_heap):
    """
    Tests heap extractAll method vs sorting an array, after random insertions and deletions.
    Returns True if the heap output is the same as the sorted array, and False otherwise.
    For testing Heap class.
    """
    ar = []
    heap = Heap(min_heap)

    # insertions
    for i in range(size):
        k = random.randint(-9999,9999)
        ar.append(k)
        heap.insert(k)

    # deletions
    for i in range(size//4):
        index = random.randint(0,len(ar)-1)
        k = ar[index]
        ar.remove(k)
        heap.delete(k)

    # sort array and extract array from heap
    ar.sort()
    if heap.isMaxHeap():
        ar.reverse()
    heap_ar = heap.extractAll()
    
    # comparison
    if len(ar) != len(heap_ar): return False
    for i in range(len(ar)):
        if ar[i] != heap_ar[i]: return False

    return True
    
def heapFullTest():
    """
    Various tests for Heap class, using both MinHeaps and MaxHeaps, including sorting and random operations.
    """
    print("Testing MinHeap: sorting")
    for i in range(1,21):
        if heapRandomSort(250, True):
            print "Test",i,"successful"
        else:
            print "Test",i,"failed"

    print("\nTesting MaxHeap: sorting")
    for i in range(1,21):
        if heapRandomSort(250, False):
            print "Test",i,"successful"
        else:
            print "Test",i,"failed"

    print("\nTesting MinHeap: general")
    for i in range(1,21):
        if heapRandomTest(250, True):
            print "Test",i,"successful"
        else:
            print "Test",i,"failed"

    print("\nTesting MaxHeap: general")
    for i in range(1,21):
        if heapRandomTest(250, False):
            print "Test",i,"successful"
        else:
            print "Test",i,"failed"

    print("\nTesting MinHeap: other operations")
    ar = [1, 4, 501, -200, 32, 7, 65, -1, 20000, -34, 17]
    min_heap = MinHeap()
    min_heap.createMinHeap(ar)

    print min_heap.extractMin()
    print min_heap.extractMin()
    print min_heap.extractMin()

    max_heap = MaxHeap()
    max_heap.createMaxHeap(ar)

    print max_heap.extractMax()
    print max_heap.extractMax()
    print max_heap.extractMax()

    print "Max: ar", max(ar), "min_heap", min_heap.maximum(), "max_heap", max_heap.maximum()
    print "Min: ar", min(ar), "min_heap", min_heap.minimum(), "max_heap", max_heap.minimum()

def sortedArrayRandomTest(size):
    """
    Creates a SortedArray object and an normal Python list with random elements of a given size.
    Compares the contents of the two objects after insertions and deletions.
    Returns False if any test shows not equal; otherwise returns True.
    Uses for testing the SortedArray class.
    """
    s_arr = SortedArray()
    ar = []

    # insertions
    for i in range(size):
        n = random.randint(-10000,10000)
        ar.append(n)
        s_arr.insert(n)
    ar.sort()
    if not sortedArrayCompare(s_arr,ar): return False

    # known deletions
    for i in range(size//2):
        index = random.randint(0,len(ar)-1)
        n = ar[i]
        s_arr.delete(n)
        ar.remove(n)
    if not sortedArrayCompare(s_arr,ar): return False

    # random deletions
    for i in range(size//4):
        n = random.randint(-10000,10000)
        if n in ar:
            ar.remove(n)
        s_arr.delete(n)
    if not sortedArrayCompare(s_arr,ar): return False

    # more insertions
    for i in range(size//4):
        n = random.randint(-10000,10000)
        ar.append(n)
        s_arr.insert(n)
    ar.sort()
    if not sortedArrayCompare(s_arr,ar): return False

    # overwrites
    for i in range(size//4):
        index = random.randint(0,len(ar)-1)
        value = random.randint(-10000,10000)
        ar[index] = value
        ar.sort()
        s_arr[index] = value
    if not sortedArrayCompare(s_arr,ar): return False

    return True

def sortedArrayCompare(s_arr, ar):
    """
    Compares a SortedArray s_arr with a normal, pre-sorted Python List. Returns False if any elements of the two are different.
    """
    if len(s_arr) != len(ar): return False
    for i in range(len(ar)):
        if ar[i] != s_arr[i]: return False
    return True 
    
def sortedArrayFullTest():
    """
    Various tests for SortedArray class, including insertion, deletion, and overwrites.
    """
    init = [1, 5, 2, 80, 42, 232, 10, -1]
    adds = [2, 20, 423, 65, 4, 98, -1, 5, 10]
    dels = [42, 232, -1, 5, 2000, -10]
    test = [1, 2, 80, 10, 2, 20, 423, 65, 4, 98, 5, 10, 555]
    test.sort()

    print "\nTesting SortedArray: various operations"
    print "Target sums: init=", sum(init),"after adds=", sum(init)+sum(adds), "test=", sum(test)
    
    s_arr = SortedArray(init)
    print "After initial: s_arr =", s_arr, "sum = ", sum(s_arr)
    for a in adds:
        s_arr.insert(a)
    print "After adds: s_arr =", s_arr, "sum = ", sum(s_arr)

    for d in dels:
        s_arr.delete(d)
    print "After deletes: s_arr =", s_arr, "sum = ", sum(s_arr)

    s_arr[0] = 555

    print "After setting element i: s_arr =", s_arr, "sum = ", sum(s_arr)
    print s_arr.minimum(), s_arr.maximum()
    
    error = False
    for i in range(len(test)):
        if test[i] != s_arr[i]:
            print "Error at index",i," test =", test[i]," s_arr =",s_arr[i]

    print "\nTesting SortedArray: random operations"
    for i in range(20):
        if sortedArrayRandomTest(1000): print "Test",i+1,"successful"
        else: print "Failure at test",i+1

def hashFunctionTest():
    """
    Creates a hash function with a given m and hashes a set number of random integers, printing the number of times each slot is hashed to.
    Used for testing purposes.
    """
    m = 128
    h = HashFunction(m)
    print(h)

    count = [0] * m
    for i in range(m*2):
        count[h.h(random.randint(-10000,10000))] += 1
    print count

def hashTableTest():
    """
    Testing functions for HashTable. Outputs the result of various tests using print.
    """
    ht = HashTable()
    
    keys = [1, 3, 78, 10, 200, 32, 2, 5, 200, 8, 73, 7, 500, 6, 121, 131, 150]
    values = ["Omaha", "Dayton", "Boston", "NYC", "LA", "Chicago", "Baton Rouge", "Miami" , "LA 2.0", "Toronto", "Calgary", "Memphis", "Phoenix", "Seattle", "SF", "Des Moines", "Lincoln"]
    deletes = [78, 8, 8, 10, 200, 32, 7, 500, 6, 121, 131, 150, 3, 1]
    test_keys = [1, 3, 78, 10, 200, 32, 2, 5, 8, 73, 40, 31, 33, -100, 45]
    test_answers1 = ["Omaha", "Dayton", "Boston", "NYC", "LA 2.0", "Chicago", "Baton Rouge", "Miami", "Toronto", "Calgary", None, None, None, None, None]
    test_answers2 = [None, None, None, None, None, None, "Baton Rouge", "Miami", None, "Calgary", None, None, None, None, None]

    print "HT initial: n=", ht.n, "m=", ht.m, "len(v)=", len(ht.v)
    for i in range(min(len(keys),len(values))):
        ht[keys[i]] = values[i]
    print "HT after inserts: n=", ht.n, "m=", ht.m, "len(v)=", len(ht.v)

    keys1 = ht.keys()
    values1 = ht.values()
    print "Sum of keys =",sum(keys1)
    print "Keys =", keys1
    print "Values =", values1
    print "HT.v =", ht

    error = False
    for i in range(min(len(test_keys),len(test_answers1))):
        if ht.lookup(test_keys[i]) != test_answers1[i]:
            print "Failed lookup: i =", i, "key =", test_keys[i], "expected =", test_answers1[i], "actual =", ht.lookup(test_keys[i])
            error = True
    if not error:
        print "*** All lookups successful after inserts only ***"

    for d in deletes:
        del ht[d]
    print "HT after deletes: n=", ht.n, "m=", ht.m, "len(v)=", len(ht.v)

    keys1 = ht.keys()
    values1 = ht.values()
    print "Sum of keys =",sum(keys1)
    print "Keys =", keys1
    print "Values =", values1
    print "HT.v =", ht

    error = False
    for i in range(min(len(test_keys),len(test_answers2))):
        if ht.lookup(test_keys[i]) != test_answers2[i]:
            print "Failed lookup: i =", i, "key =", test_keys[i], "expected =", test_answers2[i], "actual =", ht.lookup(test_keys[i])
            error = True
    if not error:
        print "*** All lookups successful after inserts and deletes ***"

def hashTableRandomTest(size):
    """
    Creates a HashTable and dictionary with random elements of a given size.
    Compares all elements of the HT and dic after insertions, deletions and failed / random deletions.
    Returns True if the two all the same at all times, and False otherwise.
    Used for testing this implementation of HashTable with the built-in versoin.
    """
    ht = HashTable()
    dic = {}
    time_ht = datetime.timedelta(0)
    time_dic = datetime.timedelta(0)

    for i in range(size):
        k, v = random.randint(1,100000), random.randint(-99999,99999)
        d = datetime.datetime.now()
        dic[k] = v
        time_dic += (datetime.datetime.now() - d)
        d = datetime.datetime.now()
        ht[k] = v
        time_ht += (datetime.datetime.now() - d)

    correct = True
    if not hashTableCompare(ht, dic):
        print "Hash table comparison failed, after insertions. ht =", ht, " dic =", dic
        correct = False
    
    keys = dic.keys()

    for i in range(size//4):
        index = random.randint(0,len(keys)-1)
        k = keys[index]
        d = datetime.datetime.now()
        if k in ht:
            del dic[k]
        time_dic += (datetime.datetime.now() - d)
        d = datetime.datetime.now()
        del ht[k]
        time_ht += (datetime.datetime.now() - d)

    if not hashTableCompare(ht, dic):
        print "Hash table comparison failed, after deletions. ht =", ht, " dic =", dic
        correct = False

    for i in range(size//4):
        k = random.randint(-999,999)
        d = datetime.datetime.now()
        if k in ht:
            del dic[k]
        time_dic += (datetime.datetime.now() - d)
        d = datetime.datetime.now()
        del ht[k]
        time_ht += (datetime.datetime.now() - d)

    if not hashTableCompare(ht, dic):
        print "Hash table comparison failed, after random deletions. ht =", ht, " dic =", dic
        correct = False 

    print "Time comparison: HashTable",time_ht, "dictionary", time_dic
    
    return correct

def hashTableCompare(ht, dic):
    """
    Compares all contents of HashTable ht with dictionary dic.
    Returns False if any values are different or missing in either object.
    """
    keys1 = ht.keys()
    keys2 = dic.keys()
    vals1 = ht.values()
    vals2 = dic.values()

    for k in keys1:
        if ht[k] != dic[k]:
            return False

    for k in keys2:
        if ht[k] != dic[k]:
            return False

    #if len(vals2) == 0:
    #    minimum = None
    #    maximum = None
    #else:
    #    minimum = min(vals2)
    #    maximum = max(vals2)
    #
    #print "min", ht.minimum(), minimum
    #print "max", ht.maximum(), maximum

    return True

def hashTableFullTest():
    print "\nHash function testing:"
    hashFunctionTest()

    print "\nHash table testing:"
    hashTableTest()

    print "\Random hash table testing:"
    for i in range(1,21):
        if hashTableRandomTest(2000):
            print "Test #",i,"successful"

def BSTFromArray(arr):
    """
    Creates a BST from the keys in a given array.
    type arr: List[]
    rtype: BST
    """
    tree = BST()
    for k in arr:
        tree.insert(Node(k))
    return tree

def BSTRandomTest(tree, size):
    """
    Fills a BST of a given size, with random elements.
    Tests the contents of the BST with an array, after insertions and deletions.
    Returns Tree if the contents of the BST are identical to the array at all times.
    For BST class and subclass testing.
    """
    passed = True
    ar = []

    # insertions
    for i in range(size):
        v = random.randint(-999,999)
        if v not in ar:
            ar.append(v)
            tree.insert(Node(v))
            
    ar.sort()
    if not BSTCompare(tree, ar):
        BSTPrintErrorMessage(tree, ar, ", after insertions")
        passed = False

    # known deletions
    for i in range(len(ar)//2):
        v = ar[i]
        ar.remove(v)
        n = tree.search(v)
        tree.delete(n)
    
    if not BSTCompare(tree, ar):
        BSTPrintErrorMessage(tree, ar, ", after known deletions")
        passed = False

    # random deletions
    for i in range(size//2):
        v = random.randint(-1000,1000)
        if v in ar:
            ar.remove(v)
        n = tree.search(v)
        tree.delete(n)

    if not BSTCompare(tree, ar):
        BSTPrintErrorMessage(tree, ar, ", after random deletions")
        passed = False

    # additional insertions
    for i in range(size//4):
        v = random.randint(-1000,1000)
        if v not in ar:
            ar.append(v)
            tree.insert(Node(v))
    ar.sort()
    if not BSTCompare(tree, ar):
        BSTPrintErrorMessage(tree, ar, ", after second insertions")
        passed = False

    return passed  
    
def BSTCompare(tree, ar):
    """ Compares the output of an InOrder Walk on a BST with a sorted array.
    Returns True if all elements are the same, and False otherwise.
    For BST class testing.
    """
    ar1 = tree.inorderWalk()
    if len(ar) != len(ar1): return False
    for i in range(len(ar)):
        if ar[i] != ar1[i]: return False
    return True

def BSTPrintErrorMessage(tree, arr, str = ""):
    """
    Prints an error message from a BST test, along with the BST and the comparison array.
    For BST class testing.
    """
    print "Failed comparison tests" + str
    print "Tree:"
    print tree
    print "In order walk:"
    print tree.inorderWalk()
    print "Array:"
    print arr
    
def BSTFullTest():
    """
    Various tests for the BST class, including insertion, deletion, inorder walks, etc.
    For BST class testing.
    """
    print "\nTesting BST: random tests"
    for i in range(20):
        tree = BST()
        passed = BSTRandomTest(tree, 1000)
        if passed:
            print "Passed random test", i+1

    print "\nTesting BST: various operations"
    tree = BST()
    for i in range(20):
        v = random.randint(-99, 99)
        tree.insert(Node(v))

    print "Height =", tree.height()
    print "Minimum =", tree.minimum()
    print "Maximum =", tree.maximum()
    print "In-order Walk =", tree.inorderWalk()
    print "Random tree ="
    print tree

    arr = [21, 45, 1, 34, 8, -1, 99, -54, 60, 2]
    tree = BSTFromArray(arr)
    print("Test tree:")
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
    
def main():
    heapFullTest()
    sortedArrayFullTest()
    hashTableFullTest()
    BSTFullTest()

if __name__ == "__main__":
    main()
