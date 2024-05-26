import pandas as pd
from sklearn.model_selection import train_test_split
from BayesianClassifier import bayesianClassifier
from DecisionTree import decisionTree

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)


def run (filePath, samplePercentage, testPercentage):
    result = ""
    targetColumn = "diabetes"

    df = pd.read_csv(filePath)

    num_desired_records = int(len(df) * float(samplePercentage) / 100)
    sample = df.sample(n=num_desired_records)

    X = sample.iloc[:, :-1] 
    y = sample.iloc[:, -1] 
    testPercentage = float(testPercentage)/100

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testPercentage, random_state=42)

    trainData = pd.concat([X_train, y_train], axis=1)
    testData = pd.concat([X_test, y_test], axis=1)


    bayesianClassifierResults, bayesianClassifierAccuracy=bayesianClassifier(trainData.copy(), testData.copy(), targetColumn)
    decisionTreeResults, decisionTreeAccuracy= decisionTree(trainData.copy(), testData.copy(), targetColumn)
    bayesianClassifierResults.reset_index(drop=True, inplace=True)
    decisionTreeResults.reset_index(drop=True, inplace=True)

    result+="Bayesian Classifier Accuracy: "+str(bayesianClassifierAccuracy)+" %\nDecision Tree Accuracy: "+str(decisionTreeAccuracy)+" %\n"
    result += "Bayesian Classifier Results\n"+bayesianClassifierResults.to_string()+"\n\nDecision Tree Results \n"+decisionTreeResults.to_string()+"\n\n\n\n"
    return result


