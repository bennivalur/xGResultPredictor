import asyncio
import json
import os
import urllib.request
import aiohttp

from understat import Understat

leagues = ['EPL','La_Liga','Bundesliga','Serie_A','Ligue_1','RFPL']
seasons = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
async def main(league:str,season:str):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        results = await understat.get_league_results(
            league, season
        )

        print('Getting ' + league + ':' + season )
        results = json.dumps(results)
        with open('results/'+league+'_'+season+'_res.json', 'w') as file:
            file.write(results)

def getSeasons(league:str,season:str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(league,season))

def getResults():
    for l in leagues:
        for s in seasons:
            getSeasons(l,s)

getResults()