from heap import Heap, MinHeap, MaxHeap
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

def main():
    heapFullTest()

if __name__ == "__main__":
    main()
