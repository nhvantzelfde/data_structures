import random

def binarySearch(s_arr, target):
    """
    Returns the index of target in the given sorted array, or the index of where target should be inserted if it does not exist.
    type s_arr: List[], must be pre-sorted and items must be comparable
    type target: any comparable item to the items in s_arr
    rtype: int
    """
    if len(s_arr) == 0: return 0

    low = 0
    high = len(s_arr)-1
    mid = (low + high) // 2
    while True:
        if high - low <= 1:
            if target <= s_arr[low]:
                return low
            elif target <= s_arr[high]:
                return high
            else:
                return high + 1

        if target == s_arr[mid]:
            return mid
        elif target < s_arr[mid]:
            high = mid - 1
        else:
            low = mid + 1

        mid = (low + high) // 2    

class SortedArray(object):
    """ Simple implementation of an always-sorted array.

    Modification of values directly is not supported. Use insert() or delete() instead.

    Attributes:
        v = array of values contained within the SortedArray
    """
    def __init__(self, values = None):
        """ Initializes an instance with optional array of values, sorting them. """
        if values:
            self.v = sorted(values)
        else:
            self.v = []
    
        self.__checkRep()
        
    def insert(self, value):
        """ Inserts a new value into the array. Finds the insertion point in O(lg n) but may still require O(n) shifts. """
        i = binarySearch(self.v, value)

        self.v.append(None)
        for j in range(len(self.v)-2,i-1,-1):
            self.v[j+1] = self.v[j]
        self.v[i] = value
        
        self.__checkRep()
    
    def delete(self, value):
        """ Deletes a value into the array. Does nothing if value does not exist. Finds the element in O(lg n) but may still require O(n) shifts. """
        i = binarySearch(self.v, value)

        if i < len(self.v) and self.v[i] == value:
            for j in range(i,len(self.v)-1):
                self.v[j] = self.v[j+1]
            self.v.pop()
        
        self.__checkRep()
    
    def index(self, value):
        """ Returns the index of a given value in the array, or None if the value is not found. """
        i = binarySearch(self.v, value)

        if i < len(self.v) and self.v[i] == value:
            return i
        else: return None   
    
    def __len__(self):
        """ Returns the length of the array. """
        return len(self.v)
    
    def __getitem__(self, k):
        """ Supports using array[i] to get a value. """
        return self.v[k]

    def __setitem__(self, k, v):
        """ Supports using array[i] = v to overwrite a value; maintains sorted order. """
        self.delete(self.v[k])
        self.insert(v)
        
    def __iter__(self):
        """ Returns an iterator over the values. """
        return iter(self.v)
        
    def __str__(self):
        """ Returns a string representation of the array. """
        return str(self.v)
        
    def __checkRep(self):
        """ Checks the representation invariant for the array, namely that it is always sorted. Used for debugging only. """
        if False: # set to True for debugging
            for i, n in enumerate(self.v):
                if i == 0: continue
                if n < self.v[i-1]: 
                    print "Invariant breach: element",n,"at index",i,"out of order"
    
def randomTest(size):
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
    if not compare(s_arr,ar): return False

    # known deletions
    for i in range(size//2):
        index = random.randint(0,len(ar)-1)
        n = ar[i]
        s_arr.delete(n)
        ar.remove(n)
    if not compare(s_arr,ar): return False

    # random deletions
    for i in range(size//4):
        n = random.randint(-10000,10000)
        if n in ar:
            ar.remove(n)
        s_arr.delete(n)
    if not compare(s_arr,ar): return False

    # more insertions
    for i in range(size//4):
        n = random.randint(-10000,10000)
        ar.append(n)
        s_arr.insert(n)
    ar.sort()
    if not compare(s_arr,ar): return False

    # overwrites
    for i in range(size//4):
        index = random.randint(0,len(ar)-1)
        value = random.randint(-10000,10000)
        ar[index] = value
        ar.sort()
        s_arr[index] = value
    if not compare(s_arr,ar): return False

    return True

def compare(s_arr, ar):
    """
    Compares a SortedArray s_arr with a normal, pre-sorted Python List. Returns False if any elements of the two are different.
    """
    if len(s_arr) != len(ar): return False
    for i in range(len(ar)):
        if ar[i] != s_arr[i]: return False
    return True 
    
def main():
    init = [1, 5, 2, 80, 42, 232, 10, -1]
    adds = [2, 20, 423, 65, 4, 98, -1, 5, 10]
    dels = [42, 232, -1, 5, 2000, -10]
    test = [1, 2, 80, 10, 2, 20, 423, 65, 4, 98, 5, 10, 555]
    test.sort()

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
    
    error = False
    for i in range(len(test)):
        if test[i] != s_arr[i]:
            print "Error at index",i," test =", test[i]," s_arr =",s_arr[i]

    for i in range(20):
        if randomTest(1000): print "Test",i+1,"successful"
        else: print "Failure at test",i+1
    
if __name__ == "__main__":
    main()
