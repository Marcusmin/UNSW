import sqlite3
import pandas as pd 
import numpy as np
from pandas.io import sql 


def read_csv(csv_name):
    return pd.read_csv(csv_name)

def make_sql(dataframe, database_file, table_name):
    cnx = sqlite3.connect(database_file)
    sql.to_sql(dataframe, name=table_name, con=cnx)

def read_sql(database_file, table_name):
    cnx = sqlite3.connect(database_file)
    return sql.read_sql('select * from ' + table_name, cnx)


if __name__ == '__main__':
    csv_name = 'a.csv'

    dataframe = read_csv(csv_name)
    database_file = 'a.db'
    table_name = 'a'
    #make_sql(dataframe, database_file, table_name)
    read_sql(database_file, table_name)
