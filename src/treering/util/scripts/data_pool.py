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


