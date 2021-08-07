import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_sensitivity(
        data,
        folder = "",
        color = (1,0,0),
        greyscale = False,
        padding = 0.25,
        title = "",
        dpi = 200
    ):
    '''
    Create a graphical representation of the sensitivity of model parameters/settings.
    '''
    
    id = title.replace(" ","_")
    
    if greyscale:
        id += "-greyscale"
        color = (0,0,0)
    
    fig_width = 2000
    fig_height = 1000
    
    fig = plt.figure(figsize=(fig_width/dpi, fig_height/dpi))
    ax = fig.add_subplot(1, 1, 1)
    
    variables = sorted([x for x in data])
    limits = set_limits(ax, variables, padding)
    
    ax.plot(limits["x_lim"], [0., 0.], "#cccccc", linestyle=":", linewidth=0.5, zorder=0)
    ax.grid(axis="x", color="#cccccc", linestyle=":", linewidth=0.5)
    ax.set_axisbelow(True)
    
    for i in range(len(variables)):
        plot_bars(ax, data[variables[i]], center=limits["x_ticks"][i], width=limits["x_var_width"], color=color)
    
    
    ax.set_title(f"Sensitivity of {id}")
    
    # center_axis(ax)
    # turn_off_axis(ax, axis="y")
    
    # Add percentage symbol to y axis
    fmt = '{x:,.0f}%'
    tick = mtick.StrMethodFormatter(fmt)
    ax.yaxis.set_major_formatter(tick)
    
    plt.savefig(
        os.path.join(folder, f"sensitivity_{id}.png"),
        bbox_inches = "tight",
        dpi = dpi
    )
    plt.close()

def set_limits(ax, variables, padding):
    '''
    From the user settings, setup the axis limits, labels and formating.
    '''
    limits = {}
    
    # x axis
    x_left = 0
    x_right = 1
    limits["x_ticks"] = np.linspace(x_left, x_right, len(variables)+2)[1:-1]
    limits["x_ticks_gap"] = limits["x_ticks"][1] - limits["x_ticks"][0]
    limits["x_tick_labels"] = variables
    limits["x_ticks_minor"] = []
    limits["x_lim"] = np.array([x_left, x_right])
    limits["x_var_width"] = (1.-padding)*limits["x_ticks_gap"]
    
    # Set axis limits
    ax.set_xlim(limits["x_lim"])
    
    # Set ticks and tick labels
    ax.tick_params(axis='x', which='major', size= 10)
    # ax.tick_params(axis='x', which='minor', size= 10)
    ax.set_xticks(limits["x_ticks"])
    ax.set_xticks(limits["x_ticks_minor"], minor = True)
    ax.set_xticklabels(limits["x_tick_labels"], rotation=60, ha="right", fontsize=6)
    
    # y axis
    # y_top = 1
    # y_center = 0
    # y_bottom = 0
    
    # limits["y_lim"] = np.array([y_bottom,y_top])
    # limits["y_top"] = np.array([y_top,y_top])
    # limits["y_center"] = np.array([y_center,y_center])
    # limits["y_bottom"] = np.array([y_bottom,y_bottom])
    
    # ax.set_ylim(limits["y_lim"])
    
    return limits

def center_axis(ax):
    '''
    By default, Matplotlib shows the axis bar at the edges of the plot.
    This function places the axis at the center of the plot, just like drawing an axis on paper:
                y
                ^
                |
                |
    ------------|-----------> x
                |
    '''
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')

    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Show ticks on the left and lower axes only (and let them protrude in both directions)
    ax.xaxis.set_tick_params(which="both", bottom='on', top=False, direction='inout')
    ax.yaxis.set_tick_params(which="both", left='on', right=False, direction='inout')

def turn_off_axis(ax, axis="y"):
    '''
    Completely remove lines and labels from an axis
    '''
    if axis == "x":
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_color('none')
        
        # Remove ticks, tick labels and axis labels
        ax.xaxis.set_tick_params(bottom=False, top=False, labelleft=False)
    elif axis == "y":
        # Remove spines
        ax.spines['left'].set_color('none')
        ax.spines['right'].set_color('none')
        
        # Remove ticks, tick labels and axis labels
        ax.yaxis.set_tick_params(left=False, right=False, labelbottom=False)

def plot_bars(ax, data, center=0., width=1., color=(0,0,0)):
    
    settings = sorted([x for x in data])
    total = len(settings)
    
    for i in range(total):
        x1 = center - 0.5*width + i*width/total
        x2 = center - 0.5*width + (i+1)*width/total
        
        y0 = 0.
        y1 = 100*data[settings[i]]
        
        alpha = min(1, 0.2 + 0.8*abs(100*settings[i]))
        
        color = (color[0], color[1], color[2], alpha)
        
        ax.fill_between([x1, x2], [y0, y0], [y1, y1], facecolor=color, edgecolor="k")