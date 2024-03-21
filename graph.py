'''
    Data.txt
    ----------------
    5 (amount of vertices)
    7 (amount of edges)
    0  1
    1  2
    2  1
    1  3
    2  3
    3  4
    4  0
        
'''

class Queue:
    def __init__(self):
        # Circular Linked List with a back pointer
        #self.mFromPath = []
        #for i in size:
        #    self.mFromPath.append(-1)
        
        self.mQueue = []
            
    def Add(self, A):
        self.mQueue.append(A)
        
    def Pop(self):
        return self.mQueue.pop()
    
    def isEmpty(self):
        if len(self.mQueue) != 0:
            return False
        return True

class Graph:
    def __init__(self, vertices):
        # non-weighted edges
        # directed
        
        self.mGraph = []
        for i in range(vertices):
            self.mGraph.append([])
        
    def addEdge(self, v0, v1):
        self.mGraph[v0].append(v1)
        
    def isEdge(self, v0, v1):
        return v1 in self.mGraph[v0]
    
    def getNeighbors(self, v):
        return self.mGraph[v]
        
    def findPath(self, v0, v1):
        # find shortest path (called breadth first search algorithm)
        # queue class
        
        Q = Queue()
        from_ = []
        
        for i in range(len(self.mGraph)):
            from_.append(-1)
        
        Q.Add(v0)
        from_[v0] = v0
        
        path = []
        
        while not Q.isEmpty():
            c = Q.Pop()
            if c == v1:
                # build path and return
                path.append(c)
                A = from_[c]
                while A != v0:
                    path.append(A)
                    A = from_[A]
                path.append(v0)
                path.reverse()
                return path
            
                '''
                
                c = Q.Pop()
                if c == v1:
                    path = [c]
                    while from_[c] != c:
                        c = from_[c]
                        path.append(c)
                    path.reverse()
                    return path
                
                '''
                
            for n in self.mGraph[c]:
                if from_[n] == -1:
                    Q.Add(n)
                    from_[n] = c
        return None