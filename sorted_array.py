import random

def binarySearch(s_arr, target):
    """ Returns the index of target in the given sorted array, or the index of where target should be inserted if it does not exist.
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
    def __init__(self, values = None):
        if values:
            self.v = sorted(values)
        else:
            self.v = []
    
        self.__checkRep()
        
    def insert(self, value):
        i = binarySearch(self.v, value)

        self.v.append(None)
        for j in range(len(self.v)-2,i-1,-1):
            self.v[j+1] = self.v[j]
        self.v[i] = value
        
        self.__checkRep()
    
    def delete(self, value):
        i = binarySearch(self.v, value)

        if i < len(self.v) and self.v[i] == value:
            for j in range(i,len(self.v)-1):
                self.v[j] = self.v[j+1]
            self.v.pop()
        
        self.__checkRep()
    
    def index(self, value):
        i = binarySearch(self.v, value)

        if i < len(self.v) and self.v[i] == value:
            return i
        else: return None   
    
    def get(self, i):
        return self.v[i]

    def total(self):
        return sum(self.v)
    
    def __str__(self):
        return str(self.v)
        
    def __checkRep(self):
        if False:
            for i, n in enumerate(self.v):
                if i == 0: continue
                if n < self.v[i-1]: 
                    print "Invariant breach: element",n,"at index",i,"out of order"
    
def randomTest(size):
    s_arr = SortedArray()
    ar = []
    for i in range(size):
        n = random.randint(-10000,10000)
        ar.append(n)
        s_arr.insert(n)
    ar.sort()
    if not compare(s_arr,ar): return False

    for i in range(size//2):
        index = random.randint(0,len(ar)-1)
        n = ar[i]
        s_arr.delete(n)
        ar.remove(n)
    if not compare(s_arr,ar): return False

    return True

def compare(s_arr, ar):
    for i in range(len(ar)):
        if ar[i] != s_arr.get(i): return False
    return True    
    
def main():
    init = [1, 5, 2, 80, 42, 232, 10, -1]
    adds = [2, 20, 423, 65, 4, 98, -1, 5, 10]
    dels = [42, 232, -1, 5, 2000, -10]
    test = [1, 2, 80, 10, 2, 20, 423, 65, 4, 98, -1, 5, 10]
    test.sort()

    print "Target sums: init=", sum(init),"after adds=", sum(init)+sum(adds), "test=", sum(test)
    
    s_arr = SortedArray(init)
    print "After initial: s_arr =", s_arr, "sum = ", s_arr.total()
    for a in adds:
        s_arr.insert(a)
    print "After adds: s_arr =", s_arr, "sum = ", s_arr.total()

    for d in dels:
        s_arr.delete(d)
    print "After deletes: s_arr =", s_arr, "sum = ", s_arr.total()
    
    error = False
    for i in range(len(test)):
        if test[i] != s_arr.get(i):
            print "Error at index",i," test =", test[i]," s_arr =",s_arr.get(i)

    for i in range(20):
        if randomTest(1000): print "Test",i+1,"successful"
        else: print "Failure at test",i+1
    
if __name__ == "__main__":
    main()
