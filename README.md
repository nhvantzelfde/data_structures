# data_structures
Elementary data structures

AVL - binary search tree, self-balancing; height is guaranteed < 1.45 * (lg n) - 
    search O(lg n)
    insert O(lg n)
    delete O(lg n)
    min O(lg n)
    max O(lg n)

BST - binary search tree, no self-balancing; h can vary from O(lg n) to O(n) - 
    search O(h)
    insert O(h)
    delete O(h)
    min O(h)
    max O(h) 

HashTable - hash table / dictionary, using table doubling - 
    search O(1)
    insert O(1) amortized
    delete O(1) amortized
    min O(n)
    max O(n) 

Heap - heap / priority queue, including both MinHeaps and MaxHeaps - 
    search O(n)
    insert O(lg n)
    delete O(lg n)
    min O(1) for MinHeap, O(n) for MaxHeap
    max O(n) for MinHeap, O(1) for MaxHeap

SortedArray - always-sorted array - 
    search O(lg n)
    insert O(n)
    delete O(n)
    min O(1)
    max O(1)
