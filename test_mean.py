"""
Input:
two .csv files which include the raw data for comparison.
Output:
BD-Rate difference; RD curve
"""

import os, argparse
import pandas as pd
import numpy as np
from utils import split_dataframe, mean_dataframe
from test import update, compare



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--csvdir1", type=str, default='csvfiles/reporting_template_lossy.csv')
    parser.add_argument("--csvdir2", type=str, default='csvfiles/test.csv')
    parser.add_argument("--csvdir_stats", type=str, default='csvfiles/reporting_template_stats.csv')
    parser.add_argument("--category", type=str, default='solid')
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

    # 3
    solid_list = ['queen_0200', 
                'soldier_vox10_0690', 
                'dancer_vox11_00000001', 
                'thaidancer_viewdep_vox12',
                'facade_00064_vox11']

    dense_list = ['soldier_viewdep_vox12', 
                'boxer_viewdep_vox12', 
                'facade_00009_vox12', 
                'house_without_roof_00057_vox12',
                'landscape_00014_vox14',
                'facade_00064_vox14']

    sparse_list = ['arco_valentino_dense_vox12', 
                    'staue_klimt_vox12', 
                    'shiva_00035_vox12', 
                    'egyptian_mask_vox12',
                    'ulb_unicorn_vox13',
                    'ulb_unicorn_hires_vox15',
                    'stanford_area_2_vox16',
                    'stanford_area_4_vox16']

    am_fused_list = ['citytunnel_q1mm', 
                    'overpass_q1mm', 
                    'tollbooth_q1mm']

    am_frame_list = ['ford_02_q1mm', 
                    'ford_03_q1mm',
                    'qnxadas-junction-approach',
                    'qnxadas-junction-exit',
                    'qnxadas-motorway-join',
                    'qnxadas-navigating-bends']

    if args.category=='solid': sequence_list = solid_list
    if args.category=='dense': sequence_list = dense_list
    if args.category=='sparse': sequence_list = sparse_list
    if args.category=='am_fused': sequence_list = am_fused_list
    if args.category=='am_frame': sequence_list = am_frame_list

    sequence_list = [seqs_name for seqs_name in sequence_list if seqs_name in df2_set.keys()]
    print('average results of sequence_list', sequence_list)
    
    if len(sequence_list) > 0:
        df1_list = [df1_set[seqs_name] for seqs_name in sequence_list]
        df2_list = [df2_set[seqs_name] for seqs_name in sequence_list]

        df1_mean = mean_dataframe(df1_list)
        df2_mean = mean_dataframe(df2_list)
        # print('df1_mean\n', df1_mean)
        # print('df2_mean\n', df2_mean)

        compare(df1_mean, df2_mean, args.xlabel, args.ylabel, 'mean')
