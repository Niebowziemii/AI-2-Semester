import numpy as np
import time
from time import perf_counter
import matplotlib
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(200000)
def create_binary_tree(elements,length,largest_el):
    large=largest_el
    left=2*largest_el+1
    right=2*largest_el+2
    if left<length and elements[left]>elements[large]:
        large = left
    if right<length and elements[right]>elements[large]:
        large = right
    if large is not largest_el:
        elements[largest_el],elements[large] = elements[large],elements[largest_el]
        create_binary_tree(elements,length,large)
def heapsort(elements):
    leng=len(elements)
    for i in range(leng//2-1,-1,-1):
        create_binary_tree(elements,leng,i)
    for i in range(leng-1,-1,-1):
        elements[0],elements[i]=elements[i],elements[0]
        create_binary_tree(elements,i,0)
    return elements
def quicksort(elements,start,end):
    if start>=end: return
    mid=elements[(end+start)//2]
    i=start
    j=end
    while i<=j:
        while elements[i]<mid: i+=1
        while elements[j]>mid: j-=1
        if i<=j:
            elements[i], elements[j] = elements[j], elements[i]
            i+=1
            j-=1
    quicksort(elements, start, j)
    quicksort(elements, i, end)
def mergesort(elements):
    if len(elements)>1:
        mid = len(elements)//2
        first = elements[:mid]
        second = elements[mid:]
        mergesort(first)
        mergesort(second)
        #laczenie tablic
        i=0
        j=0
        k=0
        while i<len(first) and j<len(second):
            if first[i]<second[j]:
                elements[k] = first[i]
                i+=1
            else:
                elements[k]=second[j]
                j+=1
            k+=1
        while i<len(first):
            elements[k] = first[i]
            i+=1
            k+=1
        while j<len(second):
            elements[k] = second[j]
            j+=1
            k+=1
def plots_in_1(name, x, y):
    plt.plot(x, y, label=name)
# ZAKOMENTOWANE CZĘŚCI KODU W CELU ZGODNOŚCI Z TESTEM W PLIKU PDF
# numbers = [49999,50000,50001]
# avshapedata = [49999,50000,50001]
numbers=[i for i in range(1000,10000,1000)]
numbers+=[i for i in range(10000,100000,10000)]
numbers+=[i for i in range(100000,1000000,100000)]
avshapedata=[i for i in range(1000,10000,1500)]
for testType in range(6):
    timeheap = []
    timemerge = []
    timequick = []
    for number in numbers:
        if testType is 0:
            randomdatamerge=np.random.normal(250,300,number).round().astype(int)
            randomdataheap=randomdatamerge[:]
            randomdataquick=randomdatamerge[:]

            start=perf_counter()
            heapsort(randomdataheap)
            stop = perf_counter()
            timeheap.append(stop-start)


            start=perf_counter()
            mergesort(randomdatamerge)
            stop = perf_counter()
            timemerge.append(stop - start)

            start=perf_counter()
            quicksort(randomdataquick,0,len(randomdataquick)-1)
            stop = perf_counter()
            timequick.append(stop - start)
        # code for const increasing and decreasing order below
        elif testType is 1:
            constdatamerge=[0for i in range(number)]
            constdataheap=constdatamerge[:]
            constdataquick=constdatamerge[:]

            start = perf_counter()
            heapsort(constdataheap)
            stop = perf_counter()
            timeheap.append(stop - start)

            start = perf_counter()
            mergesort(constdatamerge)
            stop = perf_counter()
            timemerge.append(stop - start)

            start = perf_counter()
            quicksort(constdataquick, 0, len(constdataquick) - 1)
            stop = perf_counter()
            timequick.append(stop - start)
        elif testType is 2:
            increasedatamerge =[i for i in range(number)]
            increasedataheap = increasedatamerge[:]
            increasedataquick = increasedataheap[:]

            start = perf_counter()
            heapsort(increasedataheap)
            stop = perf_counter()
            timeheap.append(stop - start)

            start = perf_counter()
            mergesort(increasedatamerge)
            stop = perf_counter()
            timemerge.append(stop - start)

            start = perf_counter()
            quicksort(increasedataquick, 0, len(increasedataquick) - 1)
            stop = perf_counter()
            timequick.append(stop - start)
        elif testType is 3:
            decreasedatamerge =[i for i in range(number-1,-1,-1)]
            decreasedataheap = decreasedatamerge[:]
            decreasedataquick = decreasedatamerge[:]
            start =perf_counter()
            heapsort(decreasedataheap)
            stop = perf_counter()
            timeheap.append(stop - start)

            start = perf_counter()
            mergesort(decreasedatamerge)
            stop = perf_counter()
            timemerge.append(stop - start)

            start = perf_counter()
            quicksort(decreasedataquick, 0, len(decreasedataquick) - 1)
            stop = perf_counter()
            timequick.append(stop - start)
    for number in avshapedata:
        if testType is 4:
            oddasc = [2*i+1  for i in range(number//2)]
            evendesc =[ 2*i for i in range(number//2-1,-1,-1)]
            odddesc = [2*i+1  for i in range(number//2-1,-1,-1)]
            evenasc =[ 2*i for i in range(number//2)]
            ashapedatamerge=oddasc+evendesc
            ashapedataheap = ashapedatamerge[:]
            ashapedataquick = ashapedataheap[:]
            start =perf_counter()
            heapsort(ashapedataheap)
            stop = perf_counter()
            timeheap.append(stop - start)

            start = perf_counter()
            mergesort(ashapedatamerge)
            stop = perf_counter()
            timemerge.append(stop - start)

            start = perf_counter()
            quicksort(ashapedataquick, 0, len(ashapedataquick) - 1)
            stop = perf_counter()
            timequick.append(stop - start)
        elif testType is 5:
            oddasc = [2*i+1  for i in range(number//2)]
            evendesc =[ 2*i for i in range(number//2-1,-1,-1)]
            odddesc = [2*i+1  for i in range(number//2-1,-1,-1)]
            evenasc =[ 2*i for i in range(number//2)]
            vshapedatamerge=odddesc+evenasc
            vshapedataheap = vshapedatamerge[:]
            vshapedataquick = vshapedataheap[:]

            start =perf_counter()
            heapsort(vshapedataheap)
            stop = perf_counter()
            timeheap.append(stop - start)

            start = perf_counter()
            mergesort(vshapedatamerge)
            stop = perf_counter()
            timemerge.append(stop - start)

            start = perf_counter()
            quicksort(vshapedataquick, 0, len(vshapedataquick) - 1)
            stop = perf_counter()
            timequick.append(stop - start)
    if testType is 0:
        plt.rcParams['figure.figsize'] = [15, 5]
        plt.xlabel('Number of elements')
        plt.ylabel('Sorting Time (in seconds)')
        plt.title("Exercise 2 - Random")
        plots_in_1("quicksort", numbers, timequick)
        plots_in_1("mergesort", numbers, timemerge)
        plots_in_1("heapsort", numbers, timeheap)
        plt.xticks([i for i in range(0,1000000,100000)])
        plt.legend(loc="upper left")
        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
        print(f"quicksort: random {timequick} for [49999,50000,50001]")
    elif testType is 1:
        plt.rcParams['figure.figsize'] = [15, 5]
        plt.xlabel('Number of elements')
        plt.ylabel('Sorting Time (in seconds)')
        plt.title("Exercise 2 - Const")
        plots_in_1("quicksort", numbers, timequick)
        plots_in_1("mergesort", numbers, timemerge)
        plots_in_1("heapsort", numbers, timeheap)
        plt.xticks([i for i in range(0, 1000000, 100000)])
        plt.legend(loc="upper left")
        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
    elif testType is 2:
        plt.rcParams['figure.figsize'] = [15, 5]
        plt.xlabel('Number of elements')
        plt.ylabel('Sorting Time (in seconds)')
        plt.title("Exercise 2 - Increase")
        plots_in_1("quicksort", numbers, timequick)
        plots_in_1("mergesort", numbers, timemerge)
        plots_in_1("heapsort", numbers, timeheap)
        plt.xticks([i for i in range(0, 1000000, 100000)])
        plt.legend(loc="upper left")
        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
    elif testType is 3:
        plt.rcParams['figure.figsize'] = [15, 5]
        plt.xlabel('Number of elements')
        plt.ylabel('Sorting Time (in seconds)')
        plt.title("Exercise 2 - Decrease")
        plots_in_1("quicksort", numbers, timequick)
        plots_in_1("mergesort", numbers, timemerge)
        plots_in_1("heapsort", numbers, timeheap)
        plt.xticks([i for i in range(0, 1000000, 100000)])
        plt.legend(loc="upper left")
        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
    elif testType is 4:
        plt.rcParams['figure.figsize'] = [15, 5]
        plt.xlabel('Number of elements')
        plt.ylabel('Sorting Time (in seconds)')
        plt.title("Exercise 2 - Ashape")
        plots_in_1("quicksort", avshapedata, timequick)
        plots_in_1("mergesort", avshapedata, timemerge)
        plots_in_1("heapsort", avshapedata, timeheap)
        plt.legend(loc="upper left")
        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
        print(f"quicksort: ashape {timequick} for [49999,50000,50001]")
    elif testType is 5:
        plt.rcParams['figure.figsize'] = [15, 5]
        plt.xlabel('Number of elements')
        plt.ylabel('Sorting Time (in seconds)')
        plt.title("Exercise 2 - Vshape")
        plots_in_1("quicksort", avshapedata, timequick)
        plots_in_1("mergesort", avshapedata, timemerge)
        plots_in_1("heapsort", avshapedata, timeheap)
        plt.legend(loc="upper left")
        plt.show()
        plt.clf()
        plt.cla()
        plt.close()
        print(f"quicksort: vshape {timequick} for [49999,50000,50001]")