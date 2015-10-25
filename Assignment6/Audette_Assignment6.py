import getopt, sys


def parsed(opts, args):
    for o, a in opts:
        if o in ("-p"):
            print("flag", o)
            print("args", a)
            print(a[0])
            print(float(a[1:]))
            #setting the prior here works if the Bayes net is already built
            bNet.setPrior(a[0], float(a[1:]))
        elif o in ("-m"):
            print("flag", o)
            print("args", a)
            print(type(a))
            bNet.calcMarginal(a)
        elif o in ("-g"):
            print("flag", o)
            print("args", a)
            print(type(a))
            '''you may want to parse a here and pass the left of |
            and right of | as arguments to calcConditional
            '''
            p = a.find("|")
            print(a[:p])
            print(a[p+1:])
            print(bNet.calcConditional(a[:p], a[p+1:]))
        elif o in ("-j"):  ## JOINT PROBABILITY is wrapped in quotes and seperated by commas
            print("flag", o)
            print("args", a)
            p = a.find(",")
            straight = stringSplit(a)
            for i in range (0, len(straight)):
                for j in range(0, len(straight)):
                    if i >= j:
                        continue
                    else:
                        print(straight[i] + ',' + straight[j] + ':  ' + str(bNet.calcJoint(straight[i], straight[j])))
        else:
            assert False, "unhandled option"

def stringSplit(s):
    string = s.strip()
    lip = []
    string = string[0:len(string)].split(",")                    
    print(string)
    return string


class BNode:
    def __init__(self, name, currentProb = 0.0, parents = [], children = [], zeroCond = False, oneCond = True):
        self.name = name
        self.parents = parents
        self.children = children
        self.zeroCond = zeroCond
        self.oneCond = oneCond
        self.currentCond = None
        self.currentProb = currentProb
        if (zeroCond == False and oneCond == True):
            self.style = 'Boolean'
        else:
            self.style = 'Binary'
                

class BayesNet:
    def __init__(self, pProb = .9, sProb = .3):
        self.nodeSet = {'Pollution': BNode('Pollution', pProb, [], [], 'high', 'low'), 'Smoker': BNode('Smoker', sProb)}
        self.nodeSet['Cancer'] = BNode('Cancer', 0.0, [self.nodeSet['Pollution'], self.nodeSet['Smoker']])
        self.nodeSet['Pollution'].children.append( self.nodeSet['Cancer'])
        self.nodeSet['Smoker'].children.append(self.nodeSet['Cancer'])
        self.nodeSet['X-Ray'] = BNode('X-Ray', 0.0, [self.nodeSet['Cancer']])
        self.nodeSet['Cancer'].children.append(self.nodeSet['X-Ray'])
        self.nodeSet['Dyspnoea'] = BNode('Dyspnoea', 0.0, [self.nodeSet['Cancer']])
        self.nodeSet['Cancer'].children.append(self.nodeSet['Dyspnoea'])

    def setPrior(self, x, prob):
        if(x == 'P'):
            self.nodeSet['Pollution'].currentProb = prob
        elif (x == 'S'):
            self.nodeSet['Smoker'].currentProb = prob
        else:
            assert False, "Unrecognized Root Node"

    def calcMarginal(self, x):
        '''Return Marginal Probability Distribution of X'''
        smoke = 0.0
        pollute = 0.0
        cancer = 0.0
        dys = 0.0
        xray = 0.0
        if x == 'P':
            smoke = smoke + self.calcJoint(x, 's')
            smoke = smoke + self.calcJoint(x, '~s')
            cancer = cancer + self.calcJoint(x, 'c')
            cancer = cancer + self.calcJoint(x, '~c')
            dys = dys + self.calcJoint(x, 'd')
            dys = dys + self.calcJoint(x, '~d')
            xray = xray + self.calcJoint(x, 'x')
            xray = xray + self.calcJoint(x, '~x')
            print ('Pollution = Low Marginal Probability')
            print ('Smoker mP: ' + str(smoke))
            print ('Cancer mP: ' + str(cancer))
            print ('Dyspnoea mP: ' + str(dys))
            print ('X-Ray mP: ' + str(xray))
        elif x == 'S':
            pollute = pollute + self.calcJoint(x, 'p')
            pollute = pollute + self.calcJoint(x, '~p')
            cancer = cancer + self.calcJoint(x, 'c')
            cancer = cancer + self.calcJoint(x, '~c')
            dys = dys + self.calcJoint(x, 'd')
            dys = dys + self.calcJoint(x, '~d')
            xray = xray + self.calcJoint(x, 'x')
            xray = xray + self.calcJoint(x, '~x')
            print ('Smoker = True Marginal Probability')
            print ('Pollution mP: ' + str(pollute))
            print ('Cancer mP: ' + str(cancer))
            print ('Dyspnoea mP: ' + str(dys))
            print ('X-Ray mP: ' + str(xray))
        elif x == 'C':
            smoke = smoke + self.calcJoint(x, 's')
            smoke = smoke + self.calcJoint(x, '~s')
            pollute = pollute + self.calcJoint(x, 'p')
            pollute = pollute + self.calcJoint(x, '~p')
            dys = dys + self.calcJoint(x, 'd')
            dys = dys + self.calcJoint(x, '~d')
            xray = xray + self.calcJoint(x, 'x')
            xray = xray + self.calcJoint(x, '~x')
            print ('Cancer = True Marginal Probability')
            print ('Pollution mP: ' + str(pollute))
            print ('Smoker mP: ' + str(smoke))
            print ('Dyspnoea mP: ' + str(dys))
            print ('X-Ray mP: ' + str(xray))
        elif x == 'D':
            pollute = pollute + self.calcJoint(x, 'p')
            pollute = pollute + self.calcJoint(x, '~p')
            cancer = cancer + self.calcJoint(x, 'c')
            cancer = cancer + self.calcJoint(x, '~c')
            smoke = smoke + self.calcJoint(x, 's')
            smoke = smoke + self.calcJoint(x, '~s')
            xray = xray + self.calcJoint(x, 'x')
            xray = xray + self.calcJoint(x, '~x')
            print ('Dyspnoea = True Marginal Probability')
            print ('Pollution mP: ' + str(pollute))
            print ('Cancer mP: ' + str(cancer))
            print ('Smoker mP: ' + str(smoke))
            print ('X-Ray mP: ' + str(xray))
        elif x == 'X':
            pollute = pollute + self.calcJoint(x, 'p')
            pollute = pollute + self.calcJoint(x, '~p')
            cancer = cancer + self.calcJoint(x, 'c')
            cancer = cancer + self.calcJoint(x, '~c')
            smoke = smoke + self.calcJoint(x, 's')
            smoke = smoke + self.calcJoint(x, '~s')
            dys = dys + self.calcJoint(x, 'd')
            dys = dys + self.calcJoint(x, '~d')
            print ('X-Ray = Positive Marginal Probability')
            print ('Pollution mP: ' + str(pollute))
            print ('Cancer mP: ' + str(cancer))
            print ('Dyspnoea mP: ' + str(dys))
            print ('Smoker mP: ' + str(smoke))
        else:
            assert False, 'Bad Node'

    def calcConditional(self, x, y, xBool = None, yBool = None):
        '''Return Conditional Probablity of X | Y'''
        a = self.checker(x)
        if (xBool == None):
            aBool = self.truFalseCheck(x)
        else:
            aBool = xBool
        b = self.checker(y)
        if (yBool == None):
            bBool = self.truFalseCheck(y)
        else:
            bBool = yBool
        if a == self.nodeSet['Cancer'] and aBool == True:
            if b == self.nodeSet['Pollution']:
                if bBool == True:
                    return ( (0.03*self.nodeSet['Smoker'].currentProb) + (0.001*(1- self.nodeSet['Smoker'].currentProb)) )
                else:
                    return ( (0.05*self.nodeSet['Smoker'].currentProb) + (0.02*(1- self.nodeSet['Smoker'].currentProb)) )
            elif b == self.nodeSet['Smoker']:
                if bBool == True:
                    return ( (0.05 * (1 - self.nodeSet['Pollution'].currentProb)) + (0.03 * (self.nodeSet['Pollution'].currentProb)) )
                else:
                    return ( (0.02 * (1- self.nodeSet['Pollution'].currentProb)) + (0.001 * self.nodeSet['Pollution'].currentProb) )
            elif b == self.nodeSet['Dyspnoea']:
                if bBool == True:
                    return ( (self.calcConditional(y, x) * self.cancerProb())/ self.dyspProb())
                else:
                    return ( (self.calcConditional(y, x) * self.cancerProb())/ (1-self.dyspProb()))
            elif b == self.nodeSet['X-Ray']:
                if bBool == True:
                    return ( (self.calcConditional(y, x) * self.cancerProb())/ self.xRayProb())
                else:
                    return ( (self.calcConditional(y, x) * self.cancerProb())/ (1-self.xRayProb()) )
            else:
                assert False, "Invalid Effect"
        elif a == self.nodeSet['Pollution'] and aBool == True:
            if b == self.nodeSet['Cancer']:
                if bBool == True:
                    return ((self.calcConditional(y, x)*self.nodeSet['Pollution'].currentProb)/self.cancerProb() )
                else:
                    return ((self.calcConditional(y, x)*self.nodeSet['Pollution'].currentProb)/(1-self.cancerProb()))
            elif b == self.nodeSet['Smoker']:
                return a.currentProb
            elif b == self.nodeSet['Dyspnoea']:
                if bBool == True:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Pollution'].currentProb)/(self.dyspProb()))
                else:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Pollution'].currentProb)/ (1- self.dyspProb()))
            elif b == self.nodeSet['X-Ray']:
                if bBool == True:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Pollution'].currentProb)/(self.xRayProb()))
                else:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Pollution'].currentProb)/(1-self.xRayProb()))
            else:
                assert False, "Invalid Effect"
        elif a == self.nodeSet['Smoker'] and aBool == True:
            if b == self.nodeSet['Cancer']:
                if bBool == True:
                    return ((self.calcConditional(y,x)*self.nodeSet['Smoker'].currentProb)/self.cancerProb())
                else:
                    return ((self.calcConditional(y,x)*self.nodeSet['Smoker'].currentProb)/(1-self.cancerProb()))
            elif b == self.nodeSet['Pollution']:
                return a.currentProb
            elif b == self.nodeSet['Dyspnoea']:
                if bBool == True:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Smoker'].currentProb)/(self.dyspProb()))
                else:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Smoker'].currentProb)/ (1- self.dyspProb()))
            elif b == self.nodeSet['X-Ray']:
                if bBool == True:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Smoker'].currentProb)/(self.xRayProb()))
                else:
                    return ( (self.calcConditional(y, x) * self.nodeSet['Smoker'].currentProb)/(1-self.xRayProb()))
            else:
                assert False, "Invalid Effect"
        elif a == self.nodeSet['Dyspnoea'] and aBool == True:
            if b == self.nodeSet['Cancer']:
                if bBool == True:
                    return .65
                else:
                    return .3
            elif b == self.nodeSet['Pollution'] or b == self.nodeSet['Smoker']:
                return ( (self.calcConditional('c', y)*.65) + ( self.calcConditional('~c', y) * .3) )
            elif b == self.nodeSet['X-Ray']:
                return self.dyspProb()
            else:
                assert False, "Invalid Effect"
        elif a == self.nodeSet['X-Ray'] and aBool == True:
            if b == self.nodeSet['Cancer']:
                if bBool == True:
                    return .9
                else:
                    return .2
            elif b == self.nodeSet['Pollution'] or b == self.nodeSet['Smoker']:
                return ((self.calcConditional('c', y)*.9) + (self.calcConditional('~c', y)*.2))
            elif b == self.nodeSet['Dyspnoea']:
                return self.xRayProb()
            else:
                assert False, "Invalid Effect"
        else:
            return (1 - self.calcConditional(x, y, True))

    
    def cancerProb(self):
        return ( (0.05 * (1 - self.nodeSet['Pollution'].currentProb) * self.nodeSet['Smoker'].currentProb) +
                 (0.02 * (1 - self.nodeSet['Pollution'].currentProb) * (1- self.nodeSet['Smoker'].currentProb)) +
                 (0.03 * self.nodeSet['Smoker'].currentProb * self.nodeSet['Pollution'].currentProb) +
                 (0.001 * (1- self.nodeSet['Smoker'].currentProb) * self.nodeSet['Pollution'].currentProb))

    def dyspProb(self):
        return ( (self.cancerProb()*.65) + ( (1-self.cancerProb())*.3 ))

    def xRayProb(self):
        return ((self.cancerProb()*.9) + ( (1-self.cancerProb()) * .2))

    def defaultProb(self, y):
        if (y == 'P' or y == 'p'):
            return self.nodeSet['Pollution'].currentProb
        elif (y == '~p'):
            return (1 - self.nodeSet['Pollution'].currentProb)
        elif (y == 'S' or y == 's'):
            return self.nodeSet['Smoker'].currentProb
        elif (y == '~s'):
            return (1-self.nodeSet['Smoker'].currentProb)
        elif (y == 'C' or y == 'c'):
            return self.cancerProb()
        elif (y == '~c'):
            return (1 - self.cancerProb())
        elif (y == 'D' or y == 'd'):
            return self.dyspProb()
        elif (y == '~d'):
            return (1 - self.dyspProb())
        elif (y == 'X' or y == 'x'):
            return self.xRayProb()
        elif (y == '~x'):
            return (1-self.xRayProb())
        else:
            assert False, 'No valid default prob'
        

    def calcJoint(self, x, y):
        '''Return Joint Probability of X, Y'''
        return (self.calcConditional(x, y)*self.defaultProb(y))

    def checker(self, x):
        if (x == 'P' or x == 'p' or x == '~p'):
            return self.nodeSet['Pollution']
        elif (x == 'S' or x == 's' or x == '~s'):
            return self.nodeSet['Smoker']
        elif (x == 'C' or x == 'c' or x == '~c'):
            return self.nodeSet['Cancer']
        elif (x == 'D' or x == 'd' or x == '~d'):
            return self.nodeSet['Dyspnoea']
        elif (x == 'X' or x == 'x' or x == '~x'):
            return self.nodeSet['X-Ray']

    def truFalseCheck(self, x):
        if x[0] == '~':
            return False
        else:
            return True
        
        

bNet = BayesNet()
try:
    opts, args = getopt.getopt(sys.argv[1:], 'g:j:m:p:')
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)
parsed(opts, args)
