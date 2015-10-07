from Lib import heapq
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
        self.r = self.reward();
        self.u = 0
        self.uprime = 0
        self.state = (self.x, self.y)

    def addAdj(self, node):
        self.adj.append(node)

    def reward(self):
        if self.k == 0:
            return 0
        elif self.k == 1:
            return -1.0
        elif self.k == 3:
            return -2.0
        elif self.k ==  4:
            return 1.0
        elif self.k == 50:
            return 50.0
        else:
            return 0

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
                valx = (end.x - self.x)*10
            else:
                valx = (self.x-end.x)*10
            if end.y > self.y:
                valy = (end.y - self.y)*10
            else:
                valy = (self.y - end.y)*10
            val = math.floor(math.sqrt((valx*valx)+(valy*valy)))
            return int(val)


def actualDist(fro, to):
    if(fro == to):
        return 0
    if(diagCheck(fro, to)):
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

def diagCheck(fro, to):
    if (fro.x - to.x == 1 or fro.x - to.x == -1):
        if (fro.y - to.y == 1 or fro.y - to.y == -1):
            return True
        else:
            return False
    else:
        return False

def valueIter(graph, epsilon = .5):
    delta = float('inf')
    uprime = 0
    count = 0
    while delta >= (epsilon * .1)/.9:
        for i in range(0, len(graph)):
            for n in graph[i]:
                n.u = n.uprime
        delta = 0
        count = count + 1
        for i in range(0, len(graph)):
            for n in graph[i]:
                uprime = 0
                uprime = n.r + .9*maxSumProb(n, len(graph[i])-1, len(graph)-1)
                if (abs(uprime - n.u) > delta):
                    delta = abs(uprime - n.u)
                n.uprime = uprime
    print(count)

def maxSumProb(n, lenx, leny):
    val = 0
    final = 0
    for k in n.adj:
        val = (transition(k.state, (0,1), n.state, lenx, leny)*k.u)
        val = val + (transition(k.state, (0,-1), n.state, lenx, leny)*k.u)
        val = val + (transition(k.state, (1, 0), n.state, lenx, leny)*k.u)
        val = val + (transition(k.state, (-1, 0), n.state, lenx, leny)*k.u)
        ##val = val*k.u
        ##val = transition(k.state, (k.state[0]-n.state[0], k.state[1]-n.state[1]), n.state, lenx, leny)*k.u
        final = max(val, final)
    return final

def transition(stateprime, action, state, lenx, leny):
    if (action == (0,1)):
        ##if(state[0] != 0 and state[0] != lenx):
        if (stateprime == (state[0], state[1]+1)):
            return 0.8
        elif (stateprime == (state[0]+1, state[1])):
            return 0.1
        elif (stateprime == (state[0]-1, state[1])):
            return 0.1
        else:
            return 0
            '''
        elif (state[0] == 0):
            if (stateprime == (state[0], state[1]+1)):
                return 0.9
            elif (stateprime == (state[0]+1, state[1])):
                return 0.1
            else:
                return 0
        else:
            if (stateprime == (state[0], state[1]+1)):
                return 0.9
            elif (stateprime == (state[0]-1, state[1])):
                return 0.1
            else:
                return 0
                '''
    elif (action == (0,-1)):
        ##if (state[0] != 0 and state[0] != lenx):
        if (stateprime == (state[0], state[1]-1)):
            return 0.8
        elif (stateprime == (state[0]+1, state[1])):
            return 0.1
        elif (stateprime == (state[0]-1, state[1])):
            return 0.1
        else:
            return 0
            '''
        elif (state[0] == 0):
            if (stateprime == (state[0], state[1]-1)):
                return 0.9
            elif (stateprime == (state[0]+1, state[1])):
                return 0.1
            else:
                return 0
        else:
            if (stateprime == (state[0], state[1]-1)):
                return 0.9
            elif (stateprime == (state[0]-1, state[1])):
                return 0.1
            else:
                return 0
                '''
    elif (action == (1, 0)):
        ##if (state[1] != leny and state[1] != 0):
        if (stateprime == (state[0]+1, state[1])):
            return 0.8
        elif (stateprime == (state[0], state[1]+1)):
            return 0.1
        elif (stateprime == (state[0], state[1]-1)):
            return 0.1
        else:
            return 0
            '''
        elif (state[1] == 0):
            if (stateprime == (state[0]+1, state[1])):
                return 0.9
            elif (stateprime == (state[0], state[1]+1)):
                return 0.1
            else:
                return 0
        else:
            if (stateprime == (state[0]+1, state[1])):
                return 0.9
            elif (stateprime == (state[0], state[1]-1)):
                return 0.1
            else:
                return 0
                '''
    elif (action == (-1, 0)):
        ##if(state[1] != 0 and state[1] != leny):
        if (stateprime == (state[0]-1, state[1])):
            return 0.8
        elif (stateprime == (state[0], state[1]+1)):
            return 0.1
        elif (stateprime == (state[0], state[1]-1)):
            return 0.1
        else:
            return 0
            '''
        elif(state[1] == 0):
            if (stateprime == (state[0]-1, state[1])):
                return 0.9
            elif (stateprime == (state[0], state[1]+1)):
                return 0.1
            else:
                return 0
        else:
            if (stateprime == (state[0]-1, state[1])):
                return 0.9
            elif (stateprime == (state[0], state[1]-1)):
                return 0.1
            else:
                return 0
                '''
    else:
        return 0


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
            elif l[i] == '3':
                n = NNode(math.floor(i/2), ypos, 3)
                lit.append(n)
            elif l[i] == '4':
                n = NNode(math.floor(i/2), ypos, 4)
                lit.append(n)
            elif l[i] == '5':
                n = NNode(math.floor(i/2), ypos, 50)
                lit.append(n)
                break
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
                    elif (graph[i+y][j+x].k != 2 and not diagCheck(graph[i][j], graph[i+y][j+x])):
                        graph[i][j].addAdj(graph[i+y][j+x])

    return graph



def aStar(start, end, heu):
    openL = []
    ##start.dist = 0
    start.h = start.u + start.r ##start.dist + start.heuristic(heu, end)
    heapq.heappush(openL, ((start.h)*-1, 0, start))
    closedL = []
    dumbprior = 0
    while not len(openL) == 0:
        node = heapq.heappop(openL)[2]
        if node == end:
            reconstruct(start, end)
            break
        else:
            closedL.append(node)
            for n in node.adj:
                if (n in closedL) or (n.k == 2):
                   continue
                g = node.u + n.r ##node.dist + actualDist(node, n)
                if g < n.u: ##< n.dist:
                    n.u = g ##dist = g
                    n.h = n.r + g ##n.heuristic(heu, end) + g
                    n.parent = node
                    if n not in openL:
                        dumbprior = dumbprior + 1
                        heapq.heappush(openL, ((n.h)*-1, dumbprior, n))


def reconstruct(start, end):
    path = []
    pathr = []
    cost = end.u
    numLoc = 0
    cNode = end
    while cNode != start:
        path.append((str(cNode.x), str(cNode.y), 'U: ' + str(cNode.u)))
        numLoc = numLoc + 1
        cNode = cNode.parent
    path.append((str(cNode.x), str(cNode.y), 'U: ' + str(cNode.u)))
    while len(path) != 0:
        pathr.append(path.pop())
    print('The Path Taken (X, Y, Utility), with lower numbers starting from the upper left')
    print(pathr)
    print('The number of locations visited: ' + str(len(pathr)))

if(len(sys.argv) == 1):
    print('No Text File read in')
elif(len(sys.argv) == 2):
    g = readIn(sys.argv[1])
    valueIter(g)
    aStar(g[len(g)-1][0], g[0][len(g[len(g)-1])-1], 1)
else:
    g = readIn(sys.argv[1])
    valueIter(g, float(sys.argv[2]))
    aStar(g[len(g)-1][0], g[0][len(g[len(g)-1])-1], 1)


