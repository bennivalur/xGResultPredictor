import asyncio
import json
import os
import urllib.request
import aiohttp
from datetime import datetime

from understat import Understat

leagues = ['EPL','La_Liga','Bundesliga','Serie_A','Ligue_1','RFPL']
seasons = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

#leagues = ['EPL']
#seasons = ['2019']

gameRange = 5

def getPastGames(teamID:str,gameID:str,game, games,gameRange):
    #filter for team
    teamGames = [x for x in games if x['h']['id'] == teamID or x['a']['id'] == teamID]
    
    #getIndex of current game
    indx = teamGames.index(game)

    #Shorten range if games played < 5
    temp_range = gameRange
    if(indx < 5):
        temp_range = indx

    gamesInRange = teamGames[indx-temp_range:indx]

    if(len(gamesInRange) < 5):
        return 'NoGames'

    xG = 0
    xGA = 0

    for tg in gamesInRange:
        if(tg['h']['id'] == teamID):
            team = 'h'
            opponent = 'a'
        else:
            team = 'a'
            opponent = 'h'

        xG += float(tg['xG'][team])
        xGA += float(tg['xG'][opponent])

    if(game['h']['id'] == teamID):
        team = 'h'
        opponent = 'a'
    else:
        team = 'a'
        opponent = 'h'

    if game['goals'][opponent] == '0':
        cs = 1
    else:
        cs = 0

    
    return {'xG':xG/len(gamesInRange),'xGA':xGA/len(gamesInRange),'conceded':int(game['goals'][opponent]),'cleanSheet':cs}


def runSeason(league,season):
    with open('results/'+league+'_'+season+'_res.json', 'r') as all_games:
        games = json.load(all_games)
    
    data = []

    games = sorted(games, key=lambda t: datetime.strptime(t['datetime'], '%Y-%m-%d %H:%M:%S'))
    game = games[15]
    for game in games:
        homeTeam = getPastGames(game['h']['id'],game['id'],game,games,gameRange)
        awayTeam = getPastGames(game['a']['id'],game['id'],game,games,gameRange)

        if(homeTeam != 'NoGames' and awayTeam != 'NoGames'):
            data.append({'xgDiff':round(awayTeam['xG']+homeTeam['xGA'],1),'cleanSheet':homeTeam['cleanSheet']})
            data.append({'xgDiff':round(homeTeam['xG']+awayTeam['xGA'],1),'cleanSheet':awayTeam['cleanSheet']})

    return data
        
def processData():
    data = []
    for l in leagues:
        for s in seasons:
            print("Running " +l + ':' + s)
            data += runSeason(l,s)

    with open('main_data.json', 'w') as file:
        file.write(json.dumps(data))

processData()