import asyncio
import json
import os
import urllib.request
import aiohttp

from understat import Understat


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

async def getLeagueTable(league,season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        table = await understat.get_league_table(
            league, season
        )

        data = json.dumps(table)
        with open('leagueTables/' + league + '_' + season + '_table.json', 'w') as file:
            file.write(data)

async def getLeagueFixtures(league,season):
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        table = await understat.get_league_fixtures(
            league, season
        )

        data = json.dumps(table)
        with open('fixtures/' + league + '_fixtures.json', 'w') as file:
            file.write(data)


def getSeasons(league:str,season:str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(league,season))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getLeagueTable(league,season))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getLeagueFixtures(league,season))

def getResults(leagues,seasons):
    for l in leagues:
        for s in seasons:
            getSeasons(l,s)


