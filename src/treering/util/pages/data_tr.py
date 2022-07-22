import os
import glob
import pandas as pd
import numpy as np


def get_current_dir():
    return os.getcwd()


def get_dataset_location():
    return os.path.join(get_current_dir(),"OpenData")


def get_data():
    directory = '../../OpenData' #get_dataset_location()
    all_files = glob.glob(directory + "/*.csv")

    df = pd.DataFrame()

    for filename in all_files:
        if filename.endswith(".csv"):
            f = open(filename, 'r')
            csv_file = pd.read_csv(filename, index_col=None, header=0)
            df = pd.concat([df, csv_file], axis=0)
            f.close()

    df.rename(columns={'res.Lbai.normalized': 'growth_index'}, inplace=True)
    df.drop(["uid_tree", "uid_radius", "SummerSMI", "SummerSMI.t_1", "Ecoregions"], axis=1, inplace=True)
    df = df.groupby(['year'], as_index=False)['growth_index'].mean()
    #df = df.pivot(index='species', columns='year', values='growth_index')
    df = df.replace(np.nan, 0)
    df.columns = df.columns.astype(str)
    return df


df = get_data()
data = df
data = data.T.reset_index()
#data = pd.melt(data, id_vars=["year"]).rename(columns={"index": "year", "value": "growth_index"})

print(df)