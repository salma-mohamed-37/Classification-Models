import numpy as np
import pandas as pd
import math

targetColumn = ""

trainData = None
testData = None

yesRecords = None
noRecords = None


class Node:
    def __init__(self, column_name=None, label=None):
        self.column_name = column_name
        self.children = {}  
        self.label = label  

    def is_leaf(self):
        return len(self.children) == 0


def setInputs(train, test,t):
    global trainData, targetColumn, testData
    trainData = train
    targetColumn = t
    testData = test

def divideContinuousColumnsIntoIntervals():
    global trainData, testData
    for column_name, dtype in trainData.dtypes.items():
        if  (dtype == "int64" or dtype == "float64" ) and trainData[column_name].nunique() > 2 :
            trainData[column_name] = pd.cut(trainData[column_name], bins=3)
            testData[column_name] = pd.cut(testData[column_name], bins=3, labels=trainData[column_name].cat.categories)


def prepareTarget(data):
    global targetColumn
    infos = {}
    yesRecords = data[data[targetColumn] == 1]
    noRecords = data[data[targetColumn] == 0]

    for column_name in data.columns:
        if column_name == targetColumn:
            yesProb = float(len(yesRecords)) / len(trainData)
            noProb = float(len(noRecords)) / len(trainData)
            if yesProb == 0:
                info = -(noProb * math.log(noProb, 2))
            elif noProb == 0:
                info = -(yesProb * math.log(yesProb, 2))
            else:
                info = -(yesProb * math.log(yesProb, 2) + noProb * math.log(noProb, 2))

        info = 0
        unique_values = data[column_name].unique()
        for v in unique_values:
            freq = (data[column_name] == v).sum()
            prob = freq / len(data)
            yesProb = (yesRecords[column_name] == v).sum() / freq
            noProb = (noRecords[column_name] == v).sum() / freq
            if yesProb == 0:
                info += prob * -(noProb * math.log(noProb, 2))
            elif noProb == 0:
                info += prob * -(yesProb * math.log(yesProb, 2))
            else:
                info += prob * -(yesProb * math.log(yesProb, 2) + noProb * math.log(noProb, 2))
        infos[column_name] = info
    return infos


def getBestSplit(infos, usedColumns):
    maximumGain = float('-inf')
    bestSplit = ""
    for column, value in infos.items():
        if column == targetColumn or column in usedColumns:
            continue
        gain = infos[targetColumn] - value

        if gain > maximumGain:
            maximumGain = gain
            bestSplit = column

    return bestSplit        


def buildTree(data, usedColumns=None):
    if usedColumns is None:
        usedColumns = []

    infos = prepareTarget(data)
    splitColumn = getBestSplit(infos, usedColumns)

    if not splitColumn:
            majority_label = data[targetColumn].mode().iloc[0]
            return Node(label=majority_label)

    node = Node(column_name=splitColumn)

    usedColumns.append(splitColumn)
    unique_values = data[splitColumn].unique()
    if data[targetColumn].nunique() == 1: 
        majority_label = data[targetColumn].mode().iloc[0]
        return Node(label=majority_label)

    for value in unique_values:
        subset_data = data[data[splitColumn] == value]
        child_node = buildTree(subset_data,usedColumns.copy())
        node.children[value] = child_node
        
    return node


def predictRecord(sample, node):
    if node.is_leaf():
        return node.label
 
    value = sample[node.column_name]
    if value in node.children:
        child_node = node.children[value]
        return predictRecord(sample, child_node)


def testing(root):
    global targetColumn, testData
    testData['Prediction']= -1
    for i ,record in testData.iterrows():
        features = record.drop('Prediction')
        testData.loc[i, 'Prediction'] =predictRecord(features, root)


def calculateAccuracy():
    global testData, targetColumn
    num_equal_records = (testData['Prediction'] == testData[targetColumn]).sum()
    accuracy = float(num_equal_records)/len(testData)
    accuracy = accuracy*100
    return accuracy        


def print_tree(node, indent=0):
    if node is None:
        return

    if node.column_name is not None:
        print("  " * indent + node.column_name)
    if node.label is not None:
        print("  " * indent +str(node.label))

    for value, child_node in node.children.items():
        print("  " * indent + str(value))
        print_tree(child_node, indent + 1)


def decisionTree(train, test,t):
    global testData
    setInputs(train, test,t)
    print("1")
    divideContinuousColumnsIntoIntervals()
    root =  buildTree(trainData)
    print("2")
    testing(root)
    print("3")
    accuracy = calculateAccuracy()
    print("4")
    return testData, accuracy

