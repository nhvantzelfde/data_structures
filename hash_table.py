import random

class HashFunction(object):
    def __init__(self, m):
        self.d = 2**31-1
        self.m = m
        self.p = self.__findPrime(self.d)
        self.a = random.randint(1,self.p-1)
        self.b = random.randint(0,self.p-1)

    def __findPrime(self, m):
        t = max(3, m + 1)
        if t % 2 == 0: t += 1
        while not self.__isPrime(t):
            t += 2
        return t

    def __isPrime(self, m):
        if m == 1: return False
        for i in range(2,int(m**0.5)+1):
            if m % i == 0: return False
        return True
        
    def h(self, k):
        return ((self.a* k + self.b) % self.p) % self.m

    def __str__(self):
        return "Hash function: m = " + str(self.m) + ", p = " + str(self.p) + ", a = " + str(self.a) + ", b = " + str(self.b)

class LinkedList(object):
    def __init__(self, v = None):
        self.prev = None
        self.next = None
        self.value = v

    def search(self, target):
        if self.value == target: return self
        elif self.next:
            return self.next.search()
        else:
            return None

    def length(self):
        if not self.next: return 1
        else: return 1 + self.next.length()

    def asArray(self, ar):
        ar.append(self.value)
        if self.next: self.next.asArray(ar)

    def __str__(self):
        if self.next: return str(self.value) + "," + str(self.next)
        else: return str(self.value)
    
class KeyValuePair(object):
    def __init__(self, k, v):
        self.key = k
        self.value = v

    def __eq__(self, other):
        if type(other) == KeyValuePair:
            return self.key == other.key
        else:
            return self.key == other

    def __le__(self, other):
        if type(other) == KeyValuePair:
            return self.key <= other.key
        else:
            return self.key <= other

    def __lt__(self, other):
        if type(other) == KeyValuePair:
            return self.key < other.key
        else:
            return self.key < other  

    def __ge__(self, other):
        if type(other) == KeyValuePair:
            return self.key >= other.key
        else:
            return self.key >= other  

    def __gt__(self, other):
        if type(other) == KeyValuePair:
            return self.key > other.key
        else:
            return self.key > other    
    
    def __str__(self):
        return "[" +str(self.key)+","+str(self.value)+"]"
    
class HashTable(object):
    def __init__(self):
        self.n = 0
        self.m = 8
        self.h = HashFunction(self.m)
        self.max_load = 1.00
        self.min_load = 0.25
        
        self.v = [None] * self.m

    def insert(self, k, v):
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
        return (1. * self.n) / self.m 

    def __grow(self):
        self.__rebuild(self.m*2)   
    
    def __shrink(self):
        self.__rebuild(self.m/2) 

    def __rebuild(self,new_m):
        kvps = self.__kvps()

        self.n = 0
        self.m = new_m
        self.h = HashFunction(self.m)
        self.v = [None] * self.m

        for kvp in kvps:
            self.insert(kvp.key,kvp.value)  

    def lookup(self, k):
        h = self.h.h(k)
        l = self.v[h]

        if not l: return None
        
        while l:
            if l.value.key == k:
                return l.value.value
            l = l.next
        return None

    def contains(self, k):
        h = self.h.h(k)
        l = self.v[h]

        if not l: return False
        
        while l:
            if l.value.key == k:
                return True    
            l = l.next
        return False

    def values(self):
        kvps = self.__kvps()

        vals = []
        for i in range(len(kvps)):
            vals.append(kvps[i].value)
        return vals

    def keys(self):
        kvps = self.__kvps()

        keys = []
        for i in range(len(kvps)):
            keys.append(kvps[i].key)
        return keys

    def __kvps(self):
        kvps = []
        for i in range(len(self.v)):
            if self.v[i]:
                self.v[i].asArray(kvps)
        return kvps

    def __str__(self):
        s = "Hash table: "
        for i,l in enumerate(self.v):
            s += "{"+str(l)+"}"
            if i != len(self.v)-1:
                s += ","
        return s

def testHash():
    m = 128
    h = HashFunction(m)
    print(h)

    count = [0] * m
    for i in range(m*2):
        count[h.h(random.randint(-10000,10000))] += 1
    print count

def testTable():
    ht = HashTable()
    
    keys = [1, 3, 78, 10, 200, 32, 2, 5, 200, 8, 73, 7, 500, 6, 121, 131, 150]
    values = ["Omaha", "Dayton", "Boston", "NYC", "LA", "Chicago", "Baton Rouge", "Miami" , "LA 2.0", "Toronto", "Calgary", "Memphis", "Phoenix", "Seattle", "SF", "Des Moines", "Lincoln"]
    deletes = [78, 8, 8, 10, 200, 32, 7, 500, 6, 121, 131, 150, 3, 1]
    test_keys = [1, 3, 78, 10, 200, 32, 2, 5, 8, 73, 40, 31, 33, -100, 45]
    test_answers1 = ["Omaha", "Dayton", "Boston", "NYC", "LA 2.0", "Chicago", "Baton Rouge", "Miami", "Toronto", "Calgary", None, None, None, None, None]
    test_answers2 = [None, None, None, None, None, None, "Baton Rouge", "Miami", None, "Calgary", None, None, None, None, None]

    print "HT initial: n=", ht.n, "m=", ht.m, "len(v)=", len(ht.v)
    for i in range(min(len(keys),len(values))):
        ht.insert(keys[i],values[i])
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
        ht.delete(d)
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
    
def main():
    print "Hash function testing:"
    testHash()
    print ""

    print "Hash table testing:"
    testTable()
    print ""

if __name__ == "__main__":
    main()
    
