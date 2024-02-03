import asyncio
import json
import os
import urllib.request
import aiohttp
from datetime import datetime
import random
from predictCS import predictCS

import pandas as pd

from understat import Understat

teams = {
    'Arsenal':0,
    'Aston Villa':0,
    'Bournemouth':0,
    'Brentford':0,
    'Brighton':0,
    'Burnley':0,
    'Chelsea':0,
    'Crystal Palace':0,
    'Everton':0,
    'Fulham':0,
    'Liverpool':0,
    'Luton':0,
    'Manchester City':0,
    'Manchester United':0,
    'Newcastle United':0,
    'Nottingham Forest':0,
    'Sheffield United':0,
    'Tottenham':0,
    'West Ham':0,
    'Wolverhampton Wanderers':0
}


async def getFixtures(season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        table = await understat.get_league_table(
            "epl", season
        )

        data = json.dumps(table)
        with open('table.json', 'w') as file:
            file.write(data)

def getUnderStat(season):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getFixtures(season))

def runWeeks(weeks):
    teams = {
        'Arsenal':0,
        'Aston Villa':0,
        'Bournemouth':0,
        'Brentford':0,
        'Brighton':0,
        'Burnley':0,
        'Chelsea':0,
        'Crystal Palace':0,
        'Everton':0,
        'Fulham':0,
        'Liverpool':0,
        'Luton':0,
        'Manchester City':0,
        'Manchester United':0,
        'Newcastle United':0,
        'Nottingham Forest':0,
        'Sheffield United':0,
        'Tottenham':0,
        'West Ham':0,
        'Wolverhampton Wanderers':0
    }

    for w in weeks:
        with open('epl/' + str(w)+'_clean_sheet_odds.json', 'r') as weekGames:
            games = json.load(weekGames)
        
        for i,g in enumerate(games):
            #print(g)
            if i % 2 == 0:
                home = games[i]["winOdds"]
                draw = 1 - games[i+1]["winOdds"]
                #away == 100
                res = random.random()
                if res <= home:
                    #print("home win")
                    teams[games[i]['team']] += 3
                elif res <= draw:
                    #print("draw")
                    teams[games[i]['team']] += 1
                    teams[games[i+1]['team']] += 1
                else:
                    #print("away win")
                    teams[games[i+1]['team']] += 3
                
    return teams

def getRealLeagueStandings():
    with open('table.json', 'r') as leagueFull:
        tl = json.load(leagueFull)

    leagueStandings = {}

    for t in tl:
        if t[0] != 'Team':
            leagueStandings[t[0]] = t[7]

    return leagueStandings

def runSimulations(n,leagueStandings):
    simulations = []
    for i in range(n):
        results = runWeeks(weeks)
        for key in results:
            results[key] += leagueStandings[key]
        res = []
        for s in sorted(results.items(),key=lambda item:item[1]):
            res.append([s[0],s[1]])
        
        simulations.append(res)

    with open('simulations.json', 'w') as file:
        file.write(json.dumps(simulations))

def processSimulations(n):
    resultOfSims = {}
    for keys in teams:
        resultOfSims[keys] = {}
        for i in range(20):
            resultOfSims[keys][str(i+1)] = 0
    
    
    with open('simulations.json', 'r') as simulations:
        s = json.load(simulations)

    resultOfSims['numberOfSimulations'] = n

    for sim in s:
        for i,t in enumerate(sim):
            resultOfSims[t[0]][str(20-i)] += 1
    
    with open('resultOfSimulations.json', 'w') as file:
        file.write(json.dumps(resultOfSims))

def printResults(n):
    
    with open('resultOfSimulations.json', 'r') as resultOfSims:
        resultOfSims = json.load(resultOfSims)

    longestTeamName = findLongestName(resultOfSims.keys())
    print(longestTeamName)
    header = balanceTeamNameSpaces('Teams',longestTeamName)
    for i in range(20):
        header = header + ' '*(5-len(str(i+1))) + str(i+1) + '|'
    
    print(header)
    for keys in resultOfSims:
        line = balanceTeamNameSpaces(keys,longestTeamName)
        if keys != 'numberOfSimulations':
            for pos in resultOfSims[keys]:
                #print(pos)
                line += balanceNumber(resultOfSims[keys][pos],n,1) + '|'
            print(line)

def findLongestName(teams):
    return len(max(teams,key=len))


def balanceTeamNameSpaces(team,longestTeamName):
    spaces = longestTeamName - len(team)
    return  ' '*spaces + team +'|'

def balanceNumber(number,n,sigDigits):
    strLength = sigDigits + 4
    perc = round(number/n*100,sigDigits)
    numLength = len(str(perc))
    return ' '*(strLength-numLength) + str(perc)



getUnderStat('2023')

weeks = [23,24,25,26,27,28,29,30,31,32,33,34,36,37,38]
predictCS(weeks)
n = 1000000
#n=10
print('--------------------')
#Get team name and actual points

leagueStandings = getRealLeagueStandings()

runSimulations(n,leagueStandings)

processSimulations(n)
printResults(n)