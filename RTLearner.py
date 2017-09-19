import numpy as np
import random


class RTLeaner(object):
    leafsize = 1
    log = False
    btree = None
    global node
    node = []


    def __init__(self, leaf_size, verbose):
        global leafsize
        global log

        leafsize = leaf_size
        log = verbose

    def author(self):
        return 'asharma313'

    def addEvidence(self, dataX, dataY):
        global btree
        global node
        data = np.column_stack((dataX, dataY))
        #dimen = data.shape
        #print data
        #arr = np.array([[1,2,3,2,9], [3,91,4,2,9], [4,2,5,2,9]])
        #check = np.all(arr[:, -1] == arr[0, -1], axis=0)
        #d = arr[arr[:, 2] < 4]
        #e = d[0, -1]
        #print d.shape[0] == 1

        btree = self.build_tree(data)
        btree.pop()
        print ("---- PRINT BTREE ------")
        print (btree)
        print ("---- COMPLETED PRINTING B-TREE ----")
        return "done"

    def build_tree(self, d):
        global leafsize
        global node

        if d.shape[0] == 1:
            leafList = ['leaf', d[0, -1], 'NA', 'NA']
            node.append(leafList)
            return leafList
        if np.all(d[:, -1] == d[0, -1], axis=0):
            leafList = ['leaf', d[0, -1], 'NA', 'NA']
            node.append(leafList)
            return leafList

        else:
            # shaping the tree
            # randomly select feature i
            datacol = d.shape[1]
            randcol = random.randint(0, datacol - 2)

            # randomly select rows to split on
            # randrows = d[np.random.randint(d.shape[0], size=2), :]

            datarow = d.shape[0]
            randrow1 = random.randint(0, datarow - 1)
            randrow2 = random.randint(0, datarow - 1)
            print("ensure not same value")

            # SAME ROW CHECK ensure random rows generated are not of the same value
            while np.all(d[randrow1, randcol] == d[randrow2, randcol], axis=0):
                randrow1 = random.randint(0, datarow - 1)
                randrow2 = random.randint(0, datarow - 1)

            print(randrow1)
            print(randrow2)
            print(np.all(d[randrow1, randcol] == d[randrow2, randcol], axis=0))
            print("ensured")

            # converting splitval from ndarray to integer
            splitval = (d[randrow1, randcol] + d[randrow2, randcol]) / 2
            # print ("splitval: ", splitval[0])
            print (splitval)

            # LEAF SIZE CRITERIA CHECK ensure leaf size check and tree is built according to given leaf size
            if d.shape[0] <= leafsize:
                if leafsize > 1:
                    arr = d[:, -1]
                    meanVal = arr.mean()
                    leafList = ['leaf', meanVal, 'NA', 'NA']
                    node.append(leafList)
                    return leafList
                leafList =['leaf', d[0, -1], 'NA', 'NA']
                node.append(leafList)
                return leafList

            # TIE CHECK
            # if there is a case where data cannot split due to ties, then find two other random values
            # try this up to 10 times
            i = 0
            while (len(d) == len(d[d[:, randcol] <= splitval])) and i < 10:
                i += 1
                randrow1 = random.randint(0, datarow - 1)
                randrow2 = random.randint(0, datarow - 1)

            # if still unsplittable then create a leaf
            if len(d) == len(d[d[:, randcol] <= splitval]):
                #randcol = random.randint(0, datacol - 2)
                arr = d[:, -1]
                meanVal = arr.mean()
                leafList = ['leaf', meanVal, 'NA', 'NA']
                node.append(leafList)
                return leafList

            leftTreeList = d[d[:, randcol] <= splitval]
            rightTreeList = d[d[:, randcol] > splitval]
            resultList = [randcol, splitval, 1, len(leftTreeList) + 1]
            if np.all(d[:, -1] == d[0, -1], axis=0):
                resultList = [randcol, splitval, 1, len(leftTreeList) + 1]
            node.append(resultList)
            leftTree = self.build_tree(leftTreeList)
            rightTree = self.build_tree(rightTreeList)
            rightTreeIndex = (len(leftTree)) + 1
            root = [randcol, splitval, 1, rightTreeIndex]
            print (root)
            print (leftTree)
            print (rightTree)
            return node

    def query(self, dataX):
        yprediction = []
        for row in dataX:
            result = self.traverse_tree(row, 0)
            yprediction.append(result)

        return yprediction

    def traverse_tree(self, d, r):
        global btree
        currNode = btree[r]
        print (currNode)

        if currNode[0] == 'leaf':
            result = currNode[1]
            return result

        compFactor = currNode[0] #compare factor is the random value chosen during creation of tree
        if d[compFactor] <= currNode[1]:
            print(currNode[2])
            r += int(currNode[2])

        if d[compFactor] > currNode[1]:
            r += int(currNode[3])
        return self.traverse_tree(d, r)