# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 21:30:59 2019

@author: VIET
"""
import pandas as pd
import concurrent.futures
import os
#%% Create read and parse datetime function
def read_data(x):
    dateparse = lambda x: pd.datetime.strptime(x, '%Y %m %d %H %M %S')
    data = pd.read_csv('data/' + x, parse_dates = {'Time': ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']}, date_parser = dateparse)
    return data

datafiles = os.listdir('data/') # List all files in the data folder
csvfiles = [file for file in datafiles if file.endswith(".csv")]
#%% Multi-processing
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        each = executor.map(read_data, csvfiles)
        full = pd.concat([each.set_index('Time') for each in each], axis=1, join='inner').reset_index()
        full.to_csv('fulldata.csv', index = False)