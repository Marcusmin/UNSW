import pandas as pd 
import numpy as np 

s = pd.Series([1,3,5, np.nan, 44, 1])
#print(s)

dates = pd.date_range('20190910', periods = 6)
#print(dates)

df = pd.DataFrame(np.arange(24).reshape(6,4),index=dates,columns=['a','b','c','d'])
#print(df)

df2 = pd.DataFrame({'A' : 1.,
                    'B' : pd.Timestamp('20130102'),
                    'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                    'D' : np.array([3] * 4,dtype='int32'),
                    'E' : pd.Categorical(["test","train","test","train"]),
                    'F' : 'foo'})
                    
#print(df2)
#print(df2.columns)
#print(df2.index)
#print(df2.values)

#select by location label
#print(df.loc['20190910'])
#print(df.loc['20190910', ['a']])

#select by index location
#print(df.iloc[3][2])
'''
df.iloc[1, 1] = np.nan
df.iloc[2, 2] = np.nan

print(df)
print(df.fillna((999)))

print(df.dropna(axis = 0, how='any')) #0 means row, 1 means column/// any all

'''
df1 = pd.DataFrame(np.ones((3,4))*0, columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1, columns=['a','b','c','d'])
df3 = pd.DataFrame(np.ones((3,4))*2, columns=['a','b','c','d'])

#concat0 纵 1 heng
res = pd.concat([df1, df2, df3], axis=0)
print(res)