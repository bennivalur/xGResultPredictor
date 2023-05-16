import asyncio
import json
import os
import urllib.request
import aiohttp
from datetime import datetime
import random

import pandas as pd

from understat import Understat

teams = {
    'Arsenal':0,
    'Aston Villa':0,
    'Bournemouth':0,
    'Brentford':0,
    'Brighton':0,
    'Chelsea':0,
    'Crystal Palace':0,
    'Everton':0,
    'Fulham':0,
    'Leicester':0,
    'Leeds':0,
    'Liverpool':0,
    'Manchester City':0,
    'Manchester United':0,
    'Newcastle United':0,
    'Nottingham Forest':0,
    'Southampton':0,
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
        'Chelsea':0,
        'Crystal Palace':0,
        'Everton':0,
        'Fulham':0,
        'Leicester':0,
        'Leeds':0,
        'Liverpool':0,
        'Manchester City':0,
        'Manchester United':0,
        'Newcastle United':0,
        'Nottingham Forest':0,
        'Southampton':0,
        'Tottenham':0,
        'West Ham':0,
        'Wolverhampton Wanderers':0
    }

    for w in weeks:
        with open(str(w)+'_clean_sheet_odds.json', 'r') as weekGames:
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

def runSimulations(n):
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

def processSimulations():
    resultOfSims = {}
    for keys in teams:
        resultOfSims[keys] = {}
        for i in range(20):
            resultOfSims[keys][str(i+1)] = 0
    
    
    with open('simulations.json', 'r') as simulations:
        s = json.load(simulations)

    resultOfSims['numberOfSimulations'] = len(s)
    print("len done")

    for sim in s:
        for i,t in enumerate(sim):
            resultOfSims[t[0]][str(20-i)] += 1
    
    with open('resultOfSimulations.json', 'w') as file:
        file.write(json.dumps(resultOfSims))





#getUnderStat('2022')

"""weeks = [37,38]
n = 2
print('--------------------')
#Get team name and actual points

leagueStandings = getRealLeagueStandings()

runSimulations(n)"""

processSimulations()
