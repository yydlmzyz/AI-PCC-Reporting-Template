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


def plot(R1, PSNR1, R2, PSNR2, figdir='./rdcurce.png'):
    fig, ax = plt.subplots(figsize=(7.3*2,5*2))
    plt.plot(R1, PSNR1, label='Anchor', color='red',marker='^', linewidth=4, markersize=16)
    plt.plot(R2, PSNR2, label='Tested', color='blue', marker='v', linewidth=4, markersize=16)
    ax.locator_params(axis='x', nbins=10)
    ax.locator_params(axis='y', nbins=10)
    plt.tick_params(labelsize=36)
    plt.xlabel("bpp", fontdict={'size':40})
    plt.ylabel("PSNR", fontdict={'size':40})
    plt.title('RD Curve', fontdict={'size':60})
    plt.grid(ls='-.')
    plt.legend(loc='lower right', prop={'size':32})
    fig.tight_layout()
    fig.savefig(figdir)
    print('save figure to ', figdir)

    return figdir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--csvdir1", type=str, default='csvfiles/anchor.csv')
    parser.add_argument("--csvdir2", type=str, default='csvfiles/tested.csv')
    parser.add_argument("--xlabel", type=str, default='bpp')
    parser.add_argument("--ylabel", type=str, default='PSNR')
    parser.add_argument("--figdir", type=str, default='./rdcurce.png')
    args = parser.parse_args()
    print('args:\n', args)

    df1 = pd.read_csv(args.csvdir1)
    df2 = pd.read_csv(args.csvdir2)

    print(args.csvdir1, ':\n', df1)
    print(args.csvdir2, ':\n', df2)

    R1 = df1[args.xlabel]
    PSNR1 = df1[args.ylabel]

    R2 = df2[args.xlabel]
    PSNR2 = df2[args.ylabel]

    bdrate = BD_RATE(R1, PSNR1, R2, PSNR2, piecewise=0)
    print('bdrate:\t\n', bdrate)

    plot(R1, PSNR1, R2, PSNR2, figdir=args.figdir)

