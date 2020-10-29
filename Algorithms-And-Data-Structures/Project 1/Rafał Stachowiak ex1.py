import time
from time import perf_counter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
def bubble(tab):
    n = len(tab)
    for i in range(n):
        for j in range(0, n-i-1):
            if tab[j]>tab[j+1]:
                tab[j],tab[j+1] = tab[j+1],tab[j]
    return tab
def count(elements,maximum):
    wynik = [0 for i in range(len(elements))]
    counter = [0 for i in range(maximum+1)]
    for element in elements:
        counter[element]+=1
    for i in range(1,len(counter)):
        counter[i] +=counter[i-1]
    for i in range(len(elements)):
        wynik[counter[elements[i]]-1] = elements[i]
        counter[elements[i]]-=1
    return wynik
def shell(elements):
    n=len(elements)
    i=0
    hole=0
    while hole<n:
        hole = 2**i+1
        i+=1
    i-=2
    hole = (2**i+1)
    while hole>0:
        for k in range(hole,n):
            temp=elements[k]
            j=k
            while j>hole-1 and elements[j-hole]>=temp:
                elements[j]=elements[j-hole]
                j=j-hole
            elements[j]=temp
        if i>0:
            i-=1
            hole = 2**i+1
        elif i==0:
            hole=1
            i-=1
        else:
            hole=0
    return elements
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

nuber_of_el=[i for i in range(100,1000,100)]
nuber_of_el_bubble=[i for i in range(100,1000,100)]
nuber_of_el_bubble+=[1000,2000,3000,4000,5000]
nuber_of_el+=[i for i in range(1000,10000,1000)]
nuber_of_el+=[i for i in range(10000,100001,10000)]
bubbletime=[]
shelltime=[]
heaptime=[]
counttime=[]
for number in nuber_of_el:
    bubbledata=np.random.normal(250,300,number).round().astype(int)
    countingdata=bubbledata[:]
    shelldata=bubbledata[:]
    heapdata=bubbledata[:]
    if number<5001:
        start=perf_counter()
        resultbubble=bubble(bubbledata)
        stop=perf_counter()
        bubbletime.append(stop-start)

    start=perf_counter()
    resultshell=shell(shelldata)
    stop=perf_counter()
    shelltime.append(stop-start)

    start=perf_counter()
    resultheap=heapsort(heapdata)
    stop=perf_counter()
    heaptime.append(stop-start)

    #to allow counting sort handle negative numbers we need to shift all elements to the right to make place for negative numbers
    low=min(countingdata)
    countingdata=[e-low for e in countingdata]
    start=perf_counter()
    result=count(countingdata,max(countingdata))
    stop=perf_counter()
    counttime.append(stop-start)
    result = [e+low for e in result]

def plots_in_1(name, x, y):
    plt.plot(x, y, label=name)



plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title("Task 1 - comparison bubblesort,countingsort,shellsort,heapsort")
plots_in_1("shellsort",nuber_of_el,shelltime)
plots_in_1("countingsort",nuber_of_el,counttime)
plots_in_1("bubblesort",nuber_of_el_bubble,bubbletime)
plots_in_1("heapsort",nuber_of_el,heaptime)
plt.xlim(1, 100000)
plt.xticks([i for i in range(0,90001,10000)])
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()
# print(result)
