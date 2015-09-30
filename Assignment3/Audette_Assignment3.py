from Lib import queue
import math
import sys

class NNode:
    def __init__(self, locx, locy, kind = 2, disT = 999999999, parent = None):
        self.x = locx
        self.y = locy
        self.k = kind
        self.dist = disT
        self.parent = parent
        self.adj = []
        self.h = float('inf')

    def addAdj(self, node):
        self.adj.append(node)

    def heuristic(self, heu, end):
        val = 0
        if heu == 1: #Manhatten Distance
            if end.x > self.x:
                val = val + (end.x-self.x)*10
            else:
                val = val + (self.x-end.x)*10
            if end.y > self.y:
                val = val + (end.y-self.y)*10
            else:
                val = val + (self.y-end.y)*10
            return int(val)
        else: #Straight Line Distance
            if end.x > self.x:
                valx = end.x - self.x
            else:
                valx = self.x-end.x
            if end.y > self.y:
                valy = end.y - self.y
            else:
                valy = self.y - end.y
            val = math.floor(math.sqrt((valx*valx)+(valy*valy))*10)
            return int(val)


def actualDist(fro, to):
    if(((fro.x+fro.y) - (to.x+to.y) == 2) or ((fro.x+fro.y) - (to.x+to.y) == -2) or ((fro.x+fro.y) - (to.x+to.y) == 0)):
        if(to.k == 0):
            return 14
        elif(to.k == 1):
            return 24
        else:
            return 9999
    else:
        if(to.k == 0):
            return 10
        elif(to.k == 1):
            return 20
        else:
            return 9999


def readIn(fileName):
    f = open(fileName)
    graph = []
    ypos = 0
    for line in f:
        l = line
        lit = []
        for i in range(0, len(l)):
            if l[i] == '0':
                n = NNode(math.floor(i/2), ypos, 0)
                lit.append(n)
            elif l[i] == '1':
                n = NNode(math.floor(i/2), ypos, 1)
                lit.append(n)
            elif l[i] == '2':
                n = NNode(math.floor(i/2), ypos, 2)
                lit.append(n)
        graph.append(lit)
        ypos = ypos + 1
    for i in range(0, len(graph)):
        for j in range(0, len(graph[i])):
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if(x == 0 and y == 0):
                        hold = None
                    elif (y+i < 0 or y+i >= len(graph) or x+j < 0 or x+j >= len(graph[i])):
                        hold = None
                    elif (graph[i+y][j+x].k != 2):
                        graph[i][j].addAdj(graph[i+y][j+x])
    
    return graph
        
        

def aStar(start, end, heu):
    openL = queue.PriorityQueue()
    start.dist = 0
    start.h = start.dist + start.heuristic(heu, end)
    openL.put((start.h, 0, start))
    closedL = []
    dumbprior = 0
    while not openL.empty():
        node = openL.get()[2]
        if node == end:
            reconstruct(start, end)
            break
        else:
            closedL.append(node)
            for n in node.adj:
                if (n in closedL) or (n.k == 2):
                    continue
                g = node.dist + actualDist(node, n)
                if n not in openL.queue or g < n.dist:
                    n.dist = g
                    n.h = n.heuristic(heu, end) + g
                    n.parent = node
                    if n not in openL.queue:
                        dumbprior = dumbprior + 1
                        openL.put((n.h, dumbprior, n))
    

def reconstruct(start, end):
    path = []
    pathr = []
    cost = end.dist
    numLoc = 0
    cNode = end
    while cNode != start:
        path.append((str(cNode.x), str(cNode.y)))
        numLoc = numLoc + 1
        cNode = cNode.parent
    path.append((str(cNode.x), str(cNode.y)))
    while len(path) != 0:
        pathr.append(path.pop())
    print('The Path Taken in (X, Y), with lower numbers starting from the upper left')
    print(pathr)
    print('The number of locations visited: ' + str(len(pathr)))
    print('The cost of the final path: ' + str(cost))
    

if(len(sys.argv) == 1):
    print('No Text File read in')
elif(len(sys.argv) == 2):
    g = readIn(sys.argv[1])
    print(str(g[len(g)-1][0].y))
    aStar(g[len(g)-1][0], g[0][len(g[len(g)-1])-1], 1)
else:
    g = readIn(sys.argv[1])
    aStar(g[len(g)-1][0], g[0][len(g[len(g)-1])-1], int(sys.argv[2]))



