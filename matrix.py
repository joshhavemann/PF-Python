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

hc = np.zeros(16)+1
ac = np.zeros(16)+1

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

def matrix(csv, pastCSV, useLast):
    matrix = np.zeros(shape=(20,20))
    return matrix
    


