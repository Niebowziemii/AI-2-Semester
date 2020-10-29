from random import sample, shuffle,seed
from time import perf_counter,sleep
from itertools import combinations
import matplotlib.pyplot as plt
import multiprocessing

class GraphFromAdjacencyMatrix(object):
    def __init__(self,size):
        self.matrix=[[0 for i in range(size)] for j in range(size)]
        self.size=size
        self.edgeCounter=0
    def __len__(self):
        return self.size
    def __str__(self):
        result=""
        for row in self.matrix:
            for val in row:
                result=result+ str(val)+' '
            result=result+'\n'
        return result
    def insertEdge(self,v1,v2):
        if v1==v2:
            self.matrix[v1][v1]=1
            self.edgeCounter+=1
        else:
            self.matrix[v1][v2]=1
            self.matrix[v2][v1]=1
            self.edgeCounter+=1

    def isEdge(self,v1,v2):
        if self.matrix[v1][v2] and self.matrix[v2][v1]:
            return True
        else:
            return False
    def checkIfNeighboursOrIfVisitedAready(self,index,vertice,solution):
        if self.matrix[solution[index-1]][vertice]==0:
            return False
        if vertice in solution:
            return False
        return True
    def checkIfHamiltonianCycleExist(self,solution,index):
        if index == self.size:
            if self.matrix[solution[index-1]][solution[0]]==1:
                return True
            else:
                return False
        for vertice in range(1,self.size):
            if self.checkIfNeighboursOrIfVisitedAready(index,vertice,solution):
                solution[index]=vertice
                if self.checkIfHamiltonianCycleExist(solution,index+1):
                    return True
            solution[index]=-1
        return False
    def printHamiltonianCycleIfExist(self):
        solution = [-1 for i in range(self.size)]
        solution[0] = 0
        if self.checkIfHamiltonianCycleExist(solution,1):
            for vertice in solution:
                print(vertice, end=" -> ")
            print(solution[0])
            return True
        else:
            print("There is no Hamiltonian Cycle")
            return False
    def bufferUpTo300Sec(self):
        p = multiprocessing.Process(target=self.printHamiltonianCycleIfExist,name="Function")
        p.start()
        p.join(300)
        if p.is_alive():
            print("Time is up +300s to the time")
            p.terminate()
            p.join()

if __name__== '__main__':
    f=open("wynik.txt","w")
    for p in range(10):
        sizes=[20,40,60,80,100,200,300]
        saturations=[0.2,0.3,0.4,0.6,0.8,0.95]
        timeHamDict={0.2:[],0.3:[],0.4:[],0.6:[],0.8:[],0.95:[]}
        for size in sizes:
            for saturation in saturations:
                #create data
                notVisitedVerticesSet = set([i for i in range(size)])
                connectedVerticesSet = set([])
                possibleNumOfEdges=size*(size-1)/2
                graphMatrixObject = GraphFromAdjacencyMatrix(size)
                #choose first vertice
                buffNot=sample(notVisitedVerticesSet,1)[0]
                notVisitedVerticesSet.remove(buffNot)
                connectedVerticesSet.add(buffNot)
                #connect the graph
                while len(notVisitedVerticesSet):
                    buffNot=sample(notVisitedVerticesSet,1)[0]
                    buffYes=sample(connectedVerticesSet,1)[0]
                    graphMatrixObject.insertEdge(buffYes,buffNot)
                    notVisitedVerticesSet.remove(buffNot)
                    connectedVerticesSet.add(buffNot)
                pairbase=(list(combinations(connectedVerticesSet,2)))
                # create rest of the edges
                shuffle(pairbase)
                while possibleNumOfEdges*saturation >graphMatrixObject.edgeCounter:
                    graphMatrixObject.insertEdge(pairbase[0][0],pairbase[0][1])
                    pairbase.pop(0)

                print("============================\n")
                # print(graphMatrixObject)
                print("HAMILTONIAN CYCLE: ")
                start=perf_counter()
                graphMatrixObject.bufferUpTo300Sec()
                stop = perf_counter()
                timeHamDict.get(saturation).append(stop - start)
                print(f"SIZE AND SATURATION: {size}, {saturation} \n============================\n")
        f.write(str(timeHamDict))
        f.write("\n")

    #generating plots
    def plots(name, x, y):
        plt.plot(x, y, label=name)

    # plot 2
    plt.rcParams['figure.figsize'] = [15, 5]
    plt.xlabel('Number of elements')
    plt.ylabel('Searching time (in seconds)')
    plt.title("Plot 2 - time of searching hamiltonian cycle in an undirected graph\
     (n vertices) with different edge saturation")
    plots("Saturation: 0.2", sizes, timeHamDict.get(0.2))
    plots("Saturation: 0.3", sizes, timeHamDict.get(0.3))
    plots("Saturation: 0.4", sizes, timeHamDict.get(0.4))
    plots("Saturation: 0.6", sizes, timeHamDict.get(0.6))
    plots("Saturation: 0.8", sizes, timeHamDict.get(0.8))
    plots("Saturation: 0.95", sizes, timeHamDict.get(0.95))
    plt.legend(loc="upper left")
    plt.show()
    plt.clf()
    plt.cla()
    plt.close()
