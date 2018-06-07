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
    def __init__(self, value = None):
        self.prev = None
        self.next = None
        self.val = value

class HashTable(object):

    def __init__(self):
        self.n = 0
        self.m = 8
        self.h = HashFunction(m)
        self.max_load = 0.50
        self.min_load = 0.25
        
        self.v = [None] * m

    def insert(self, k, v):
        h = self.h.h(k)
        l = self.v[h]

        p = l.prev
        while l:
            if l.val[0] == k:
                l.val[1] = v
                return
            p = l
            l = l.next
            
        new = LinkedList([k,v])

        if p:
            p.next = new
            new.prev = p
        else:
            self.v[h] = new

        self.n += 1

        if self.load() > self.max_load:
            self.__grow()

    def load(self):
        return (1. * self.n) / m 

    def __grow(self):
        pass
    
    def __shrink(self):
        pass

    def __rebuild(self):
        pass

    def delete(self, k):
        h = self.h.h(k)
        l = self.v[h]

        p = l.prev
        while l:
            if l.val[0] == k:
                if p:
                    p.next = l.next
                    if l.next:
                        l.next.prev = p
                else:
                    self.v[h] = None
                self.n -= 1
                return
            p = l
            l = l.next
            
        if self.load() < self.min_load:
            self.__shrink()

    def lookup(self, k):
        h = self.h.h(k)
        l = self.v[h]

        p = l.prev
        while l:
            if l.val[0] == k:
                return l.val[1]
            p = l
            l = l.next
        return None

    def contains(self, k):
        h = self.h.h(k)
        l = self.v[h]

        p = l.prev
        while l:
            if l.val[0] == k:
                return True
            p = l
            l = l.next
        return False

    def values(self):
        pass

    def keys(self):
        pass


def main():
    m = 128
    h = HashFunction(m)
    print(h)

    count = [0] * m
    for i in range(m*2):
        count[h.h(random.randint(-10000,10000))] += 1
    print count

if __name__ == "__main__":
    main()
    
        
