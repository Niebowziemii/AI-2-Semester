from itertools import combinations_with_replacement
from random import shuffle,randint
from time import perf_counter
# import matplotlib.pyplot as plt
class GraphFromAdjacencyMatrix(object):
    def __init__(self,size):
        self.matrix=[]
        for i in range(size):
            self.matrix.append([0 for i in range(size)])
        self.size=size
    def __len__(self):
        return self.size
    def __str__(self):
        result=""
        for row in self.matrix:
            for val in row:
                result=result+ str(val)+' '
            result=result+'\\'
        return result
    def insertEdge(self,v1,v2):
        if v1==v2:
            self.matrix[v1][v1]=1
        else:
            self.matrix[v1][v2]=1
            self.matrix[v2][v1]=1
    def isEdge(self,v1,v2):
        if self.matrix[v1][v2] and self.matrix[v2][v1]:
            return True
        else:
            return False

class GraphFromIncidenceMatrix(object):
    def __init__(self, size):
        self.size = size
        edgeNum = 0.6*(self.size * (self.size - 1) * 0.5 + self.size)
        self.matrix = [[] for i in range(int(edgeNum))]

    def __len__(self):
        return self.size

    def __str__(self):
        result = ""
        for row in self.matrix:
            for val in row:
                result = result + str(val) + ' '
            result = result + '\\'
        return result

    def insertEdge(self,v1,v2):
        edgeNum = 0.6*(self.size * (self.size - 1) * 0.5 + self.size)
        for row in range(int(edgeNum)):
            if len(self.matrix[row]) ==0:
                for col in range(self.size):
                    if col==v1 or col==v2:
                        self.matrix[row].append(1)
                    else:
                        self.matrix[row].append(0)
                break
    def isEdge(self,v1,v2):
        for row in self.matrix:
            if row[v1] and row[v2] :
                return True
        return False

def listToString(edgeList):
    result=""
    for i in range(len(edgeList)):
        result+=str(edgeList[i][0])+' '+str(edgeList[i][1])+'\\'
    return result
def isEdgeInList(pair,list):
    revpair=[pair[1],pair[0]]
    return (pair in list or revpair in list)
def incListToString(incList):
    result=""
    for sublist in incList:
        for index in range(1,len(sublist),1):
            result=result+str(sublist[index])+' '
        result+='\\'
    return result
def isEdgeInIncList(incList,pair):
    if pair[1] in incList[pair[0]] or  pair[0] in incList[pair[1]]:
        return True
    return False
# WRITING IN THE FILE GRAPH REPRESENTATIONS
num=[5]#,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
arrayfulltimeAM=[]
arrayfulltimeIM=[]
arrayfulltimeEL=[]
arrayfulltimeIL=[]
avearrayfulltimeAM=[]
avearrayfulltimeIM=[]
avearrayfulltimeEL=[]
avearrayfulltimeIL=[]
for size in num:
    #vertex matrix
    edgeNum=size*(size-1)*0.5+size
    indexList=[i for i in range(size)]
    graphFromAdjacencyMatrix=GraphFromAdjacencyMatrix(size)
    allEdgesList=list(combinations_with_replacement(indexList,2))
    shuffle(allEdgesList)
    saturationBorder=0.6*edgeNum
    buff=0
    for pair in allEdgesList:
        if buff<saturationBorder:
            graphFromAdjacencyMatrix.insertEdge(pair[0],pair[1])
            buff+=1
    fileGraphFromAdjacencyMatrixWrite = open("fileGraphFromAdjacencyMatrix.txt","w")
    fileGraphFromAdjacencyMatrixWrite.write(str(graphFromAdjacencyMatrix))
    fileGraphFromAdjacencyMatrixWrite.close()
    print(graphFromAdjacencyMatrix)
    #incidence matrix
    graphFromIncidenceMatrix=GraphFromIncidenceMatrix(size)
    buff=0
    for pair in allEdgesList:
        if buff<saturationBorder:
            graphFromIncidenceMatrix.insertEdge(pair[0],pair[1])
            buff+=1
    fileGraphFromIncidenceMatrixWrite = open("fileGraphFromIncidenceMatrix.txt","w")
    fileGraphFromIncidenceMatrixWrite.write(str(graphFromIncidenceMatrix))
    fileGraphFromIncidenceMatrixWrite.close()
    print(graphFromIncidenceMatrix)
    # edge list
    graphFromEdgeList=[]
    buff=0
    for pair in allEdgesList:
        if buff<saturationBorder:
            graphFromEdgeList.append([pair[0],pair[1]])
            buff+=1
    graphFromEdgeListWrite = open("fileGraphFromEdgeList.txt","w")
    graphFromEdgeListWrite.write(listToString(graphFromEdgeList))
    graphFromEdgeListWrite.close()
    print(graphFromEdgeList)
    # incidence list
    buff=0
    graphFromIncidenceList = [['{}:'.format(i)]for i in range(int(size))]
    while buff<saturationBorder:
        edge=randint(0,size-1)
        vertice=randint(0,size-1)
        if int(vertice) not in graphFromIncidenceList[edge] and edge not in graphFromIncidenceList[int(vertice)] and edge is not int(vertice):
            graphFromIncidenceList[edge].append(int(vertice))
            graphFromIncidenceList[int(vertice)].append(int(edge))
            buff+=1
        elif edge not in graphFromIncidenceList[int(vertice)] and edge is int(vertice):
            graphFromIncidenceList[int(vertice)].append(int(edge))
            buff += 1
    graphFromIncidenceListWrite = open("fileGraphFromIncidenceList.txt","w")
    graphFromIncidenceListWrite.write(incListToString(graphFromIncidenceList))
    graphFromIncidenceListWrite.close()
    print(graphFromIncidenceList)
    # READING FORM THE FILE AND TIME COUNTING
    # adjacency matrix
    fileGraphFromAdjacencyMatrixOpen = open("fileGraphFromAdjacencyMatrix.txt","r")
    buffMatrix=fileGraphFromAdjacencyMatrixOpen.readlines()
    buffMatrix=[i for i in buffMatrix[0].split("\\")]
    buffMatrix.pop(-1)
    buffMatrix=[[i for i in buffMatrix[i].split(" ")]for i in range(size)]
    for numList in buffMatrix:
        numList.pop(-1)
    buffMatrix=[[int(i) for i in buffMatrix[i]]for i in range(size)]
    edgesList=[]
    for row in range(len(buffMatrix)):
        for col  in range(row,len(buffMatrix),1):
            if buffMatrix[row][col]:
                edgesList.append([row,col])
    shuffle(edgesList)
    graphFromAdjacencyMatrixRead=GraphFromAdjacencyMatrix(size)
    for pair in edgesList:
        graphFromAdjacencyMatrixRead.insertEdge(pair[0],pair[1])
    timeOfSearchingAdjastmentMatrix=[]
    print("Adjacency Matrix")
    for pair in edgesList:
        start=perf_counter()
        a=graphFromAdjacencyMatrixRead.isEdge(pair[0],pair[1])
        stop=perf_counter()
        if(a):
            print("udało się ", pair)
        else:
            print("nie udało się ",pair)
        timeOfSearchingAdjastmentMatrix.append(stop-start)
    fileGraphFromAdjacencyMatrixOpen.close()
    # incident matrix
    fileGraphFromIncidenceMatrixOpen = open("fileGraphFromIncidenceMatrix.txt","r")
    buffMatrix=fileGraphFromIncidenceMatrixOpen.readlines()
    buffMatrix=[i for i in buffMatrix[0].split("\\")]
    buffMatrix.pop(-1)
    buffMatrix=[[i for i in buffMatrix[i].split(" ")]for i in range(int(0.6*edgeNum))]
    for numList in buffMatrix:
        numList.pop(-1)
    buffMatrix=[[int(i) for i in buffMatrix[i]]for i in range(int(0.6*edgeNum))]
    edgesList=[]
    for row in range(len(buffMatrix)):
        count=0
        pair=[0,0]
        for col in range(size):
            if buffMatrix[row][col]==1 and count==0:
                if sum(buffMatrix[row])==1:
                    pair[0]=col
                    pair[1]=col
                    count+=2
                    continue
                else:
                    pair[0]=col
                    count+=1
            elif buffMatrix[row][col]==1 and count==1:
                pair[1]=col
                count+=1
        edgesList.append(pair)
    shuffle(edgesList)
    graphFromIncidenceMatrixRead=GraphFromIncidenceMatrix(size)
    for pair in edgesList:
        graphFromIncidenceMatrixRead.insertEdge(pair[0],pair[1])
    timeOfSearchingIncidenceMatrix=[]
    print("Incidence Matrix")
    for pair in edgesList:
        start=perf_counter()
        a=graphFromIncidenceMatrixRead.isEdge(pair[0],pair[1])
        stop=perf_counter()
        if(a):
            print("udało się ", pair)
        else:
            print("nie udało się ",pair)
        timeOfSearchingIncidenceMatrix.append(stop-start)
    fileGraphFromIncidenceMatrixOpen.close()
    # edge list
    fileGraphFromEdgeListOpen = open("fileGraphFromEdgeList.txt","r")
    buffMatrix=fileGraphFromEdgeListOpen.readlines()
    buffMatrix=[i for i in buffMatrix[0].split("\\")]
    buffMatrix.pop(-1)
    buffMatrix=[[i for i in buffMatrix[i].split(" ")]for i in range(int(0.6*edgeNum))]
    buffMatrix=[[int(i) for i in buffMatrix[i]]for i in range(int(0.6*edgeNum))]
    timeOfSearchingEdgeList=[]
    print("Edge list")
    for pair in buffMatrix:
        start=perf_counter()
        a=isEdgeInList(pair,buffMatrix)
        stop=perf_counter()
        if(a):
            print("udało się ", pair)
        else:
            print("nie udało się ",pair)
        timeOfSearchingEdgeList.append(stop-start)
    fileGraphFromEdgeListOpen.close()
    # incidence list
    fileGraphFromIncidenceListOpen = open("fileGraphFromIncidenceList.txt","r")
    buffMatrix=fileGraphFromIncidenceListOpen.readlines()
    buffMatrix=[i for i in buffMatrix[0].split("\\")]
    buffMatrix=[[i for i in buffMatrix[i].split(" ")]for i in range(size)]
    for sublist in buffMatrix:
        sublist.pop(-1)
    try:
        buffMatrix=[[int(i) for i in buffMatrix[i]]for i in range(size)]
    except Exception:
        pass
    timeOfSearchingIncidenceList=[]
    listOfEdgesInIncList=[]
    for i in range(len(buffMatrix)):
        for j in range(len(buffMatrix[i])):
            if buffMatrix[i][j]>=i:
                listOfEdgesInIncList.append([i,buffMatrix[i][j]])
    shuffle(listOfEdgesInIncList)
    print("Incidence list")
    # print(buffMatrix)
    for pair in listOfEdgesInIncList:
        start=perf_counter()
        a=isEdgeInIncList(buffMatrix,pair)
        stop=perf_counter()
        if(a):
            print("udało się ", pair)
        else:
            print("nie udało się ",pair)
        timeOfSearchingIncidenceList.append(stop-start)
    fileGraphFromIncidenceListOpen.close()
    arrayfulltimeAM.append(sum(timeOfSearchingAdjastmentMatrix))
    arrayfulltimeIM.append(sum(timeOfSearchingIncidenceMatrix))
    arrayfulltimeEL.append(sum(timeOfSearchingEdgeList))
    arrayfulltimeIL.append(sum(timeOfSearchingIncidenceList))
    avearrayfulltimeAM.append(sum(timeOfSearchingAdjastmentMatrix)/len(timeOfSearchingAdjastmentMatrix))
    avearrayfulltimeIM.append(sum(timeOfSearchingIncidenceMatrix)/len(timeOfSearchingIncidenceMatrix))
    avearrayfulltimeEL.append(sum(timeOfSearchingEdgeList)/len(timeOfSearchingEdgeList))
    avearrayfulltimeIL.append(sum(timeOfSearchingIncidenceList)/len(timeOfSearchingIncidenceList))

# # generating plots
# def plots(name, x, y):
#     plt.plot(x, y, label=name)
# # plot 1
# plt.rcParams['figure.figsize'] = [15, 5]
# plt.xlabel('Number of elements')
# plt.ylabel('Searching time (in seconds)')
# plt.title("Plot 1 - Sum of times of searching one pair in a given structure")
# plots("Adjacency matrix", num, arrayfulltimeAM)
# plots("Incidence matrix", num, arrayfulltimeIM)
# plots("Edge list", num, arrayfulltimeEL)
# plots("Incidence list", num, arrayfulltimeIL)
# plt.legend(loc="upper left")
# plt.show()
# plt.clf()
# plt.cla()
# plt.close()
# # plot 2
# plt.rcParams['figure.figsize'] = [15, 5]
# plt.xlabel('Number of elements')
# plt.ylabel('Searching time (in seconds)')
# plt.title("Plot 2 - average time of searching one pair in a given structure")
# plots("Adjacency matrix", num, avearrayfulltimeAM)
# plots("Incidence matrix", num, avearrayfulltimeIM)
# plots("Edge list", num, avearrayfulltimeEL)
# plots("Incidence list", num, avearrayfulltimeIL)
# plt.legend(loc="upper left")
# plt.show()
# plt.clf()
# plt.cla()
# plt.close()