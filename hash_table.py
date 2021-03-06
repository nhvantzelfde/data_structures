import random

class HashFunction(object):
    """ Simple hash function, for use with hash tables.

    Calculates a hash in the form ((ak + b) mod p) mod m.
    Create with a desired m = hash table size, and call h(k) to hash a given key k.
    Meant to be immutable once created. A new instance should be created for new m.
    
    Attributes:
        (class) d = size of the universe of keys
        _m = size of the hash table
        _p = prime between d and 2*d
        _a = random number between [1,_p - 1]
        _b = random number between [0,_p - 1]
    """

    d = 2**31-1

    def __init__(self, m):
        """ Initializes the instance with parameter m, the size of the hash table. """
        self._m = m
        self._p = HashFunction._findPrime(HashFunction.d)
        self._a = random.randint(1,self._p-1)
        self._b = random.randint(0,self._p-1)
        
    def h(self, k):
        """ Returns the hash value for a given input key k. """
        return ((self._a * k + self._b) % self._p) % self._m

    @classmethod
    def _findPrime(cls, n):
        """ Finds a prime, using brute force, greater than n. """
        t = max(3, n+1)
        if t % 2 == 0: t += 1
        while not cls._isPrime(t):
            t += 2
        return t

    @classmethod
    def _isPrime(cls, n):
        """ Determines whether a given integer n is prime or not. """
        if n == 1: return False
        for i in range(2,int(n**0.5)+1):
            if n % i == 0: return False
        return True

    def __str__(self):
        """ Returns a string representation of the hash function. """
        return "Hash function: m = " + str(self._m) + ", p = " + str(self._p) + ", a = " + str(self._a) + ", b = " + str(self._b)

class LinkedList(object):
    """ Simple doubly-linked list.

    Attributes:
        prev = previous element in the list
        next = next element in the list
        value = value for this element in the list
    """

    def __init__(self, v = None):
        """ Initializes a linked list with an optional given value. """
        self.prev = None
        self.next = None
        self.value = v

    def search(self, target):
        """ Searches the linked list started at this element for a given target value. """
        if self.value == target: return self
        elif self.next:
            return self.next.search()
        else:
            return None

    def asArray(self, ar):
        """ Appends the linked list starting at this element to the passed array. """
        ar.append(self.value)
        if self.next: self.next.asArray(ar)

    def __len__(self):
        """ Returns the length of the list starting at this element. """
        if not self.next: return 1
        else: return 1 + len(self.next)

    def __str__(self):
        """ Returns a string representation of the linked list starting at this element. """
        if self.next: return str(self.value) + "," + str(self.next)
        else: return str(self.value)
    
class KeyValuePair(object):
    """ A pair of (key, value) for use in hash tables and other data structures.

    Implements a full suite of comparisons based on key value, so it can be treated as a single value for heaps and other structures.
    The key should not be changed after being added to a hash table or the table will not be able to find the KVP.

    Attributes:
        key = key for this pair, used for comparisons with other KVPs or ints/floats and for determining the hash table slot
        value = the value associated with the given key
    """
    
    def __init__(self, k, v):
        """ Initializes a KVP with a given key and value. """
        self.key = k
        self.value = v

    def __eq__(self, other):
        """ Implements '==' comparison function, for use with other KVPs or other ints/floats. """
        if type(other) == KeyValuePair:
            return self.key == other.key
        else:
            return self.key == other

    def __le__(self, other):
        """ Implements '<=' comparison function. """
        if type(other) == KeyValuePair:
            return self.key <= other.key
        else:
            return self.key <= other

    def __lt__(self, other):
        """ Implements '<' comparison function. """
        if type(other) == KeyValuePair:
            return self.key < other.key
        else:
            return self.key < other  

    def __ge__(self, other):
        """ Implements '>=' comparison function. """
        if type(other) == KeyValuePair:
            return self.key >= other.key
        else:
            return self.key >= other  

    def __gt__(self, other):
        """ Implements '>' comparison function. """
        if type(other) == KeyValuePair:
            return self.key > other.key
        else:
            return self.key > other    
    
    def __str__(self):
        """ Returns a string representation of the KVP. """
        return "[" +str(self.key)+","+str(self.value)+"]"
    
class HashTable(object):
    """ Implementation of a hash table / dictionary, comparable to the built-in dict. Uses chaining.

    Supports lookup and insert in O(1) amortized. Uses table doubling / halving to grow and shrink the table, as requried.
    Direct modification of the values or counts is not supported. Use insert() and delete() instead.

    Attributes:
        (class) max_load = maximum load before the table grows
        (class) min_load = minimum load before the table shrinks; should be smaller than max_load to function properly
        _n = number of distinct elements stored in the table
        _m = current size of the array
        _h = hash function
        _v = the array storing linked lists at each hash value
    """

    max_load = 1.00
    min_load = 0.25

    def __init__(self):
        """ Initializes an empty hash table. """
        self._n = 0
        self._m = 8
        self._h = HashFunction(self._m)
        self._v = [None] * self._m

    def insert(self, k, v):
        """ Inserts a value into the hash table, keyed with the given key. If the key already exists in the hash table, the value is overwritten. """
        h = self._h.h(k)
        l = self._v[h]

        if not l:
            self._v[h] = LinkedList(KeyValuePair(k,v))
        else:
            p = l.prev
            while l:
                if l.value.key == k:
                    l.value.value = v
                    return
                p, l = l, l.next

            new = LinkedList(KeyValuePair(k,v))
            p.next = new
            new.prev = p
            
        self._n += 1
        
        if self.load() > self.max_load:
            self._grow()

    def delete(self, k):
        """ Deletes an entry in the hash table at a given key. If no such element exists, this does nothing. """
        h = self._h.h(k)
        l = self._v[h]

        if not l:
            return
        else:
            p = l.prev
            while l:
                if l.value.key == k:
                    if p:
                        p.next = l.next
                        if l.next:
                            l.next.prev = p
                    else:
                        self._v[h] = l.next
                        if l.next:
                            l.next.prev = None
                    self._n -= 1
                    break
                p, l = l, l.next
            
            if self.load() < self.min_load:
                self._shrink()

    def load(self):
        """ Returns the current load of the hash table. """
        return (1. * self._n) / self._m 

    def _grow(self):
        """ Doubles the current size of the array storing the hash table. """
        self._rebuild(self._m*2)   
    
    def _shrink(self):
        """ Halves the current size of the array storing the hash table. """
        self._rebuild(self._m/2) 

    def _rebuild(self,new_m):
        """ Rebuilds the array storing the hash table, at a given size new_m. """
        kvps = self._kvps()

        self._n = 0
        self._m = new_m
        self._h = HashFunction(self._m)
        self._v = [None] * self._m

        for kvp in kvps:
            self.insert(kvp.key,kvp.value)  

    def lookup(self, k):
        """ Returns the value associated with key k, or None if no such value exists. """
        h = self._h.h(k)
        l = self._v[h]

        if not l: return None
        
        while l:
            if l.value.key == k:
                return l.value.value
            l = l.next
        return None

    def contains(self, k):
        """ Returns True if the key k is in the hash table, and False otherwise. """
        h = self._h.h(k)
        l = self._v[h]

        if not l: return False
        
        while l:
            if l.value.key == k:
                return True    
            l = l.next
        return False

    def values(self):
        """ Returns an array representing all the values currently stored in the hash table. """
        kvps = self._kvps()

        vals = []
        for i in range(len(kvps)):
            vals.append(kvps[i].value)
        return vals

    def keys(self):
        """ Returns an array representing all the keys currently stored in the hash table. """
        kvps = self._kvps()

        keys = []
        for i in range(len(kvps)):
            keys.append(kvps[i].key)
        return keys

    def _kvps(self):
        """ Returns an array with all the KeyValuePairs currently stored in the hash table. """
        kvps = []
        for i in range(len(self._v)):
            if self._v[i]:
                self._v[i].asArray(kvps)
        return kvps

    def minimum(self):
        """ Returns the minimum value in the table. """
        vals = self.values()
        if len(vals) == 0: return None
        return min(self.values())

    def maximum(self):
        """ Returns the minimum value in the table. """
        vals = self.values()
        if len(vals) == 0: return None
        return max(self.values())
        
    def __getitem__(self, k):
        """ Allows retrieving a value by calling hashtable[k]. """
        return self.lookup(k)

    def __setitem__(self, k, v):
        """ Allows setting a value by calling hashtable[k] = v. """
        return self.insert(k, v)

    def __delitem__(self, k):
        """ Allows deleting a value by calling del hashtable[k]. """
        return self.delete(k)

    def __contains__(self, k):
        """ Allows calling k in hashtable to determine whether a key is in the table. """
        return self.contains(k)
    
    def __str__(self):
        """ Returns an string representation of the hash table. """
        kvps = self._kvps()

        s = "{"
        for i, kvp in enumerate(kvps):
            s += str(kvp.key) + ": " + str(kvp.value)
            if i != len(kvps)-1:
                s += ", "
        s += "}"
        return s
