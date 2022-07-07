'''
Error calculations

First calculate actual table given csv of results for season, then compare
the difference in positions for the teams, then apply for various points of the
season.
'''

import numpy as np
import pandas as pd
from old import sort
from old import oldranking as oldr

def actual(df):
    '''
    Given a dataframe for one season, returns the final table.
    '''
    df = df[['HomeTeam', 'AwayTeam','FTR']]
    names = df.HomeTeam.unique()
    teams = len(names)
    entries = len(df)

    output = np.empty(2*teams, dtype=object)
    for i in range(teams):
        output[2*i] = names[i]
        output[2*i+1] = 0
    output = output.reshape(teams,2)

    for i in range(entries):
        match = df['FTR'][i]
        hIndex = np.where(names == df['HomeTeam'][i])
        aIndex = np.where(names == df['AwayTeam'][i])
        if match == 'H':
            output[hIndex,1] += 3
        elif match == 'A':
            output[aIndex,1] += 3
        elif match == 'D':
            output[hIndex,1] += 1
            output[aIndex,1] += 1
    output = sort(output)
    return output

def oneStepError(table, prediction):
    '''
    Given two sorted scoring vectors not including scores, calculates the
    difference in positions between them.
    '''
    error = 0
    for i in range(len(table)):
        j = np.where(prediction == table[i])[0][0]
        error += np.abs(i-j)
    return error

'''
For the input for the next function, predictions is a grid of the names, where
each column is a prediction, and the row is its place in the prediction (top is
highest). Do not include the scores. Order the columns in date order, with the
oldest on the left and the newest on the right
'''
def multipleStepError(table, predictions):
    '''
    Calculates the error at each prediction stage and sums it, with weighting
    '''
    table = table[:,0]
    _, n = predictions.shape
    errorArray = np.zeros(n)
    weightsArray = np.zeros(n)
    for i in range(n):
        weightsArray[i] = 10 * np.tanh((6*i) / (n-1) -3) + 1.5 
        - 10 * np.tanh(-3)
        errorArray[i] = oneStepError(table,predictions[:,i])
    return np.dot(weightsArray, errorArray)


'''
df22 = pd.read_csv("2022.csv")
table22 = actual(df22)
print(table22)
oldRanking = oldr("2022.csv")
print(oldRanking)
finalError = oneStepError(table22[:,0],oldRanking[:,0])
print(finalError)
'''
