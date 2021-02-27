import json
import pandas as pd
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error

import statistics

def makePlot():
    data = pd.read_json('main_data.json')
    
    data = data.loc[(data['xgDiff'] >= 1)].groupby('xgDiff').mean()
    data = data.reset_index()
    
    
    
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
    
    plt.figtext(.5,.93,_title,fontsize=12,ha='center')
    plt.figtext(.5,.89,'Sum of xGA and xG of Opponent in Last 5 games vs Frequency of Clean Sheets',fontsize=8,ha='center')
    
    plt.ylabel('Frequency of Clean Sheets')
    plt.xlabel('xGA + xG of Opponent')
    
    plot_credits = 'Data: Understat | plot by: @bennivaluR_'
    plt.figtext(.68, .02, plot_credits, fontsize=6)
    _file_name = 'xg_spread'
    #Save the figure as a png
    plt.savefig( _file_name, facecolor=fig.get_facecolor(), dpi=1200)

makePlot()