import pandas as pd
from sklearn.model_selection import train_test_split
targetColumn = ""

trainData = None
testData = None

yesRecords = None
noRecords = None

targetProbabilities = {}

givenYes = {}
givenNo ={}


def setInputs(train, test, t):
    global targetColumn, trainData, testData
    targetColumn = t
    trainData = train
    testData = test

def calculateProbabilities():
    global yesRecords, noRecords, targetColumn, trainData, targetProbabilities
    yesRecords = trainData[trainData[targetColumn] == 1]
    yesRecords =  yesRecords.iloc[:, :-1]
    noRecords = trainData[trainData[targetColumn] == 0]
    noRecords = noRecords.iloc[:, :-1]

    targetProbabilities[1] = len(yesRecords)/len(trainData)
    targetProbabilities[0] = len(noRecords)/len(trainData)

    for column_name, dtype in yesRecords.dtypes.items():
        uniqueValues = yesRecords[column_name].unique()
        for v in uniqueValues:
            givenYes[column_name+","+str(v)] = (yesRecords[column_name].value_counts()[v])/len(yesRecords)   

    for column_name, dtype in noRecords.dtypes.items():
        uniqueValues = noRecords[column_name].unique()
        for v in uniqueValues:
            givenNo[column_name+","+str(v)] = (noRecords[column_name].value_counts()[v])/len(noRecords)

      
def testing():
    global testData, targetProbabilities, givenYes, givenNo
    result ={}
    testData['Prediction'] = None
    
    for index, record in testData.iterrows():
        yesValue = targetProbabilities[1]
        noValue =  targetProbabilities[0]

        for column_name in testData.columns:
            try:
                yesValue *= givenYes[column_name+","+str(record[column_name])]
                noValue *= givenNo[column_name+","+str(record[column_name])] 
            except:
                pass
                
        if yesValue > noValue:
             testData.loc[index, 'Prediction'] = 1
        elif yesValue < noValue:    
             testData.loc[index, 'Prediction'] = 0
           

def calculateAccuracy():
    global testData, targetColumn
    num_equal_records = (testData['Prediction'] == testData[targetColumn]).sum()
    accuracy = float(num_equal_records)/len(testData)
    accuracy = accuracy*100
    return accuracy        


def bayesianClassifier(train, test, t):
    global testData
    setInputs(train, test, t)
    calculateProbabilities()
    testing()
    accuracy = calculateAccuracy()
    return testData, accuracy
    