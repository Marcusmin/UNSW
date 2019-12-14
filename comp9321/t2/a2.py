import pandas as pd
import numpy as np

def read_csv(file_name):
    return pd.read_csv(file_name)

def main():
    file_name = 'Books.csv'
    df = read_csv(file_name)
    df['Place of Publication'] = df['Place of Publication'].apply(lambda x: 'London' if 'London' in x else x.replace('-', ' '))
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    print(df['Date of Publication'])
if __name__ == '__main__':
    main()