'''
Matrix

Gets a single coefficient given a csv, and a home and away team

Available data:
    
FTHG and HG = Full Time Home Team Goals
FTAG and AG = Full Time Away Team Goals
FTR and Res = Full Time Result (H=Home Win, D=Draw, A=Away Win)
HTHG = Half Time Home Team Goals will not use
HTAG = Half Time Away Team Goals will not use
HTR = Half Time Result (H=Home Win, D=Draw, A=Away Win) will not use

Match Statistics (where available)
Attendance = Crowd Attendance
Referee = Match Referee
HS = Home Team Shots
AS = Away Team Shots
HST = Home Team Shots on Target
AST = Away Team Shots on Target
HHW = Home Team Hit Woodwork
AHW = Away Team Hit Woodwork
HC = Home Team Corners
AC = Away Team Corners
HF = Home Team Fouls Committed
AF = Away Team Fouls Committed
HFKC = Home Team Free Kicks Conceded
AFKC = Away Team Free Kicks Conceded
HO = Home Team Offsides
AO = Away Team Offsides
HY = Home Team Yellow Cards
AY = Away Team Yellow Cards
HR = Home Team Red Cards
AR = Away Team Red Cards
HBP = Home Team Bookings Points (10 = yellow, 25 = red) will not use
ABP = Away Team Bookings Points (10 = yellow, 25 = red) will not use

Note that Free Kicks Conceeded includes fouls, offsides and any other offense
commmitted and will always be equal to or higher than the number of fouls.
 Fouls make up the vast majority of Free Kicks Conceded.
 Free Kicks Conceded are shown when specific data on Fouls are not available
 (France 2nd, Belgium 1st and Greece 1st divisions).

Note also that English and Scottish yellow cards do not include the initial
yellow card when a second is shown to a player converting it into a red,
but this is included as a yellow (plus red) for European games.
    
'''
import numpy as np
import pandas as pd
from error import actual

# Sets of coefficients used for minimisation
co_FTHG = 1
co_FTAG = 1
co_HTHG = 1
co_HTAG = 1
co_HS = 1
co_AS = 1
co_HST = 1
co_AST = 1
co_HF = 1
co_AF = 1
co_HC = 1
co_AC = 1
co_HY = 1
co_AY = 1
co_HR = 1
co_AR = 1

hc = np.zeros(16)+1/16
ac = np.zeros(16)+1/16

def singleEntry(csv, homeTeam, awayTeam, homeCoeffs, awayCoeffs):
    '''
    

    Parameters
    ----------
    csv : csv file to be used
    homeTeam : string of home team's name
    awayTeam : string of away team's name
    homeCoeffs : array of coefficients for home team
    awayCoeffs : array of coefficients for home team
    

    Returns
    -------
    A home team value and an away team value

    '''
    df = pd.read_csv(csv)
    df = df[df['HomeTeam'] == homeTeam]
    df = df[df['AwayTeam'] == awayTeam]
    df = df.drop(['Div', 'Date' , 'Time','FTR', 'HTR', 'HomeTeam', 'AwayTeam', 'Referee'], axis=1)
    homeValue = awayValue = 0
    for i in range(len(homeCoeffs)):
        
        homeValue += homeCoeffs[i] * df.iloc[0][i]
        awayValue += awayCoeffs[i] * df.iloc[0][i]
    return homeValue, awayValue

def getCSV(season):
    '''
    Single csv given string of season
    '''
    return "https://www.football-data.co.uk/mmz4281/"+season+"/E0.csv"

def getCSVs(currentSeason,league):
    '''
    Will return a CSV for that season and league
    (0 for prem, 1 for championship), and the past 3 seasons before that,
    needs to be strings in the format '2122' (for example).
    '''
    part1 = "https://www.football-data.co.uk/mmz4281/"
    part2 = "/E"
    part3 = ".csv"
    int1 = int(currentSeason[0:2])
    int2 = int(currentSeason[2:4])
    csv1 = part1+currentSeason+part2+league+part3
    csv2 = part1+str(int1-1)+str(int2-1)+part2+league+part3
    csv3 = part1+str(int1-2)+str(int2-2)+part2+league+part3
    csv4 = part1+str(int1-3)+str(int2-3)+part2+league+part3
    return csv1, csv2, csv3, csv4

seasonWeighting = 2/3
minus1Weighting = 1/2
minus2Weighting = 1/4
minus3Weighting = 1/8

def pastPrep(lastseason):
    csvA, csvB, csvC, csvD = getCSVs(lastseason,"0")
    # 2021 1920 1819 1718
    csvE, csvF, csvG, csvH = getCSVs(lastseason,"1")
    data = pd.read_csv(csvA,encoding = 'unicode_escape')
    print(data.HomeTeam.unique())
    last = actual(pd.read_csv(csvE,encoding = 'unicode_escape'))
    lastprem = actual(pd.read_csv(csvA,encoding = 'unicode_escape'))
    ch1 = last[0,0]
    ch2 = last[1,0]
    ch3 = last[2,0]
    pr18 = lastprem[17,0]
    pr19 = lastprem[18,0]
    pr20 = lastprem[19,0]
    data.replace(pr18, ch1, inplace = True)
    data.replace(pr19, ch2, inplace = True)
    data.replace(pr20, ch3, inplace = True)
    print(data.HomeTeam.unique())
    return data



def matrix(currentSeason):
    
    csvA, csvB, csvC, csvD = getCSVs("2122","0")
    df = pd.read_csv(csvA,encoding = 'unicode_escape')
    names = df.HomeTeam.unique()
    teams = len(names)
    seasonForm = np.zeros(teams)
    matrix = np.zeros(shape=(teams,teams))
    print(names)
    entries = len(df)
    played = np.eye(teams)
    homeSF = 1
    awaySF = 1
    for k in range(entries): # Extracting data from dataframe
        home = df['HomeTeam'][k]
        away = df['AwayTeam'][k]
        index1 = np.argwhere(names == home)[0][0]
        index2 = np.argwhere(names == away)[0][0]
        played[index1,index2] = 1

    for i in range(teams):
        for j in range(teams):
            if played[i,j] == 1:
                homescore, awayscore = singleEntry(csvA,names[i],names[j],hc,ac)
                seasonForm[i] += homescore
                seasonForm[j] += awayscore

            elif played[j,i] == 1:
                homescore, awayscore = singleEntry(csvA,names[j],names[i],hc,ac)
                matrix[i,j] += homeSF * homescore
                matrix[j,i] += awaySF * awayscore

            else:
                # turn past prep to csv and input
                homescore, awayscore = singleEntry(csvB,names[i],names[j],hc,ac)
                matrix[i,j] += homescore
                matrix[j,i] += awayscore
            #then add guaranteed past results and season form then add actual results in, then minimise error, and scale by a constant factor (then adding in results again unscaled)
    return matrix
