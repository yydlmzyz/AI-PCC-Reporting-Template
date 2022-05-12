"""
Input:
two .csv files which include the raw data for comparison.
Output:
BD-Rate difference; RD curve
"""

import os, argparse
from re import L
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bjontegaard_metric import BD_RATE, BD_PSNR


def split_dataframe(df, index_name='sequence', columns=None):
    """
    """
    df.set_index(index_name, inplace=True)
    indices = df.index.unique()
    df_set = {}
    for _, index in enumerate(indices):
        if columns is None: df_one = df.loc[index]
        else: df_one = df.loc[index][columns]
        df_set[index] = df_one
    
    return df_set


def plot(data_list, figdir='./rdcurce.png',
          color_list=['red','green','blue'], marker_list=['^','v','>', '<']):
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
    plt.title(figname, fontdict={'size':60})
    plt.grid(ls='-.')
    plt.legend(loc='lower right', prop={'size':32})
    fig.tight_layout()
    fig.savefig(figdir)
    print('save figure to ', figdir)

    return figdir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--csvdir1", type=str, default='csvfiles/reporting_template_lossy.csv')
    parser.add_argument("--csvdir2", type=str, default='csvfiles/test.csv')
    parser.add_argument("--xlabel", type=str, default='numBitsGeoEncT')
    parser.add_argument("--ylabel", type=str, default='d1T')
    parser.add_argument("--figdir", type=str, default='./rdcurce.png')
    args = parser.parse_args()
    print('args:\n', args)

    df1 = pd.read_csv(args.csvdir1)
    df1_set = split_dataframe(df1)
    # columns=['numOutputPointsT', 'numBitsGeoEncT', 'd1T', 'd2T']

    df2 = pd.read_csv(args.csvdir2)
    df2_set = split_dataframe(df2)

    seqs_name_list = list(df2_set.keys())
    
    for _, seqs_name in enumerate(seqs_name_list):
        df1_one = df1_set[seqs_name]
        df2_one = df2_set[seqs_name]
        print(df1_one, '\n', df2_one)
        # BD-Rate
        R1 = df1_one[args.xlabel]
        PSNR1 = df1_one[args.ylabel]
        R2 = df2_one[args.xlabel]
        PSNR2 = df2_one[args.ylabel]
        bdrate = BD_RATE(R1, PSNR1, R2, PSNR2, piecewise=0)
        print('bdrate:\t', bdrate)
        # plot
        data1 = {'name':'anchor', 'xlabel':args.xlabel, 'ylabel':args.ylabel, 
            'x':df1_one[args.xlabel], 'y':df1_one[args.ylabel]}
        data2 = {'name':'test', 'xlabel':args.xlabel, 'ylabel':args.ylabel, 
            'x':df2_one[args.xlabel], 'y':df2_one[args.ylabel]}
        figdir = os.path.join('figs', seqs_name+'.png')
        os.makedirs('figs', exist_ok=True)
        plot([data1, data2], figdir=figdir)

