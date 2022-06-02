import pandas as pd
import numpy as np


def split_dataframe(df, index_name='sequence', columns=None):
    """split the input dataframe into multiple dataframes by the index_name
    """
    df.set_index(index_name, inplace=True)
    indices = df.index.unique()
    df_set = {}
    for _, index in enumerate(indices):
        if columns is None: df_one = df.loc[index]
        else: df_one = df.loc[index][columns]
        df_set[index] = df_one
    
    return df_set


def mean_dataframe(df_list):
    """calculate the average value of input df_list
    """
    df_mean = pd.DataFrame()
    for index in df_list[0].columns:
        df_mean[index] = np.stack([df[index] for df in df_list]).mean(axis=0)
    
    return df_mean

