import os
import glob
import pandas as pd


class my_data:

    def get_data(self):
        directory = self.get_dataset_location()
        all_files = glob.glob(directory + "/*.csv")

        df = pd.DataFrame()

        for filename in all_files:
            if filename.endswith(".csv"):
                f = open(filename, 'r')
                csv_file = pd.read_csv(filename, index_col=None, header=0)
                df = pd.concat([df, csv_file], axis=0)
                f.close()

        return df

    def get_current_dir(self):
        return os.getcwd()

    def get_dataset_location(self):
         return os.path.join(self.get_current_dir(), "src","treering","OpenData")

    def get_dataset_location2(self):
        return os.path.join(self.get_current_dir(), "src", "treering", "OpenData2")


    def get_data_for_cluster(self):
        directory = self.get_dataset_location2()
        all_files = glob.glob(directory + "/*.csv")

        df_c = pd.DataFrame()

        for filename in all_files:
            if filename.__contains__('data_clustered'):
                f = open(filename, 'r')
                csv_file = pd.read_csv(filename, index_col=None, header=0)
                df_c = pd.concat([df_c, csv_file], axis=0)
                f.close()

        return df_c

    def get_data_with_province(self):
        directory = self.get_dataset_location2()
        all_files = glob.glob(directory + "/*.csv")

        df_p = pd.DataFrame()

        for filename in all_files:
            if filename.__contains__('tree_ring_part'):
                f = open(filename, 'r')
                csv_file = pd.read_csv(filename, index_col=None, header=0)
                df_p = pd.concat([df_p, csv_file], axis=0)
                f.close()

        return df_p