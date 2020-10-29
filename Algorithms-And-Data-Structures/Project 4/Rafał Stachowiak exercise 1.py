from random import sample, shuffle,seed
from time import perf_counter,sleep
from itertools import combinations
import matplotlib.pyplot as plt

class GraphFromAdjacencyList(object):
    def __init__(self,size):
        self.matrix=[[] for i in range(size)]
        self.size=size
        self.edgeCounter=0

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.matrix)

    def insertEdge(self,v1,v2):
        if not self.isEdge(v1,v2):
            self.matrix[v1].append(v2)
            self.matrix[v2].append(v1)
            self.edgeCounter+=1

    def removeEdge(self,v1,v2):
        for index, vertice in enumerate(self.matrix[v1]):
            if vertice==v2:
                self.matrix[v1].pop(index)
        for index, vertice in enumerate(self.matrix[v2]):
            if vertice==v1:
                self.matrix[v2].pop(index)

    def isEdge(self,v1,v2):
        if v1 in self.matrix[v2] and v2 in self.matrix[v1]:
            return True
        else:
            return False

    def isEmpty(self):
        flag =True
        for list in self.matrix:
            if len(list) is not 0:
                return False
        return False
def convertEdgeListToAdjList(edgeList,adjList):
    for edgepair in edgeList:
        adjList.insertEdge(edgepair[0],edgepair[1])
def Hierholzer(adjList,verticeList):
    stack=[]
    result=[]
    stack.append(0)
    v=adjList.matrix[0][0]
    while stack:
        u = stack[-1]
        while adjList.matrix[u]:
            v=sample(adjList.matrix[u],1)[0]
            adjList.removeEdge(u,v)
            stack.append(v)
            u = v
        buffStack = stack.pop()
        result.append(buffStack)
    return result


if __name__== '__main__':
    sizes=[12,24,36,48,60,72,84,96,100,200,300]
    saturations=[0.2,0.3,0.4,0.6,0.8,0.95]
    timeDict={0.2:[],0.3:[],0.4:[],0.6:[],0.8:[],0.95:[]}
    for size in sizes:
        for saturation in saturations:
            #create data
            print(f"generowanie grafu...{saturation}, {size}")
            notVisitedVerticesSet = [i for i in range(size)]
            connectedVerticesSet = notVisitedVerticesSet.copy()
            possibleNumOfEdges=size*(size-1)/2
            edgeList=[]
            #choose first vertice
            buffNot=sample(notVisitedVerticesSet,2)
            notVisitedVerticesSet.remove(buffNot[1])
            notVisitedVerticesSet.remove(buffNot[0])
            edgeList.append(buffNot)
            #connect the graph
            while len(notVisitedVerticesSet):
                buffNot=sample(notVisitedVerticesSet,1)[0]
                buffYes=edgeList[-1]
                edgeList.append([buffYes[1],buffNot])
                notVisitedVerticesSet.remove(buffNot)
            edgeList.append([edgeList[-1][1],edgeList[0][0]])
            threeVertices = list(combinations(connectedVerticesSet, 3))
            counter = len(edgeList)
            for triple in threeVertices:
                if counter < saturation * possibleNumOfEdges:
                    # print(counter, possibleNumOfEdges * saturation)
                    if [triple[0], triple[1]] not in edgeList and [triple[1], triple[0]] not in edgeList \
                            and [triple[0], triple[2]] not in edgeList and [triple[2], triple[0]] not in edgeList \
                            and [triple[1], triple[2]] not in edgeList and [triple[2], triple[1]] not in edgeList:
                        edgeList.append([triple[0], triple[1]])
                        edgeList.append([triple[0], triple[2]])
                        edgeList.append([triple[1], triple[2]])
                        counter += 3
                else:
                    continue
            print("Graf wygenerowany")
            adjList=GraphFromAdjacencyList(size)
            convertEdgeListToAdjList(edgeList,adjList)
            # print(edgeList)
            # print(graphMatrixObject)
            print("============================\nEULERIAN CYCLE: ")
            start=perf_counter()
            a = Hierholzer(adjList,connectedVerticesSet)
            stop = perf_counter()
            timeDict.get(saturation).append(stop - start)
            for num in range(0,len(a)-1,1):
                print(f"{a[num]} -> ", end="")
            print(a[-1])

            print(f"SIZE AND SATURATION: {size}, {saturation} \n============================\n")
        print(timeDict)

    #generating plots
    def plots(name, x, y):
        plt.plot(x, y, label=name)
    # plot 1
    plt.rcParams['figure.figsize'] = [15, 5]
    plt.xlabel('Number of elements')
    plt.ylabel('Searching time (in seconds)')
    plt.title("Plot 1 - time of searching eulerian cycle in an undirected graph\
     (n vertices) with different edge saturation")
    plots("Saturation: 0.2", sizes, timeDict.get(0.2))
    plots("Saturation: 0.3", sizes, timeDict.get(0.3))
    plots("Saturation: 0.4", sizes, timeDict.get(0.4))
    plots("Saturation: 0.6", sizes, timeDict.get(0.6))
    plots("Saturation: 0.8", sizes, timeDict.get(0.8))
    plots("Saturation: 0.95", sizes, timeDict.get(0.95))
    plt.legend(loc="upper left")
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()
