from random import randint
from itertools import product
from time import perf_counter
import matplotlib.pyplot as plt
def bruteForce(weights,costs,elementNum,size):
    products = ["".join(seq) for seq in product("01", repeat = elementNum)]
    vectors = [[int(i) for i in list(subproduct)] for subproduct in products]
    results=[[0,0] for _ in vectors]
    for indexVec,vector in enumerate(vectors):
        for indexNum, number in enumerate(vector):
            if number:
                results[indexVec][0]+=weights[indexNum]
                results[indexVec][1]+=costs[indexNum]
        if results[indexVec][0]>size:
            results[indexVec][0]=results[indexVec][1]=0
    # print(vectors,'\n',results)
    # print(vectors[results.index(max(results,key = lambda x: x[1]))],results.index(max(results,key = lambda x: x[1])),max(results,key = lambda x: x[1]))
    return vectors[results.index(max(results,key = lambda x: x[1]))]

def dynamicSolution(size,elementNum,weights,costs):
    weights=[0]+weights
    costs=[0]+costs
    matrix=[[0 for i in range(size+1)]for i in range(elementNum+1)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i==0 or j==0:
                continue
            elif weights[i]>j:
                matrix[i][j]=matrix[i-1][j]
            elif weights[i]<=j:
                matrix[i][j]=max(matrix[i-1][j],costs[i]+matrix[i-1][j-weights[i]])
    solutionIndexes=[]
    for col in matrix:
        print(col)
    optimalVal=matrix[-1][-1]
    col=size
    row=elementNum
    while optimalVal:
        if matrix[row-1][col]==optimalVal:
            row -= 1
            continue
        else:
            solutionIndexes.append(row)
            optimalVal -= costs[row]
            col-=weights[row]
            row -= 1

    solutionIndexes=[i-1 for i in solutionIndexes]
    result = [0 if i not in solutionIndexes else 1 for i in range(len(weights)-1)]
    # print("inside the function",result,solutionIndexes)
    return result

def greedyWay(weights,costs,size):
    indexes = [i for i in range(len(weights))]
    ratio = [costs[i]/weights[i] for i in  range(len(weights))]
    triples = list(zip(weights,costs,indexes,ratio))
    buffer=[]
    result = [0 for _ in range(len(weights))]
    triplesSorted = sorted(triples,key= lambda x: x[3], reverse=True)
    # print(triplesSorted)
    for triple in triplesSorted:
        if triple[0]<=size:
            buffer.append(triple)
            size-=triple[0]
            result[buffer[-1][2]]+=1
    return result

sizes = [5,10,15,20,25] # pojemność plecaka
elementNums = [5,10,15,20,25] # ilość wygenerowanych elementów
timeBruteForce = []
timeDynamic = []
timeGreedy = []
for (elementNum,size) in zip(elementNums,sizes):
    weights = [randint(1,size) for i in range(1,elementNum+1,1)] # wagi poszczególnych przedmiotów
    costs = [randint(1,elementNum) for _ in range(elementNum)] # wartość poszczególnych przedmiotów
    # weights=[5,3,1,5,2,14]
    # costs = [3,2,6,2,17,32]
    print(f"weights: {weights}, costs: {costs}\n")

    start = perf_counter()
    solution = bruteForce(weights,costs,elementNum,size)
    stop = perf_counter()
    values=[weights[i] if solution[i] else 0 for i in range(len(weights))]
    print(f"BruteForce solution: {solution}, values sum: {sum(values)}\n")
    timeBruteForce.append(stop-start)

    start = perf_counter()
    solution = dynamicSolution(size,elementNum,weights,costs)
    stop = perf_counter()
    values = [weights[i] if solution[i] else 0 for i in range(len(weights))]
    print(f"Dynamic programming solution: {solution}, values sum: {sum(values)}\n")
    timeDynamic.append(stop - start)

    start = perf_counter()
    solution = greedyWay(weights, costs, size)
    stop = perf_counter()
    values = [weights[i] if solution[i] else 0 for i in range(len(weights))]
    print(f"Greedy way solution: {solution}, values sum: {sum(values)}\n")
    timeGreedy.append(stop - start)

#generating plots
def plots(name, x, y):
    plt.plot(x, y, label=name)
# plot 1
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Searching time (in seconds)')
plt.title("Plot 1 - time of solving knapsack problem of size n")
plots("Brute Force", sizes, timeBruteForce)
plots("Dynamic Programming", sizes,timeDynamic)
plots("Greedy way", sizes, timeGreedy)
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()