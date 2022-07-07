'''
A copy of old functions from the original version
'''

import numpy as np
import pandas as pd

def eig(matrix):
    '''
    Returns leading eigenvalue and eigenvector
    '''
    evals, evectors = np.linalg.eig(matrix)
    norm = np.zeros(len(evals))
    for i in range(len(evals)):
        norm[i] = np.absolute(evals[i])
    index = np.argmax(norm)
    return evals[index], np.real(evectors[:,index])

def sort(A):
    '''
    Sorts teams
    '''
    sortM = np.copy(A)
    sortM = sortM[np.argsort(sortM[:, 1])]
    C = np.zeros_like(sortM)
    for i in range(len(sortM)):
        C[i] = sortM[len(sortM)-i-1]
    return C

def oldprep(df):
    '''Prepares dataframe for use given dataframe and season, returns \
        prepared dataframe'''
    df = df[['HomeTeam', 'AwayTeam','FTHG','FTAG','FTR']]
    df = df.sort_values(by=["HomeTeam", "AwayTeam"], inplace=False)
    df = df.reset_index()
    return df

def method(df):
    '''
    Carries out the ranking/prediction calculations given a dataframe, \
        returns the matrix
    '''

    names = df.HomeTeam.unique()
    teams = len(names)
    played = np.eye(teams)
    entries = len(df)
    results = np.zeros(shape=(teams, teams))
    goals = np.zeros(shape=(teams, teams))
    hg = np.zeros(shape=(teams, teams))
    points = np.zeros(shape=(teams, teams))

    for k in range(entries): # Extracting data from dataframe
        home = df['HomeTeam'][k]
        away = df['AwayTeam'][k]
        homegoals = df['FTHG'][k]
        awaygoals = df['FTAG'][k]
        match = df['FTR'][k]
        index1 = np.argwhere(names == home)[0][0]
        index2 = np.argwhere(names == away)[0][0]
        played[index1,index2] = 1

        if match == 'A':
            results[index1, index2] = 0
        elif match == 'H':
            results[index1, index2] = 3
        elif match == 'D':
            results[index1, index2] = 1

        if homegoals + awaygoals == 0:
            hg[index1, index2] = 0
        else:
            hg[index1, index2] = homegoals / (homegoals + awaygoals)

    for i in range(teams):
        points[i] = results[i]
    for i in range(teams):
        for j in range(teams):
            if i != j:
                if results[j,i] == 0 and played[j,i] == 1:
                    points[i,j] += 3
                elif results[j,i] == 1:
                    points[i,j] += 1

    goals = np.copy(hg)
    for i in range(teams):
        for j in range(teams):
            if (i != j) and played[j,i] == 1:
                goals[i,j] += (1 - hg[j,i])

    A = points + goals

    for i in range(teams):
        for j in range(teams):
            if A[i,j] ==0:
                A[i,j] = 0.01
    return A

def oldranking(csv):
    '''
    Rank teams given a single season csv file, outputs the leading
        eigenvector
    '''

    df = pd.read_csv(csv,encoding = 'unicode_escape')
    df = oldprep(df)
    A = method(df)
    names = df.HomeTeam.unique()
    teams = len(names)


    _, pfv = eig(A)
    if pfv[0] < 0:
        constant = -1
    else:
        constant = 1

    output = np.empty(2*teams, dtype=object)
    for i in range(teams):
        output[2*i] = names[i]
        output[2*i+1] = constant * pfv[i]
    output = output.reshape(teams,2)

    final = sort(output)

    return final
