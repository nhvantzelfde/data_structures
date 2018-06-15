import random
import datetime

class HashFunction(object):
    """ Simple hash function, for use with hash tables.

    Calculates a hash in the form ((ak + b) mod p) mod m.
    Create with a desired m = hash table size, and call h(k) to hash a given key k.
    Meant to be immutable once created. A new instance should be created for new m.
    
    Attributes:
        d = size of the universe of keys
        m = size of the hash table
        p = prime between _d and 2*_d
        a = random number between [1,p-1]
        b = random number between [0,p-1]
    """

    def __init__(self, m):
        """ Initializes the instance with parameter m, the size of the hash table. """
        self.d = 2**31-1
        self.m = m
        self.p = self.__findPrime(self.d)
        self.a = random.randint(1,self.p-1)
        self.b = random.randint(0,self.p-1)

    def __findPrime(self, n):
        """ Finds a prime, using brute force, greater than n. """
        t = max(3, n+1)
        if t % 2 == 0: t += 1
        while not self.__isPrime(t):
            t += 2
        return t

    def __isPrime(self, n):
        """ Determines whether a given integer n is prime or not. """
        if n == 1: return False
        for i in range(2,int(n**0.5)+1):
            if n % i == 0: return False
        return True
        
    def h(self, k):
        """ Returns the hash value for a given input key k. """
        return ((self.a * k + self.b) % self.p) % self.m

    def __str__(self):
        """ Returns a string representation of the hash function. """
        return "Hash function: m = " + str(self.m) + ", p = " + str(self.p) + ", a = " + str(self.a) + ", b = " + str(self.b)

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
        n = number of distinct elements stored in the table
        m = current size of the array
        h = hash function
        max_load = maximum load before the table grows
        min_load = minimum load before the table shrinks; should be smaller than max_load to function properly
        v = the array storing linked lists at each hash value
    """

    def __init__(self):
        """ Initializes an empty hash table. """
        self.n = 0
        self.m = 8
        self.h = HashFunction(self.m)
        self.max_load = 1.00
        self.min_load = 0.25
        
        self.v = [None] * self.m

    def insert(self, k, v):
        """ Inserts a value into the hash table, keyed with the given key. If the key already exists in the hash table, the value is overwritten. """
        h = self.h.h(k)
        l = self.v[h]

        if not l:
            self.v[h] = LinkedList(KeyValuePair(k,v))
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
            
        self.n += 1
        
        if self.load() > self.max_load:
            self.__grow()

    def delete(self, k):
        """ Deletes an entry in the hash table at a given key. If no such element exists, this does nothing. """
        h = self.h.h(k)
        l = self.v[h]

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
                        self.v[h] = l.next
                        if l.next:
                            l.next.prev = None
                    self.n -= 1
                    break
                p, l = l, l.next
            
            if self.load() < self.min_load:
                self.__shrink()

    def load(self):
        """ Returns the current load of the hash table. """
        return (1. * self.n) / self.m 

    def __grow(self):
        """ Doubles the current size of the array storing the hash table. """
        self.__rebuild(self.m*2)   
    
    def __shrink(self):
        """ Halves the current size of the array storing the hash table. """
        self.__rebuild(self.m/2) 

    def __rebuild(self,new_m):
        """ Rebuilds the array storing the hash table, at a given size new_m. """
        kvps = self.__kvps()

        self.n = 0
        self.m = new_m
        self.h = HashFunction(self.m)
        self.v = [None] * self.m

        for kvp in kvps:
            self.insert(kvp.key,kvp.value)  

    def lookup(self, k):
        """ Returns the value associated with key k, or None if no such value exists. """
        h = self.h.h(k)
        l = self.v[h]

        if not l: return None
        
        while l:
            if l.value.key == k:
                return l.value.value
            l = l.next
        return None

    def contains(self, k):
        """ Returns True if the key k is in the hash table, and False otherwise. """
        h = self.h.h(k)
        l = self.v[h]

        if not l: return False
        
        while l:
            if l.value.key == k:
                return True    
            l = l.next
        return False

    def values(self):
        """ Returns an array representing all the values currently stored in the hash table. """
        kvps = self.__kvps()

        vals = []
        for i in range(len(kvps)):
            vals.append(kvps[i].value)
        return vals

    def keys(self):
        """ Returns an array representing all the keys currently stored in the hash table. """
        kvps = self.__kvps()

        keys = []
        for i in range(len(kvps)):
            keys.append(kvps[i].key)
        return keys

    def __kvps(self):
        """ Returns an array with all the KeyValuePairs currently stored in the hash table. """
        kvps = []
        for i in range(len(self.v)):
            if self.v[i]:
                self.v[i].asArray(kvps)
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
        kvps = self.__kvps()

        s = "{"
        for i, kvp in enumerate(kvps):
            s += str(kvp.key) + ": " + str(kvp.value)
            if i != len(kvps)-1:
                s += ", "
        s += "}"
        return s

def testHash():
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

def testTable():
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

def randomTest(size):
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
    if not compareHashTables(ht, dic):
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

    if not compareHashTables(ht, dic):
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

    if not compareHashTables(ht, dic):
        print "Hash table comparison failed, after random deletions. ht =", ht, " dic =", dic
        correct = False 

    print "Time comparison: HashTable",time_ht, "dictionary", time_dic
    
    return correct

def compareHashTables(ht, dic):
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

def main():
    print "Hash function testing:"
    testHash()
    print ""

    print "Hash table testing:"
    testTable()
    print ""

    print "Random hash table testing:"
    for i in range(1,21):
        if randomTest(25000):
            print "Test #",i,"successful"
    print ""

if __name__ == "__main__":
    main()
    
