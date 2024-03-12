import asyncio
import json
import os
import urllib.request
import aiohttp
from datetime import datetime

import pandas as pd

from understat import Understat


teams = [
    {'title':'0','uid':-1},
    {'title':'Arsenal','uid': '83'},
    {'title':'Aston Villa','uid':'71'},
    {'title':'Bournemouth','uid':'73'},
    {'title':'Brentford','uid':'244'},
    {'title':'Brighton','uid':'220'},
    {'title':'Burnley','uid':'92'},
    {'title':'Chelsea', 'uid':'80'},
    {'title':'Crystal Palace','uid':'78'},
    {'title':'Everton','uid':'72'},
    {'title':'Fulham','uid':'228'},
    {'title':'Liverpool','uid':'87'},
    {'title':'Luton','uid':'256'},
    {'title':'Manchester City','uid':'88'},
    {'title':'Manchester United','uid':'89'},
    {'title':'Newcastle United','uid':'86'},
    {'title':'Nottingham Forest','uid':'249'},
    {'title':'Sheffield United', 'uid':'238'},
    {'title':'Tottenham','uid':'82'},
    {'title':'West Ham', 'uid':'81'},
    {'title':'Wolverhampton Wanderers','uid':'229'},
]
async def getFixtures(season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_fixtures(
            "epl", season
        )

        data = json.dumps(results)
        with open('fixtures.json', 'w') as file:
            file.write(data)

def getUnderStat(season):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getFixtures(season))

def fplFixtures():
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/fixtures/").read()
    fpl = json.loads(fpl)
    fixtures = [x for x in fpl if x['finished'] == False and x['kickoff_time'] != None]
    results = json.dumps(fixtures)
    with open('fixtures.json', 'w') as file:
        file.write(results)

def getResults(league):
    with open('results/'+ league +'_2023_res.json', 'r') as all_weeks:
        results = json.load(all_weeks)
    return results
    

def calcCSOdds(xGSum):
    odds = (xGSum * -1 * 0.114150) + 0.599407
    if odds <= 0:
        return 0
    return odds

def calcWinOdds(xGSum):
    odds = (xGSum  * 0.116178) + 0.392198
    if odds <= 0:
        return 0
    return odds

def getNextGameWeek():
    
    fpl = urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/").read()
    fpl_players = json.loads(fpl)
    fpl_players = fpl_players['events']
    results = json.dumps(fpl_players)
    with open('events.json', 'w') as file:
        file.write(results)

    with open('events.json', 'r') as all_weeks:
        weeks = json.load(all_weeks)
    
    for e in weeks:
        if(e['is_next']):
            return e['id']

def getGameWeek(week):
    with open('events.json', 'r') as all_games:
        games = json.load(all_games)
    
    return games[week-1]


def getFix(league):
    with open('fixtures/' +league + '_fixtures.json', 'r') as all_games:
        games = json.load(all_games)
    
    return games

def calcXG(games,teamID):
    xG = 0
    xGA = 0
    
    for tg in games:
        if(tg['h']['id'] == teamID):
            team = 'h'
            opponent = 'a'
        else:
            team = 'a'
            opponent = 'h'

        xG += float(tg['xG'][team])
        xGA += float(tg['xG'][opponent])
    if(len(games) != 0):
        xG = xG/len(games)
        xGA = xGA/len(games)
    return {'xG':xG,'xGA':xGA}

#getUnderStat(2020)
#fplFixtures()
def predictCS(weeks,gameRange):
    fplFixtures()
    for week in weeks:

        deadline = getGameWeek(week)['deadline_time']
        if(week == 38):
            endOfGameWeek = "3023-05-28T14:00:00Z"
        else:
            endOfGameWeek = getGameWeek(week+1)['deadline_time']

        #Get upcoming fixtures
        games = getFix('epl')
        games = sorted(games, key=lambda t: datetime.strptime(t['kickoff_time'], '%Y-%m-%dT%H:%M:%SZ'))

        #Filter games in upcoming gameweek
        gameweekGames = []
        for g in games:
            if(g['kickoff_time'] < endOfGameWeek and g['kickoff_time'] > deadline):
                gameweekGames.append([teams[g['team_h']],teams[g['team_a']]])
            
        #Get games already played
        results = getResults('EPL')

        allOdds = []

        for g in gameweekGames:
            #Get last X games a team played in
            homeTeamGames = [x for x in results if x['h']['id'] == g[0]['uid'] or x['a']['id'] == g[0]['uid']][-gameRange:]
            awayTeamGames = [x for x in results if x['h']['id'] == g[1]['uid'] or x['a']['id'] == g[1]['uid']][-gameRange:]
            if(len(homeTeamGames) == 0):
                print(g)
            #Calculate xg
            homeXG = calcXG(homeTeamGames,g[0]['uid'])
            awayXG = calcXG(awayTeamGames,g[1]['uid'])

            #Calculate odds
            homeOdds = round(calcCSOdds(awayXG['xG']+homeXG['xGA']),2)
            awayOdds = round(calcCSOdds(homeXG['xG']+awayXG['xGA']),2)

            #Calculate win odds
            homeWinOdds = round(calcWinOdds((homeXG['xG']+awayXG['xGA']) - (awayXG['xG']+homeXG['xGA'])),2)
            awayWinOdds = round(calcWinOdds((awayXG['xG']+homeXG['xGA']) - (homeXG['xG']+awayXG['xGA'])),2)

            allOdds.append({'team':g[0]['title'],'opponent':g[1]['title'],'csOdds':homeOdds,'winOdds':homeWinOdds})
            allOdds.append({'team':g[1]['title'],'opponent':g[0]['title'],'csOdds':awayOdds,'winOdds':awayWinOdds})

        #Print the odds
        '''
        for i,x in enumerate(allOdds):
            if i % 2 == 0:
                print(f'{allOdds[i]["team"]}: {allOdds[i]["winOdds"]} - DRAW: {round(1 - allOdds[i]["winOdds"] - allOdds[i+1]["winOdds"],2)} - {allOdds[i+1]["team"]}: {allOdds[i+1]["winOdds"]}')
            else:
                print("-----------------------------------------------------------------------------")
        '''



        with open('epl/' + str(week) + '_odds.json', 'w') as file:
            file.write(json.dumps(allOdds))

def predictRestOfSeasonCS(league,gameRange):
    
        
    #Get upcoming fixtures
    games = getFix(league)
    
    #Get games already played
    results = getResults(league)

    allOdds = []

    for g in games:
        #Get last X games a team played in
        homeTeamGames = [x for x in results if x['h']['id'] == g['h']['id'] or x['a']['id'] == g['h']['id']][-gameRange:]
        awayTeamGames = [x for x in results if x['h']['id'] == g['a']['id'] or x['a']['id'] == g['a']['id']][-gameRange:]
        if(len(homeTeamGames) == 0):
            print(g)
            print(results[0])
        #Calculate xg
        homeXG = calcXG(homeTeamGames,g['h']['id'])
        awayXG = calcXG(awayTeamGames,g['a']['id'])

        #Calculate odds
        homeOdds = round(calcCSOdds(awayXG['xG']+homeXG['xGA']),2)
        awayOdds = round(calcCSOdds(homeXG['xG']+awayXG['xGA']),2)

        #Calculate win odds
        homeWinOdds = round(calcWinOdds((homeXG['xG']+awayXG['xGA']) - (awayXG['xG']+homeXG['xGA'])),2)
        awayWinOdds = round(calcWinOdds((awayXG['xG']+homeXG['xGA']) - (homeXG['xG']+awayXG['xGA'])),2)

        allOdds.append({'team':g['h']['title'],'opponent':g['a']['title'],'csOdds':homeOdds,'winOdds':homeWinOdds})
        allOdds.append({'team':g['a']['title'],'opponent':g['h']['title'],'csOdds':awayOdds,'winOdds':awayWinOdds})

    #Print the odds
    '''
    for i,x in enumerate(allOdds):
        if i % 2 == 0:
            print(f'{allOdds[i]["team"]}: {allOdds[i]["winOdds"]} - DRAW: {round(1 - allOdds[i]["winOdds"] - allOdds[i+1]["winOdds"],2)} - {allOdds[i+1]["team"]}: {allOdds[i+1]["winOdds"]}')
        else:
            print("-----------------------------------------------------------------------------")
    '''



    with open('csOdds/' + league +'_odds.json', 'w') as file:
        file.write(json.dumps(allOdds))