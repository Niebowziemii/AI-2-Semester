'''
/*MIT License
Copyright(c) 2020 Rafał Stachowiak
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and /or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from string import ascii_letters
from random import choice
from random import shuffle
from time import perf_counter
from typing import List
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class Node:
    def __init__(self, surname: str = None, name: str = None, indexnum: str = None, next: object = None) -> None:
        self.surname = surname
        self.indexnum = indexnum
        self.name = name
        self.next = next

    def __str__(self) -> str:
        return 'Node[' + "student nr: " + str(self.indexnum) + " name: " + str(self.name) + " surname: " + str(
            self.surname) + ']'


class OrderedList:
    def __init__(self) -> None:
        """
        constructs an empty ordered list
        """
        self.first = None
        self.last = None

    def clear(self):
        self.__init__()

    def insert(self, name: str, surname: str, indexnum: str) -> None:
        """
        inserting data about student
        :param name: name [string]
        :param surname: surname [string]
        :param indexnum: [integer]
        :return:
        """
        if self.first is None:
            self.first = Node(surname, name, indexnum, None)
            self.last = self.first
        elif self.last is self.first:
            if int(self.first.indexnum) < int(indexnum):
                self.last = Node(name, surname, indexnum, None)
                self.first.next = self.last
            else:
                self.last = Node(self.first.name, self.first.surname, self.first.indexnum)
                self.last.next = None
                self.first = Node(name, surname, indexnum, None)
                self.first.next = self.last
        else:
            current = Node(name, surname, indexnum, None)
            parent = self.first
            child = self.first.next
            while int(child.indexnum) < int(indexnum) and child.next is not None:
                child = child.next
                parent = parent.next
            if child is not None and parent is not None and int(child.indexnum) > int(indexnum) and int(
                    parent.indexnum) < int(indexnum):
                parent.next = current
                current.next = child
            elif child.next is None and parent.next is not None and int(child.indexnum) < int(indexnum):
                child.next = current
            elif int(parent.indexnum) > int(current.indexnum):
                current.next = parent
                self.first = current
                print("")

    def __str__(self) -> str:
        """
        print an ordered list
        :return string with list's objects
        """
        if self.first is not None:
            current = self.first
            out = 'OrderedList [\n' + "student nr: " + str(current.indexnum) + " name: \"" + str(
                current.name) + "\" surname: \"" + str(current.surname) + '\"\n'
            while current.next is not None:
                current = current.next
                out += "student nr: " + str(current.indexnum) + " name: \"" + str(
                    current.name) + "\" surname: \"" + str(current.surname) + '\"\n'
            return out + ']'
        return 'OrderedList []'

    def length(self) -> int:
        """
        gives length of the list
        :return: number of elements
        """
        if self.first is not None:
            i = 1
            current = self.first
            while current.next is not None:
                current = current.next
                i = i + 1
            return i
        return 0

    def search(self, indexnum: str, printit: bool = True) -> bool:
        """
        search for the student of a given index number if there is no such student - prints out a message
        :param indexnum: index number of a student we are searching for [integer]
        :param printit: allows for diagnostic print of comments
        :return: print Name and Surname if exist; message if not and returns True or false depending on the result
        """
        flag = False
        if self.length():
            current = self.first
            if current.indexnum is not indexnum:
                while current.next is not None:
                    current = current.next
                    if current.indexnum is indexnum:
                        flag = True
                        if printit:
                            print(
                                "Student of an index number: \"" + str(current.indexnum) + "\" found! \n Name:\"" + str(
                                    current.name) + "\" surname: \"" + str(current.surname) + "\"\n")
                        return flag
            else:
                flag = True
                if printit:
                    print("Student of an index number: \"" + str(current.indexnum) + "\" found! \nName:\"" + str(
                        current.name) + "\" surname: \"" + str(current.surname) + "\"\n")
                return flag
        if not flag:
            if printit:
                print("There is no student in the list that has the index number: \"" + str(indexnum) + "\"")
            return flag
        if not self.length():
            print("The list is empty")

    def remove(self, indexnum: str) -> bool:
        """
        removes a student with a given index number from the list
        :param indexnum: index number [integer]
        :return True if succeeded false if not
        """
        if not self.length():
            print("The list is empty there is nothing to remove!")
            return False
        else:
            if not self.search(indexnum, False):
                print("In this list a student with given index number does not exist!")
                return False
            else:
                current = self.first
                if current.indexnum is indexnum:
                    if current.next is not None:
                        self.first = current.next
                    else:
                        self.first = None
                    return True
                while current.next is not None:
                    if current.next.indexnum is indexnum:
                        newNext = current.next.next
                        if newNext is not None:
                            current.next = newNext
                        else:
                            current.next = None
                        return True
                    else:
                        current = current.next
                return False


class BSTNode:

    def __init__(self, surname: str = None, name: str = None, indexnum: str = None) -> None:
        self.surname = surname
        self.name = name
        self.indexnum = indexnum
        self.right = None
        self.left = None

    def __str__(self) -> str:
        return 'Node[' + "student nr: " + str(self.indexnum) + " name: " + str(self.name) + " surname: " + str(
            self.surname) + "] On the left: " + str(self.left) + " on the right: " + str(self.right)


class BinaryTree:
    def __init__(self, root: object = None) -> None:
        self.root = root

    def __str__(self):
        return str(self.root)

    def clear(self):
        self.__init__()

    def insert(self, node: object, surname: str = None, name: str = None, indexnum: str = None) -> None:
        if node is not None:
            if int(indexnum) < int(node.indexnum):
                if node.left is None:
                    node.left = BSTNode(surname, name, indexnum)
                else:
                    self.insert(node.left, surname, name, indexnum)
            else:
                if node.right is None:
                    node.right = BSTNode(surname, name, indexnum)
                else:
                    self.insert(node.right, surname, name, indexnum)
        else:
            self.root = BSTNode(surname, name, indexnum)

    def search(self, node, indexnum: str, flag) -> object:
        if node is None:
            if flag:
                print("There is no student in the tree with an index number: \"", indexnum, "\"")
            return None
        elif indexnum is node.indexnum:
            if flag:
                print("Student with index number: ", indexnum, " found! \n Name: ", node.name, " Surname: ",
                      node.surname, " .")
            return node
        elif int(indexnum) < int(node.indexnum):
            return self.search(node.left, indexnum, flag)
        else:
            return self.search(node.right, indexnum, flag)

    def searchbg(self, node, indexnum, flagg):
        if not flagg:
            return self.search(node, indexnum, False)
        else:
            return self.search(node, indexnum, True)

    def searchParent(self, indexnum):
        current = self.root
        parent = None
        while current is not None and current.indexnum is not indexnum:
            parent = current
            if int(indexnum) < int(current.indexnum):
                current = current.left
            else:
                current = current.right
        return parent

    def minimumIndexInSubTree(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def remove(self, root, indexnum):
        parent = None
        current = self.searchbg(root, indexnum, False)
        parent = self.searchParent(indexnum)
        if current is None:
            return "Student with index number: \"" + str(indexnum) + "\" does not exist in the tree"
        # there is no children
        if current.right is None and current.left is None:
            if current is not root:
                if parent.left is current:
                    parent.left = None
                else:
                    parent.right = None
            else:
                self.root = None
        elif current.left is not None and current.right is not None:
            successor = self.minimumIndexInSubTree(current.right)
            bufferi, buffern, buffers = successor.indexnum, successor.name, successor.surname
            self.remove(root, successor.indexnum)
            current.indexnum, current.name, current.surname = bufferi, buffern, buffers
        else:
            child = current.left if current.left is not None else current.right
            if current is not root:
                if current is parent.left:
                    parent.left = child
                else:
                    parent.right = child
            else:
                self.root = child

    def inorderPrint(self, node):
        if node is not None:
            self.inorderPrint(node.left)
            print("Student nr: \"" + str(node.indexnum) + "\" name: \"" + str(node.name) + "\" surname: \"" + str(
                node.surname) + "\"")
            self.inorderPrint(node.right)
    def preorderPrint(self, node):
        if node is not None:
            print("Student nr: \"" + str(node.indexnum) + "\" name: \"" + str(node.name) + "\" surname: \"" + str(
                node.surname) + "\"")
            self.preorderPrint(node.left)
            self.preorderPrint(node.right)
    def postorderPrint(self, node):
        if node is not None:
            self.preorderPrint(node.left)
            self.preorderPrint(node.right)
            print("Student nr: \"" + str(node.indexnum) + "\" name: \"" + str(node.name) + "\" surname: \"" + str(
                node.surname) + "\"")
    def reverseOrder(self,node):
        if node is not None:
            self.preorderPrint(node.right)
            print("Student nr: \"" + str(node.indexnum) + "\" name: \"" + str(node.name) + "\" surname: \"" + str(
                node.surname) + "\"")
            self.preorderPrint(node.left)
    def printEverythingSafelyIfIsEmpty(self, flag: int = 1) -> None:
        if self.root is None:
            print("The Tree is empty")
        elif flag is 1:
            self.inorderPrint(self.root)

    def storeNodes(self, root, nodes):
        if not root:
            return
        self.storeNodes(root.left, nodes)
        nodes.append(root)
        self.storeNodes(root.right, nodes)

    def buildTreeNow(self, nodes, start, end):
        if start > end:
            return None
        mid = (start + end) // 2
        node = nodes[mid]
        node.left = self.buildTreeNow(nodes, start, mid - 1)
        node.right = self.buildTreeNow(nodes, mid + 1, end)
        return node

    def buildBalancedTree(self, root):
        nodes = []
        self.storeNodes(root, nodes)
        n = len(nodes)
        self.root = self.buildTreeNow(nodes, 0, n - 1)

# kod do testów poniżej

# binary = BinaryTree()
# binary.insert(binary.root,"Rwnsjedinsar","Asssskskydws",4)
# binary.insert(binary.root,"Kwbsrjdogsaw","Dejdkantskre" ,7)
# binary.insert(binary.root,"Swifnesarksw","Pnhatdeoicnq" ,1)
# binary.insert(binary.root,"Cwjdernswero","Iaserjddswut" ,5)
# binary.insert(binary.root,"Swdbwiednawe","Aqwevytskdyt" ,2)
# binary.insert(binary.root,"Swropdcufsaz","Ldarwncdrisa" ,9)
# binary.insert(binary.root,"Swertpflsawr","Usfrwjdloers" ,3)
# binary.insert(binary.root,"Jwrdlaserods","Jhserpdawerl" ,10)
# binary.insert(binary.root,"Baaserdokews","Mnstarwjcdri" ,6)
# binary.insert(binary.root,"Qzserfsiogaw","Msderlfdswie" ,8)
# binary.insert(binary.root,"Msraskermsqa","Haserodxcswt"  ,11)
#
# print(binary.root)
# binary.inorderPrint(binary.root)
# print()
# binary.preorderPrint(binary.root)
# print()
# binary.postorderPrint(binary.root)
# print()
#
#
# print("AFTER BALANCING")
# binary.buildBalancedTree(binary.root)
# print(binary.root)
# binary.inorderPrint(binary.root)
# print()
# binary.preorderPrint(binary.root)
# print()
# binary.postorderPrint(binary.root)
# print()



# FILE GENERATOR AND ORDERED LIST DRIVER CODE

n: List[int] = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                10000, 25000, 50000, 75000, 100000]
# ordered list

aveTimeInsertOL = []
aveTimeSearchOL = []
aveTimeRemoveOL = []
aveTimeInsertBT = []
aveTimeSearchBT = []
aveTimeSearchBBT = []
aveTimeRemoveBT = []
timeOfInsertingBinaryTree = []
timeOfRemovingBinaryTree = []
timeOfSearchingBinaryTreeInOrder = []
timeOfSearchingBalancedBinaryTreeInOrder = []
timeOfInsertingOrderedList = []
timeOfRemovingOrderedList = []
timeOfSearchingOrderedList = []
sumtimeOfInsertingBinaryTree = []
sumtimeOfRemovingBinaryTree = []
sumtimeOfSearchingBinaryTreeInOrder = []
sumtimeOfSearchingBalancedBinaryTreeInOrder = []
sumtimeOfInsertingOrderedList = []
sumtimeOfRemovingOrderedList = []
sumtimeOfSearchingOrderedList = []
for num in n:
    file = open("danelist.txt", "w")
    for i in range(num):
        file.write(
            "naz" + str(choice(ascii_letters) * 12) + ',' + str(choice(ascii_letters) * 12) + ',' + str(i + 1) + '\n')
    file.close()
    file = open("danelist.txt", "r")
    a = OrderedList()
    content = file.readlines()
    content = [x.split(',') for x in content]
    content = [[x[0], x[1], x[2].strip()] for x in content]
    listOfKeys = [x[2] for x in content]
    shuffle(content)
    shuffle(listOfKeys)
    # inserting elements from file
    print(a)
    for sublist in content:
        start = perf_counter()
        a.insert(sublist[0], sublist[1], sublist[2])
        stop = perf_counter()
        print("added", sublist)
        timeOfInsertingOrderedList.append(stop - start)
    sumtimeOfInsertingOrderedList.append(sum(timeOfInsertingOrderedList))
    aveTimeInsertOL.append(sum(timeOfInsertingOrderedList) / len(timeOfInsertingOrderedList))
    print(a, '\n')
    # searching elements
    shuffle(listOfKeys)
    for key in listOfKeys:
        start = perf_counter()
        a.search(key)
        stop = perf_counter()
        timeOfSearchingOrderedList.append(stop - start)
    sumtimeOfSearchingOrderedList.append(sum(timeOfSearchingOrderedList))
    aveTimeSearchOL.append(sum(timeOfSearchingOrderedList) / len(timeOfSearchingOrderedList))
    # removing elements from list
    for key in listOfKeys:
        start = perf_counter()
        a.remove(key)
        stop = perf_counter()
        print("removing", key)
        timeOfRemovingOrderedList.append(stop - start)
    sumtimeOfRemovingOrderedList.append(sum(timeOfRemovingOrderedList))
    aveTimeRemoveOL.append(sum(timeOfRemovingOrderedList) / len(timeOfRemovingOrderedList))
    print(a)
    file.close()

    # BINARY SEARCH TREE DRIVER CODE

    # for num in n:
    file = open("danedrzewo.txt", "w")
    for i in range(num):
        file.write(
            "naz" + str(choice(ascii_letters) * 12) + ',' + str(choice(ascii_letters) * 12) + ',' + str(i + 1) + '\n')
    file.close()
    file = open("danedrzewo.txt", "r")
    b = BinaryTree()
    content = file.readlines()
    content = [x.split(',') for x in content]
    content = [[x[0], x[1], x[2].strip()] for x in content]
    listOfKeys = [x[2] for x in content]
    shuffle(content)
    shuffle(listOfKeys)
    # inserting elements from file
    print(b)
    for sublist in content:
        start = perf_counter()
        b.insert(b.root, sublist[0], sublist[1], sublist[2])
        stop = perf_counter()
        print("added", sublist)
        timeOfInsertingBinaryTree.append(stop - start)
    sumtimeOfInsertingBinaryTree.append(sum(timeOfInsertingBinaryTree))
    aveTimeInsertBT.append(sum(timeOfInsertingBinaryTree) / len(timeOfInsertingBinaryTree))
    b.printEverythingSafelyIfIsEmpty(1)
    # searching elements in ordinary binary tree
    shuffle(listOfKeys)
    for key in listOfKeys:
        start = perf_counter()
        b.searchbg(b.root, key, True)
        stop = perf_counter()
        timeOfSearchingBinaryTreeInOrder.append(stop - start)
    sumtimeOfSearchingBinaryTreeInOrder.append(sum(timeOfSearchingBinaryTreeInOrder))
    aveTimeSearchBT.append(sum(timeOfSearchingBinaryTreeInOrder) / len(timeOfSearchingBinaryTreeInOrder))
    # creating a balanced binary search tree
    c = BinaryTree()
    c.buildBalancedTree(b.root)
    # searching elements in balanced tree
    shuffle(listOfKeys)
    for key in listOfKeys:
        start = perf_counter()
        c.searchbg(c.root, key, True)
        stop = perf_counter()
        timeOfSearchingBalancedBinaryTreeInOrder.append(stop - start)
    sumtimeOfSearchingBalancedBinaryTreeInOrder.append(sum(timeOfSearchingBalancedBinaryTreeInOrder))
    aveTimeSearchBBT.append(
        sum(timeOfSearchingBalancedBinaryTreeInOrder) / len(timeOfSearchingBalancedBinaryTreeInOrder))
    # removing elements from list
    for key in listOfKeys:
        start = perf_counter()
        b.remove(b.root, key)
        stop = perf_counter()
        print("removing", key)
        timeOfRemovingBinaryTree.append(stop - start)
    sumtimeOfRemovingBinaryTree.append(sum(timeOfRemovingBinaryTree))
    aveTimeRemoveBT.append(sum(timeOfRemovingBinaryTree) / len(timeOfRemovingBinaryTree))
    b.printEverythingSafelyIfIsEmpty(1)
    file.close()


# GENERATING PLOTS

def plots(name, x, y):
    plt.plot(x, y, label=name)


# plot 1
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title("Plot 1 - Average time needed to insert one element in Ordered List and Binary Search Tree")
plots("Ordered List", n, aveTimeInsertOL)
plots("Binary Search Tree", n, aveTimeInsertBT)
plt.xticks()
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()

# plot 2
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title(
    "Plot 2 - Average time needed to search one element in Ordered List, Binary Search Tree and Balanced Binary Search Tree")
plots("Ordered List", n, aveTimeSearchOL)
plots("Binary Search Tree", n, aveTimeSearchBT)
plots("Balanced Binary Search Tree", n, aveTimeSearchBBT)
plt.xticks()
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()

# plot 3
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title("Plot 3 - Average time needed to remove one element in Ordered List and Binary Search Tree ")
plots("Ordered List", n, aveTimeRemoveOL)
plots("Binary Search Tree", n, aveTimeRemoveBT)
plt.xticks()
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()

# plot 4
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title("Plot 4 - Time needed to insert all elements in Ordered List and Binary Search Tree")
plots("Ordered List", n, sumtimeOfInsertingOrderedList)
plots("Binary Search Tree", n, sumtimeOfInsertingBinaryTree)
plt.xticks()
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()

# plot 5
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title(
    "Plot 5 - Time needed to search all elements in Ordered List, Binary Search Tree and Balanced Binary Search Tree")
plots("Ordered List", n, sumtimeOfSearchingOrderedList)
plots("Binary Search Tree", n, sumtimeOfSearchingBinaryTreeInOrder)
plots("Balanced Binary Search Tree", n, sumtimeOfSearchingBalancedBinaryTreeInOrder)
plt.xticks()
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()

# plot 6
plt.rcParams['figure.figsize'] = [15, 5]
plt.xlabel('Number of elements')
plt.ylabel('Sorting Time (in seconds)')
plt.title("Plot 6 - Time needed to remove all elements in Ordered List and Binary Search Tree")
plots("Ordered List", n, sumtimeOfRemovingOrderedList)
plots("Binary Search Tree", n, sumtimeOfRemovingBinaryTree)
plt.xticks()
plt.legend(loc="upper left")
plt.show()
plt.clf()
plt.cla()
plt.close()

# GENERATING TABLES

aveTimeSearchOL = [round(i, 16) for i in aveTimeSearchOL]
aveTimeSearchBT = [round(i, 16) for i in aveTimeSearchBT]
aveTimeSearchBBT = [round(i, 16) for i in aveTimeSearchBBT]
aveTimeInsertBT = [round(i, 16) for i in aveTimeInsertBT]
aveTimeInsertOL = [round(i, 16) for i in aveTimeInsertOL]
aveTimeRemoveBT = [round(i, 16) for i in aveTimeRemoveBT]
aveTimeRemoveOL = [round(i, 16) for i in aveTimeRemoveOL]
sumtimeOfInsertingOrderedList = [round(i, 16) for i in sumtimeOfInsertingOrderedList]
sumtimeOfInsertingBinaryTree = [round(i, 16) for i in sumtimeOfInsertingBinaryTree]
sumtimeOfSearchingOrderedList = [round(i, 16) for i in sumtimeOfSearchingOrderedList]
sumtimeOfSearchingBinaryTreeInOrder = [round(i, 16) for i in sumtimeOfSearchingBinaryTreeInOrder]
sumtimeOfSearchingBalancedBinaryTreeInOrder = [round(i, 16) for i in sumtimeOfSearchingBalancedBinaryTreeInOrder]
sumtimeOfRemovingOrderedList = [round(i, 16) for i in sumtimeOfRemovingOrderedList]
sumtimeOfRemovingBinaryTree = [round(i, 16) for i in sumtimeOfRemovingBinaryTree]
headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

# table 1
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['NUMBER OF ELEMENTS', 'Ordered List', 'Binary Search Tree'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            [i for i in n],
            aveTimeInsertOL,
            aveTimeInsertBT],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor] * len(n)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=10)
    ))
])
fig.update_layout(
    title={
        'text': "Table 1 - Average time of inserting <br> one element in n-element Ordered List and Binary Search Tree",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()

# table 2
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['NUMBER OF ELEMENTS', 'Ordered List', 'Binary Search Tree', 'Balanced Binary Search Tree'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            [i for i in n],
            aveTimeSearchOL,
            aveTimeSearchBT,
            aveTimeSearchBBT],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor] * len(n)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=11)
    ))
])
fig.update_layout(
    title={
        'text': "Table 2 - Average time of searching one element<br>in n-element Ordered List, Binary Search Tree and Balanced Binary Search Tree",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()

# table 3
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['NUMBER OF ELEMENTS', 'Ordered List', 'Binary Search Tree'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            [i for i in n],
            aveTimeRemoveOL,
            aveTimeRemoveBT],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor] * len(n)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=11)
    ))
])
fig.update_layout(
    title={
        'text': "Table 3 - Average time of removing one element<br>in n-element Ordered List and Binary Search Tree",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()

# table 4
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['NUMBER OF ELEMENTS', 'Ordered List', 'Binary Search Tree'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            [i for i in n],
            sumtimeOfInsertingOrderedList,
            sumtimeOfInsertingBinaryTree],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor] * len(n)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=11)
    ))
])
fig.update_layout(
    title={
        'text': "Table 4 - Time of inserting all elements<br>in n-element Ordered List and Binary Search Tree",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()

# table 5
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['NUMBER OF ELEMENTS', 'Ordered List', 'Binary Search Tree', 'Balanced Binary Search Tree'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            [i for i in n],
            sumtimeOfSearchingOrderedList,
            sumtimeOfSearchingBinaryTreeInOrder,
            sumtimeOfSearchingBalancedBinaryTreeInOrder],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor] * len(n)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=11)
    ))
])
fig.update_layout(
    title={
        'text': "Table 5 - Time of searching all elements in n-element <br> Ordered List, Binary Search Tree and Balanced Binary Search Tree",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()

# table 6
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['NUMBER OF ELEMENTS', 'Ordered List', 'Binary Search Tree'],
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            [i for i in n],
            sumtimeOfRemovingOrderedList,
            sumtimeOfRemovingBinaryTree],
        line_color='darkslategray',
        # 2-D list of colors for alternating rows
        fill_color=[[rowOddColor, rowEvenColor] * len(n)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=11)
    ))
])
fig.update_layout(
    title={
        'text': "Table 6 - Time of removing all elements<br>in n-element Ordered List and Binary Search Tree",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()