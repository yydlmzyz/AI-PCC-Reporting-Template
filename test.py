"""
Input:
two .csv files which include the raw data for comparison.
Output:
BD-Rate difference; RD curve
"""

import os, argparse
import pandas as pd
import numpy as np
from bjontegaard_metric import BD_RATE, BD_PSNR
from utils import split_dataframe, mean_dataframe
from plot import plot_curves


def update(df, df_stats):
    """calculate bpp according to the raw data (df) and the stats data
    """
    index_name='sequence'
    if df.index.name != index_name: 
        df.set_index(index_name, inplace=True)
    if df_stats.index.name != index_name: 
        df_stats.set_index(index_name, inplace=True)
    # add meta information like numInputPoints, PeakValue, etc.
    for stats_idx in  df_stats.columns:
        if stats_idx not in df.keys():
            print('add stats index', stats_idx)
            df[stats_idx] = [df_stats.loc[idx][stats_idx] for idx in df.index]

    # calculate bpp
    if 'bppGeo' not in df.keys() and 'numBitsGeoEncT' in df.keys():
        bppGeo = df['numBitsGeoEncT']/df['numInputPointsT']
        bppGeo = bppGeo.round(8)
        df['bppGeo'] = bppGeo

    if 'bppRgb' not in df.keys() and 'numBitsRgbEncT' in df.keys():
        bppRgb = df['numBitsRgbEncT']/df['numInputPointsT']
        bppRgb = bppRgb.round(8)
        df['bppRgb'] = bppRgb

    if 'bppRef' not in df.keys() and 'numBitsRefEncT' in df.keys():
        bppRef = df['numBitsRefEncT']/df['numInputPointsT']
        bppRef = bppRef.round(8)
        df['bppRef'] = bppRef

    if 'bppTotal' not in df.keys() and 'numBitsTotalDecT' in df.keys():
        bppTotal = df['numBitsTotalDecT']/df['numInputPointsT']
        bppTotal = bppTotal.round(8)
        df['bppTotal'] = bppTotal
    
    return df


def compare(df1, df2, xlabel, ylabel, seqs_name):
    """calculate BD-Rate, plot RD curve and save image to './figs'
    """
    # BD-Rate
    R1 = df1[xlabel]
    PSNR1 = df1[ylabel]
    R2 = df2[xlabel]
    PSNR2 = df2[ylabel]
    bdrate = BD_RATE(R1, PSNR1, R2, PSNR2, piecewise=0)
    bdrate = round(bdrate, 2)
    print('bdrate:\t', bdrate)

    # plot RD-curves
    data1 = {'name':'anchor', 'xlabel':xlabel, 'ylabel':ylabel, 
        'x':df1[xlabel], 'y':df1[ylabel]}
    data2 = {'name':'test', 'xlabel':xlabel, 'ylabel':ylabel, 
        'x':df2[xlabel], 'y':df2[ylabel]}
    figdir = os.path.join('figs', seqs_name+'_'+xlabel+'_'+ylabel+'_'+str(round(bdrate))+'.png')
    os.makedirs('figs', exist_ok=True)
    plot_curves([data1, data2], figdir=figdir)

    return 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--csvdir1", type=str, default='csvfiles/reporting_template_lossy.csv')
    parser.add_argument("--csvdir2", type=str, default='csvfiles/test.csv')
    parser.add_argument("--csvdir_stats", type=str, default='csvfiles/reporting_template_stats.csv')
    parser.add_argument("--xlabel", type=str, default='bppGeo')
    parser.add_argument("--ylabel", type=str, default='d1T')
    args = parser.parse_args()
    print('args:\n', args)

    # 1. update csvfile: (calculate bpp)
    df_stats = pd.read_csv(args.csvdir_stats)

    df1 = pd.read_csv(args.csvdir1)
    df1 = update(df1, df_stats)
    # df1.to_csv(args.csvdir1, index=True)

    df2 = pd.read_csv(args.csvdir2)
    df2 = update(df2, df_stats)
    # df2.to_csv(args.csvdir2, index=True)

    # 2. split concatenated frames to single frame for comparisons
    df1_set = split_dataframe(df1)
    df2_set = split_dataframe(df2)

    # 3. plot rd curves and bdrate for each sequence in csvdir2
    sequence_list = list(df2_set.keys())
    print(sequence_list)
    for _, seqs_name in enumerate(sequence_list):
        print('seqs_name:\t', seqs_name)
        df1_one = df1_set[seqs_name]
        df2_one = df2_set[seqs_name]
        # print(df1_one, '\n', df2_one)
        compare(df1_one, df2_one, args.xlabel, args.ylabel, seqs_name)
    

