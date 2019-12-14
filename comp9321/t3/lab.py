import matplotlib.pyplot as plt
import pandas as pd

def clean(df):
    # Let's Clean the data to get rid of exceptions
    df['Place of Publication'] = df['Place of Publication'].apply(
        lambda x: 'London' if 'London' in x else x.replace('-', ' '))
    return df

file_name = 'Books.csv'

df = pd.read_csv(file_name)
df = clean(df)
'''
print(df['Place of Publication'])
print('------------------count---------------\n')
print(df['Place of Publication'].value_counts())
'''

count = df['Place of Publication'].value_counts()
count.plot.pie(subplots=True)

file_name = 'iris.csv'
df = pd.read_csv(file_name)
df = df.groupby('species').mean()
#print(df)
df.plot.bar()

df = pd.read_csv(file_name)
df_s = df.query('species == "setosa"')
df_v1 = df.query('species == "versicolor"')
df_v2 = df.query('species == "virginica"')

fig, axes = plt.subplots(nrows=2, ncols=2)

ax = df_s.plot.scatter(x='sepal_length', y='sepal_width', label='setosa', ax = axes[0][0])
ax = df_v1.plot.scatter(x='sepal_length', y='sepal_width', color = 'red',label='setosa',ax = ax)
ax = df_v2.plot.scatter(x='sepal_length', y='sepal_width', color = 'green', label='setosa', ax = ax)

ax = df_s.plot.scatter(x='petal_length', y='petal_width', label='setosa',ax = axes[0][1])
ax = df_v1.plot.scatter(x='petal_length', y='petal_width', color = 'red',label='setosa',ax = ax)
ax = df_v2.plot.scatter(x='petal_length', y='petal_width', color = 'green', label='setosa', ax = ax)



plt.show()