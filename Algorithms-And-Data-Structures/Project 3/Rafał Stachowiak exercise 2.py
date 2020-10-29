from itertools import permutations
from random import shuffle
from time import perf_counter
import matplotlib.pyplot as plt
from math import log2
class AdjacencyMatrix(object):
    def __init__(self,size):
        self.matrix=[]
        for i in range(size):
            self.matrix.append([0 for i in range(size)])
        self.size=size
    def __len__(self):
        return self.size
    def __str__(self):
        retu=""
        for row in self.matrix:
            for el in row:
                retu+=str(el)+str(" ")
            retu+=str('\n')
        return retu
    def insertEdge(self,v1,v2):
        '''
        inserts an edge to a matrix
        :param v1: "source" "out_edge"
        :param v2: "destination" "in_edge"
        :return:
        '''
        self.matrix[v1][v2]=1

def topologicalSortingAM(adjacencyMatrix):
    sortedArray=[]
    visited=[0 for i in range(adjacencyMatrix.size)]
    in_degree=[0 for i in range(adjacencyMatrix.size)]
    for i in range(adjacencyMatrix.size):
        for j in range(adjacencyMatrix.size):
            if adjacencyMatrix.matrix[i][j] == 1:
                in_degree[j]=in_degree[j]+1
    queue=[]
    for i in range(adjacencyMatrix.size):
        if in_degree[i] is 0:
            queue.append(i)
            visited[i]=True
    while queue:
        vertex=queue[0]
        queue.pop(0)
        sortedArray.append(vertex)
        for j in range(adjacencyMatrix.size):
            if adjacencyMatrix.matrix[vertex][j] == 1 and visited[j] == 0:
                in_degree[j] = in_degree[j]-1
                if in_degree[j]==0:
                    queue.append(j)
                    visited[j]=True
    return sortedArray if len(sortedArray) == adjacencyMatrix.size else []

def printIfBeginCountingFromOne(list):
    return [i+1 for i in list]

# object = AdjacencyMatrix(9)
# object.insertEdge(0,2)
# object.insertEdge(0,1)
# object.insertEdge(0,3)
# object.insertEdge(8,3)
# object.insertEdge(2,5)
# object.insertEdge(2,4)
# object.insertEdge(5,4)
# object.insertEdge(1,6)
# object.insertEdge(6,7)
# if topologicalSortingAM(object)==[]:
#     print("[error] not sorted correctly - this graph is not acyclic")
# else:
#     print("udało się ")
#
# print("topologically sorted list of vertices: ",printIfBeginCountingFromOne(topologicalSortingAM(object)))
#
# object2 = AdjacencyMatrix(14)
# object2.insertEdge(1,0)
# object2.insertEdge(0,2)
# object2.insertEdge(1,4)
# object2.insertEdge(2,4)
# object2.insertEdge(2,10)
# object2.insertEdge(2,3)
# object2.insertEdge(3,11)
# object2.insertEdge(11,12)
# object2.insertEdge(3,10)
# object2.insertEdge(3,7)
# object2.insertEdge(5,12)
# object2.insertEdge(13,12)
# object2.insertEdge(13,6)
# object2.insertEdge(6,5)
# object2.insertEdge(5,9)
# object2.insertEdge(7,6)
# object2.insertEdge(10,7)
# object2.insertEdge(4,7)
# object2.insertEdge(8,4)
# object2.insertEdge(9,8)
#
# if topologicalSortingAM(object2)==[]:
#     print("[error] not sorted correctly - this graph is not acyclic")
# else:
#     print("udało się ")
#     print("topologically sorted list of vertices: ",printIfBeginCountingFromOne(topologicalSortingAM(object2)))


verticeNum=[100,200,300,400,500,1000,1100,1200,1300,1400,1500,2000,3000,4000,5000,6000,7000,8000,9000,10000]
timeAdjacencyMatrixInLoop=[]
for size in verticeNum:
    # generowanie danych
    adjacencyMatrix=AdjacencyMatrix(size)
    allPairs=[]
    saturation=0.3
    for rowIndex in range(1,adjacencyMatrix.size,1):
        for colIndex in range(0,rowIndex,1):
            allPairs.append([rowIndex,colIndex])
    shuffle(allPairs)
    allowedPairs=allPairs[:int(len(allPairs)*saturation)]
    for pair in allowedPairs:
        adjacencyMatrix.insertEdge(pair[0],pair[1])
    # mierzenie czasu
    start=perf_counter()
    if topologicalSortingAM(adjacencyMatrix)==[]:
        print("[error] not sorted correctly - this graph is not acyclic")
    else:
        print("udało się ")
    stop =  perf_counter()
    timeAdjacencyMatrixInLoop.append(stop-start)
    print("vertice list: ",allowedPairs,"edges number: ",int(len(allPairs)*saturation))
    print("topologically sorted list of vertices: ",topologicalSortingAM(adjacencyMatrix))
print("time of sorting: ",timeAdjacencyMatrixInLoop)
# generating plots

def plots(name, x, y):
    plt.plot(x, y, label=name)


# plot 1
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Searching time (in seconds)')
plt.title("Plot 1 - Time of topological sorting a graph with n vertices")
plots("Adjacency matrix", verticeNum, timeAdjacencyMatrixInLoop)
plots("nlogn line",verticeNum,[i*log2(i) for i in verticeNum])
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()