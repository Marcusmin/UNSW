import pandas as pd
import numpy as np

def read_csv(file_name):
    return pd.read_csv(file_name)

def drop_column(df_name, drop_list):
    return df_name.drop(columns = drop_list)

def calculate_null(df_name):
    return df_name.isna().sum()

def main():
    file_name = 'Books.csv'
    dataframe = read_csv(file_name)
    print(dataframe.shape)
    #print(dataframe.isna().sum())
    drop_list = ['Edition Statement',
        'Corporate Author',
        'Corporate Contributors',
        'Former owner',
        'Engraver',
        'Contributors',
        'Issuance type',
        'Shelfmarks'
    ]
    dropped = drop_column(dataframe, drop_list)
    for each in dropped.columns:
        print(each)
    null_sum = calculate_null(dataframe)
    #print(null_sum)
if __name__ == '__main__':
    main()