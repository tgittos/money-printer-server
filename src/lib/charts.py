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
    orange_line = 'o-'
    
    oscillator_colors = [
        red_line,
        green_line,
        orange_line
    ]
    
    has_multi_osc = True in ['own_scale' in o for o in oscillators]
    n = 1
    if has_multi_osc:
        n = 2
    fig, axs = plt.subplots(len(data) + n, sharex=True, sharey=False)
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
        scale = None
        if 'own_scale' in o:
            scale = o['own_scale']
        
        # generate new subplot, if requested
        if not scale == None and scale:
            # plot data
            if c_type == 'line':
                axs[len(data)+1].plot(vals, label = label)

            if c_type == 'bar':
                x_pos = [i for i, _ in enumerate(vals)]
                axs[len(data)+1].bar(x_pos, vals, label = label)
            axs[len(data)+1].legend()
        else:      
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