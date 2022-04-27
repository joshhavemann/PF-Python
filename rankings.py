'''
Premier League ranking generator for essay
'''
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

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
    B = np.copy(A)
    B = B[np.argsort(B[:, 1])]
    C = np.zeros_like(B)
    for i in range(len(B)):
        C[i] = B[len(B)-i-1]
    return C

def scalehome(x):
    ''' Scale if away game played already, scaling for home'''
    minval = 1.5
    maxval = 7.5
    scale = 2.11

    if 0 <= x <= minval / scale:
        return minval
    elif minval / scale < x < maxval / scale:
        return x * scale
    elif maxval / scale <= x <= 4:
        return maxval
    else:
        print("error in scalehome!")
        return -1

def scaleaway(x):
    ''' Scale if home game played already, scaling for away'''
    minval = 1
    maxval = 7
    scale = 1 + (1 / 1.11)

    if 0 <= x <= minval / scale:
        return minval
    elif minval / scale < x < maxval / scale:
        return x * scale
    elif maxval / scale <= x <= 4:
        return maxval
    else:
        print("error in scaleaway!")
        return -1

def prep(df,season):
    '''Prepares dataframe for use given dataframe and season, returns \
        prepared dataframe'''
    df = df[['Season','HomeTeam', 'AwayTeam','FTHG','FTAG','FTR']]
    df = df.loc[df['Season'] == season]
    df = df.sort_values(by=["HomeTeam", "AwayTeam"], inplace=False)
    df = df.reset_index()
    return df

def prep_pred(df):
    '''Prepares dataframe for use '''
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
            if played[i,j] == 0:
                if played[j,i] == 0:
                    A[i,j] == B[i,j] #change to last seasons
                    A[j,i] == B[j,i] #change to last seasons

                else:
                    A[i,j] = scalehome(A[i,j])
                    A[j,i] = scaleaway(A[j,i])
                played[i,j] == 1
                played[j,i] == 1

    for i in range(teams):
        for j in range(teams):
            if A[i,j] ==0:
                A[i,j] = 0.01
    return A

def ranking(csv, season):
    '''
    Rank teams given a csv file and the season to use, outputs the leading
        eigenvector and the matrix
    '''

    df = pd.read_csv(csv,encoding = 'unicode_escape')
    df = prep(df, season)
    A = method(df)
    names = df.HomeTeam.unique()
    teams = len(names)


    _, pfv = eig(A)

    output = np.empty(2*teams, dtype=object)
    for i in range(teams):
        output[2*i] = names[i]
        output[2*i+1] = pfv[i]
    output = output.reshape(teams,2)

    final = sort(output)

    return final, A

def prediction(url):
    '''
    Predict rankings given a csv file and the season to use, outputs the
        leading eigenvector and the matrix
    '''
    df = pd.read_csv(url)
    df = prep_pred(df)
    A = method(df)
    names = df.HomeTeam.unique()
    teams = len(names)

    _, pfv = eig(A)

    output = np.empty(2*teams, dtype=object)
    if pfv[0] < 0:
        constant = -1
    else:
        constant = 1
    for i in range(teams):
        output[2*i] = names[i]
        output[2*i+1] = constant * pfv[i]
    output = output.reshape(teams,2)

    final = sort(output)

    return final, A

permute = np.zeros(400).reshape(20,20)
permute[0,0] = 1
permute[1,1] = 1
permute[2,3] = 1
permute[3,4] = 1
permute[4,5] = 1
permute[5,6] = 1
permute[6,7] = 1
permute[7,14] = 1
permute[14,2] = 1
permute[8,8] = 1
permute[9,9] = 1
permute[10,10] = 1
permute[11,11] = 1
permute[12,12] = 1
permute[13,13] = 1
permute[15,15] = 1
permute[16,16] = 1
permute[17,17] = 1
permute[18,18] = 1
permute[19,19] = 1

largeData = "results.csv"
liveData = "https://www.football-data.co.uk/mmz4281/2122/E0.csv"
seasonString = "2020-21"

positions, last = ranking(largeData, seasonString)
print("ranking of last season:")
print(positions)
print()
B = np.matmul(np.matrix.transpose(permute),np.matmul(last,permute))
finalpos, x = prediction(liveData)
print("prediction for this season:")
print(finalpos)

x_pos = [i for i, _ in enumerate(finalpos[:,0])]
plt.bar(x_pos,finalpos[:,1])
plt.xticks(x_pos, finalpos[:,0],rotation='vertical',fontsize=11)
plt.xlabel(r"Team",fontsize=11)
plt.ylabel(r"Score",fontsize=11)
plt.savefig('prediction.pdf', format="pdf", bbox_inches='tight')
plt.show()

print()
print("Data last updated: " \
      +str(pd.read_csv(liveData,encoding = 'unicode_escape')['Date'].iloc[-1]))