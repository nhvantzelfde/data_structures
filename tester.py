from heap import Heap, MinHeap, MaxHeap
from sorted_array import SortedArray
import random

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
        
def main():
    heapFullTest()
    sortedArrayFullTest()

if __name__ == "__main__":
    main()
