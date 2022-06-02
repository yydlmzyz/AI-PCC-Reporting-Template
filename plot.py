import os
import matplotlib.pyplot as plt


def plot_curves(data_list, figdir='./rdcurce.png',
                color_list=['red','green','blue'], marker_list=['^','v','>', '<']):
    """plot (RD) curves for each x/y pair in the data_list
    """
    fig, ax = plt.subplots(figsize=(7.3*2,5*2))
    for i, data in  enumerate(data_list):
        plt.plot(data['x'], data['y'], label=data['name'], 
                 color=color_list[i%len(color_list)], 
                 marker=marker_list[i%len(marker_list)], 
                 linewidth=4, markersize=16)
    xlabel, ylabel = data_list[0]['xlabel'], data_list[0]['ylabel']
    ax.locator_params(axis='x', nbins=10)
    ax.locator_params(axis='y', nbins=10)
    plt.tick_params(labelsize=36)
    plt.xlabel(xlabel, fontdict={'size':40})
    plt.ylabel(ylabel, fontdict={'size':40})
    figname = os.path.split(figdir)[-1].split('.')[0]
    plt.title(figname, fontdict={'size':40})
    plt.grid(ls='-.')
    plt.legend(loc='lower right', prop={'size':40})
    fig.tight_layout()
    fig.savefig(figdir)
    print('save figure to ', figdir)

    return figdir

