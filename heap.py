
class Heap(object):
    """ Heap data structure, implemented as an array.

    Can be used to create both MinHeaps (a.k.a. Priority Queues) and MaxHeaps.
    Heap invariant: MinHeap: key at an index is less than or equal to keys of its children
                    MaxHeap: key at an index is greater than or equal to keys of its children
    Keys should not be manipulated directly, but rather by calling createHeap, insert, and extract.

    Attributes:
        _min_heap = True if the heap is a MinHeap, False if it is a MaxHeap
        _keys = list of keys in the heap

    """
    
    def __init__(self, min_heap):
        """ Initializes a heap. Use min_heap = True for a MinHeap / Priority Queue, and min_heap = False for a MaxHeap. """
        self._min_heap = min_heap
        self._keys = []

    def createHeap(self, keys):
        """ Creates a heap from the given list of keys. Overwrites any existing keys in the heap. """
        self._keys = list(keys)
        for i in range(len(self._keys)//2-1,-1,-1):
            self._heapify(i)
        self.__checkRep()

    def modifyKey(self, i, key):
        """ Decreases (for a MinHeap) or increases (for a MaxHeap) the key at a given index. """
        if i >= self.size():
            return
        elif self.isMinHeap() and key > self._keys[i]:
            return
        elif self.isMaxHeap() and key < self._keys[i]:
            return
        
        self._keys[i] = key
        p = self._parent(i)
        while i > 0 and self._compareKeys(self._keys[i],self._keys[self._parent(i)]):
            self._keys[i], self._keys[self._parent(i)] = self._keys[self._parent(i)], self._keys[i]
            i = self._parent(i)
            
        self.__checkRep()

    def minimum(self):
        """ Returns the minimum key in the heap. Takes O(1) for a MinHeap and O(n) time for MaxHeap. """
        if self.size() == 0:
            return None
        elif self.isMinHeap():
            return self._keys[0]
        else:
            return min(self._keys)

    def maximum(self):
        """ Returns the maximum key in the heap. Takes O(1) for a MaxHeap and O(n) time for MinHeap. """
        if self.size() == 0:
            return None
        elif self.isMaxHeap():
            return self._keys[0]
        else:
            return max(self._keys)
        
    def extract(self):
        """ Extracts the minimum (for MinHeap) or maximum (for MaxHeap) key in the heap. """
        return self._extractIndex(0)

    def extractAll(self):
        """ Extracts all elements in order. Heap becomes empty. """
        ar = []
        while self.size() > 0:
            ar.append(self.extract())
        return ar
        
    def insert(self, key):
        """ Inserts a key into the heap. """
        if self.isMinHeap():
            default = float("inf")
        else:
            default = -float("inf")
            
        self._keys.append(default)
        self.modifyKey(self._last(),key)
        
    def delete(self, key):
        """ Deletes the first instance of a key from the heap. Does nothing if the key does not exist. """
        for i in range(len(self._keys)):
            if self._keys[i] == key:
                self._extractIndex(i)
                break
    
    def isMinHeap(self):
        """ Returns True if the heap is a MinHeap, and False otherwise. """
        return self._min_heap
    
    def isMaxHeap(self):
        """ Returns True if the heap is a MaxHeap, and False otherwise. """
        return not self.isMinHeap()
        
    def size(self):
        """ Returns the size / length of the heap. """
        return len(self)

    def _heapify(self, i):
        """ Fixes the heap invariant at a given index. """
        l = self._left(i)
        r = self._right(i)
        current = i
        if l < self.size() and self._compareKeys(self._keys[l],self._keys[current]):
            current = l
        if r < self.size() and self._compareKeys(self._keys[r],self._keys[current]):
            current = r
        if current != i:
            self._keys[i], self._keys[current] = self._keys[current], self._keys[i]
            self._heapify(current)

    def _compareKeys(self, k1, k2):
        """ Returns either k1 < k2 (for MinHeap) or k1 > k2 (for MaxHeap). Used in heapify and modifyKey. """
        if self.isMinHeap():
            return k1 < k2
        else:
            return k1 > k2

    def _extractIndex(self, i):
        """ Removes and returns the key at a given index. """
        if i >= self.size(): return None
        else:
            self._keys[i], self._keys[self._last()] = self._keys[self._last()], self._keys[i]
            result = self._keys.pop()

            p = self._parent(i)
            l = self._left(i)
            r = self._right(i)
            
            if i == 0 or (l < self.size() and self._compareKeys(self._keys[l],self._keys[i])) or (r < self.size() and self._compareKeys(self._keys[r],self._keys[i])):
                self._heapify(i)
            elif i < self.size():
                self.modifyKey(i,self._keys[i])
            
            self.__checkRep()
            return result
        
    def _parent(self, i):
        """ Returns the index of the parent of a given index. """
        return (i + 1) // 2 - 1

    def _left(self, i):
        """ Returns the index of the left child of a given index. """
        return 2 * (i + 1) - 1

    def _right(self, i):
        """ Returns the index of the right child of a given index. """
        return 2 * (i + 1)

    def _last(self):
        """ Returns the index of the last key in the heap. """
        return len(self._keys)-1
        
    def __len__(self):
        """ Returns the length / size of the heap. """
        return len(self._keys)
    
    def __str__(self):
        """ Returns a string representation of the heap. """
        if self.isMinHeap(): s = "Min"
        else: s = "Max"
        s += "Heap, keys = " + str(self._keys)
        return s

    def __checkRep(self):
        """ Checks the rep invariant for the structure. Prints a message if the invariant is not met. For debugging. """
        if False: # set to True for debugging
            for i in range(self.size()):
                l = self._left(i)
                r = self._right(i)
                if l < self.size() and self._compareKeys(self._keys[l], self._keys[i]):
                    print "Rep Invariant Error, index =", i, ", len =", self.size(), ", key =", self._keys[i], ", left =", self._keys[l]
                if r < self.size() and self._compareKeys(self._keys[r], self._keys[i]):
                    print "Rep Invariant Error, index =", i, ", len =", self.size(), ", key =", self._keys[i], ", right =", self._keys[r]

class MinHeap(Heap):
    """ MinHeap, with all functionality derived from Heap class.

    This is purely a convenience class, with additional methods based on the name.
    The same functionality can be had by creating an instance of Heap using Heap(True).

    Attributes:
        none, apart from parent class
    """
    
    def __init__(self):
        """ Initializes a new MinHeap. """
        super(MinHeap, self).__init__(True)
        
    def createMinHeap(self, keys):
        """ Creates a MinHeap from an array of keys. Erases any existing keys. """
        super(MinHeap, self).createHeap(keys)

    def decreaseKey(self, i, key):
        """ Decreases a key at a given index i. Does nothing if the new key is larger than existing. """
        super(MinHeap, self).modifyKey(i, key)

    def extractMin(self):
        """ Extracts the minimum key in the heap. Returns None if the heap is empty. """
        return super(MinHeap, self).extract()

class MaxHeap(Heap):
    """ MaxHeap, with all functionality derived from Heap class.

    This is purely a convenience class, with additional methods based on the name.
    The same functionality can be had by creating an instance of Heap using Heap(False).

    Attributes:
        none, apart from parent class
    """
    
    def __init__(self):
        """ Initializes a new MaxHeap. """
        super(MaxHeap, self).__init__(False)
        
    def createMaxHeap(self, keys):
        """ Creates a MaxHeap from an array of keys. Erases any existing keys. """
        super(MaxHeap, self).createHeap(keys)

    def increaseKey(self, i, key):
        """ Increases a key at a given index i. Does nothing if the new key is smaller than existing. """
        super(MaxHeap, self).modifyKey(i, key)

    def extractMax(self):
        """ Extracts the maximum key in the heap. Returns None if the heap is empty. """
        return super(MaxHeap, self).extract()
