import pandas as pd 
import numpy as np 

def read_csv(csv_name):
    return pd.read_csv(csv_name)

def print_csv(csv_file, p_column = True, p_row = True):
    if p_column:
        print(",".join([column for column in csv_file]))
    if p_row:
        for index, row in dataframe.iterrows():
            print(",".join([str(row[column]) for column in csv_file]))


if __name__ == '__main__':
    csv_name = 'a.csv'
    '''
    step 1
        read the csv file
    '''
    dataframe = read_csv(csv_name)
    print(dataframe)
    '''
    step 2
        print column
        print row
    '''
    #print_csv(dataframe)
    #for index, row in dataframe.iterrows():
    #    print(index, row)