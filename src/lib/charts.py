# python shit
from datetime import datetime, timedelta, timezone

# others shit
from matplotlib import pyplot
import pandas as pandas
import numpy as np
from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def chart(ticker, data, oscillators = [], debug = False):
    # define vars
    blue_line = '-'
    red_line = 'r-'
    green_line = 'g-'
    
    oscillator_colors = [
        red_line,
        green_line
    ]
    
    fig, axs = plt.subplots(len(data) + 1, sharex=True, sharey=False)
    fig.set_size_inches(18.5, 10.5, forward=True)
    
    # extract data sets and axis names from the data
    for i in range(0, len(data)):
        label = data[i]['label']
        vals = data[i]['data']
    
        # plot data
        axs[i].plot(vals, label = label)
    
    # chart the oscilators
    for o in oscillators:
        label = o['label']
        vals = o['data']
        c_type = o['chart']
        
        # plot data
        if c_type == 'line':
            axs[len(data)].plot(vals, label = label)
        
        if c_type == 'bar':
            x_pos = [i for i, _ in enumerate(vals)]
            axs[len(data)].bar(x_pos, vals, label = label)
        
    # label the x axis
    plt.xlabel("Days")
    
    # display the legend
    axs[0].legend()
    axs[1].legend()
    
    # set the color
    # plt.setp(lines, color='r', linewidth=2.0)
    
    # render
    plt.show()