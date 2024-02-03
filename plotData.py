import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

def makeXGPlot():
    data = pd.read_json('main_data.json')
    
    data = data.loc[(data['xgDiff'] >= 1) & (data['xgDiff'] < 5)].groupby('xgDiff').mean()
    data = data.reset_index()
    
    text_color = '#FFFFFF'
    
    
    x = data.xgDiff
    y = data.cleanSheet

    fig, ax = plt.subplots()

    # calc the trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--",color='#4130B0')

    ax.scatter(x, y,s=5,color='#F96E46')
    print("y=%.6fx+%.6f"%(z[0],z[1]))
    ax.set_facecolor('#3D315B')
    fig.set_facecolor('#3D315B')

    _title = 'xG & Clean Sheets'
    
    plt.figtext(.5,.93,_title,fontsize=12,ha='center',color=text_color)
    plt.figtext(.5,.89,'Sum of xGA and xG of Opponent in Last 5 games vs Frequency of Clean Sheets',fontsize=8,ha='center',color=text_color)
    
    plt.ylabel('Frequency of Clean Sheets',color=text_color)
    plt.xlabel('xG of Opponent + Own xGA',color=text_color)
    
    plot_credits = 'Data: Understat | plot by: @bennivaluR_'
    plt.figtext(.68, .02, plot_credits, fontsize=6,color=text_color)

    ax.spines['bottom'].set_color(text_color)
    ax.spines['top'].set_color(text_color) 
    ax.spines['right'].set_color(text_color)
    ax.spines['left'].set_color(text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    _file_name = 'xg_spread'
    #Save the figure as a png
    plt.savefig( _file_name, facecolor=fig.get_facecolor(), dpi=1200)

def makeWinPlot():
    data = pd.read_json('main_data.json')
    
    data = data.loc[(data['xGTotalDifference'] > -3) & (data['xGTotalDifference'] < 3)].groupby('xGTotalDifference').mean()
    data = data.reset_index()
    
    text_color = '#FFFFFF'
    
    
    x = data.xGTotalDifference
    y = data.win

    fig, ax = plt.subplots()

    # calc the trendline
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x,p(x),"r--",color='#4130B0')

    ax.scatter(x, y,s=5,color='#F96E46')
    print("y=%.6fx+%.6f"%(z[0],z[1]))
    ax.set_facecolor('#3D315B')
    fig.set_facecolor('#3D315B')

    _title = 'xG & Wins'
    
    plt.figtext(.5,.93,_title,fontsize=12,ha='center',color=text_color)
    plt.figtext(.5,.89,' xG and xG Againts in Last 5 games vs Frequency of Wins (Big 5 Leagues)',fontsize=8,ha='center',color=text_color)
    
    plt.ylabel('Frequency of Wins',color=text_color)
    plt.xlabel('(xG-xGA) - (Opponent xG-xGA)',color=text_color)
    
    plot_credits = 'Data: Understat | plot by: @bennivaluR_'
    plt.figtext(.68, .02, plot_credits, fontsize=6,color=text_color)

    ax.spines['bottom'].set_color(text_color)
    ax.spines['top'].set_color(text_color) 
    ax.spines['right'].set_color(text_color)
    ax.spines['left'].set_color(text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    _file_name = 'win_spread'
    #Save the figure as a png
    plt.savefig( _file_name, facecolor=fig.get_facecolor(), dpi=1200)

def makeSingleGameWinPlot():
    data = pd.read_json('singleGameXGDiffWinRate_data.json')
    
    data = data.loc[(data['xGTotalDifference'] > -3) & (data['xGTotalDifference'] < 3)].groupby('xGTotalDifference').mean()
    data = data.reset_index()
    
    text_color = '#FFFFFF'
    
    
    x = data.xGTotalDifference
    y = data.win

    fig, ax = plt.subplots()

    plt.grid()
    ax.scatter(x, y,s=10,color='#F96E46')
    ax.set_facecolor('#3D315B')
    fig.set_facecolor('#3D315B')

    _title = 'xG & Wins'
    
    plt.figtext(.5,.93,_title,fontsize=12,ha='center',color=text_color)
    plt.figtext(.5,.89,' Win% vs xG Differential',fontsize=8,ha='center',color=text_color)
    
    plt.ylabel('Frequency of Wins',color=text_color)
    plt.xlabel('xG Difference',color=text_color)
    
    plot_credits = 'Data: Understat | plot by: @bennivaluR_'
    plt.figtext(.68, .02, plot_credits, fontsize=6,color=text_color)
    

    ax.spines['bottom'].set_color(text_color)
    ax.spines['top'].set_color(text_color) 
    ax.spines['right'].set_color(text_color)
    ax.spines['left'].set_color(text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)
    _file_name = 'singleGameXGDiffWinRate'
    #Save the figure as a png
    plt.savefig( _file_name, facecolor=fig.get_facecolor(), dpi=1200)

