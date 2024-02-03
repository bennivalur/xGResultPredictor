from getData import getResults
from processData import processData
from predictCS import predictCS,getNextGameWeek
from graphCSOdds import drawCleanSheetOdds
from graphWinOdds import drawWinOdds
from plotData import makeXGPlot, makeWinPlot,makeSingleGameWinPlot

#leagues = ['EPL','La_Liga','Bundesliga','Serie_A','Ligue_1','RFPL']
leagues = ['EPL']
seasons = ['2023']
#seasons = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']
nextGameWeek = getNextGameWeek()

#Get and process data
getResults(leagues,seasons)
processData(leagues,seasons)
predictCS([nextGameWeek])

#Plot results
drawCleanSheetOdds(nextGameWeek)
drawWinOdds(nextGameWeek)
makeXGPlot()
makeWinPlot()
makeSingleGameWinPlot()
