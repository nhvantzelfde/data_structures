
def binarySearch(s_ar, target):
    """
    Returns the index of target in the given sorted array, or the index of where target should be inserted if it does not exist.
    type s_ar: List[], must be pre-sorted and items must be comparable
    type target: any object comparable to the items in s_arr
    rtype: int
    """
    if len(s_ar) == 0: return 0

    low = 0
    high = len(s_ar)-1
    mid = (low + high) // 2
    while True:
        if high - low <= 1:
            if target <= s_ar[low]:
                return low
            elif target <= s_ar[high]:
                return high
            else:
                return high + 1

        if target == s_ar[mid]:
            return mid
        elif target < s_ar[mid]:
            high = mid - 1
        else:
            low = mid + 1

        mid = (low + high) // 2    

class SortedArray(object):
    """ Simple implementation of an always-sorted array.

    Modification of values directly is not supported. Use insert() or delete() instead.

    Attributes:
        _v = array of values contained within the SortedArray
    """
    
    def __init__(self, values = None):
        """ Initializes an instance with optional array of values, sorting them. """
        if values:
            self._v = sorted(values)
        else:
            self._v = []
    
        self.__checkRep()
        
    def insert(self, value):
        """ Inserts a new value into the array. Finds the insertion point in O(lg n) but may still require O(n) shifts. """
        i = binarySearch(self._v, value)

        self._v.append(None)
        for j in range(len(self._v)-2,i-1,-1):
            self._v[j+1] = self._v[j]
        self._v[i] = value
        
        self.__checkRep()
    
    def delete(self, value):
        """ Deletes a value into the array. Does nothing if value does not exist. Finds the element in O(lg n) but may still require O(n) shifts. """
        i = binarySearch(self._v, value)

        if i < len(self._v) and self._v[i] == value:
            for j in range(i,len(self._v)-1):
                self._v[j] = self._v[j+1]
            self._v.pop()
        
        self.__checkRep()
    
    def index(self, value):
        """ Returns the index of a given value in the array, or None if the value is not found. """
        i = binarySearch(self._v, value)

        if i < len(self._v) and self._v[i] == value:
            return i
        else: return None   

    def minimum(self):
        """ Returns the minimum element of the array. """
        if len(self._v) == 0: return None
        else: return self._v[0]

    def maximum(self):
        """ Returns the maximum element of the array. """
        if len(self._v) == 0: return None
        else: return self._v[-1]
        
    def __len__(self):
        """ Returns the length of the array. """
        return len(self._v)
    
    def __getitem__(self, k):
        """ Supports using array[i] to get a value. """
        return self._v[k]

    def __setitem__(self, k, v):
        """ Supports using array[i] = v to overwrite a value; maintains sorted order. """
        self.delete(self._v[k])
        self.insert(v)
        
    def __iter__(self):
        """ Returns an iterator over the values. """
        return iter(self._v)
        
    def __str__(self):
        """ Returns a string representation of the array. """
        return str(self._v)
        
    def __checkRep(self):
        """ Checks the representation invariant for the array, namely that it is always sorted. Used for debugging only. """
        if False: # set to True for debugging
            for i, n in enumerate(self._v):
                if i == 0: continue
                if n < self._v[i-1]: 
                    print "Invariant breach: element",n,"at index",i,"out of order"

