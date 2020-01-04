#!/usr/bin/env python
# coding: utf-8

# # create data frames

# In[4]:


import pandas as pd


# In[6]:


columns = ['name', 'age', 'gender', 'job']

user1 = pd.DataFrame([['alice', 19, "F", "student"],
['john', 26, "M", "student"]],
columns=columns)

user2 = pd.DataFrame([['eric', 22, "M", "student"],
['paul', 58, "F", "manager"]],
columns=columns)

user3 = pd.DataFrame(dict(name=['peter', 'julie'],
age=[33, 44], gender=['M', 'F'],
job=['engineer', 'scientist']))
print(user1)
print(user2)
print(user3)


# # combining data frames

# In[7]:


user1.append(user2)
users = pd.concat([user1, user2, user3])
print(users)


# In[8]:


#Join DataFrame
user4 = pd.DataFrame(dict(name=['alice', 'john', 'eric', 'julie'],
height=[165, 180, 175, 171]))
print(user4)


# In[9]:


#Use intersection of keys from both frames
merge_inter = pd.merge(users, user4, on="name")
print(merge_inter)


# In[11]:


#Reshaping by pivoting
#“Unpivots” a DataFrame from wide format to long (stacked) format,
staked = pd.melt(users, id_vars="name", var_name="variable", value_name="value")
print(staked)


# In[12]:


# examine the users data
users # print the first 30 and last 30 rows
type(users) # DataFrame
users.head() # print the first 5 rows
users.tail() # print the last 5 rows
users.index # "the index" (aka "the labels")
users.columns # column names (which is "an index")
users.dtypes # data types of each column
users.shape # number of rows and columns
users.values # underlying numpy array
users.info() # concise summary (includes memory usage as of pandas 0.15.0)


# In[13]:


#Columns selection
users['gender'] # select one column
type(users['gender']) # Series
users.gender # select one column using the DataFrame
# select multiple columns
users[['age', 'gender']] # select two columns
my_cols = ['age', 'gender'] # or, create a list...
users[my_cols] # ...and use that list to select columns
type(users[my_cols]) # DataFrame


# # Rows selection (basic)
# iloc is strictly integer position based

# In[15]:



df = users.copy()
df.iloc[0] # first row
df.iloc[0, 0] # first item of first row
df.iloc[0, 0] = 55
for i in range(users.shape[0]):
 row = df.iloc[i]
 row.age *= 100  # setting a copy, and not the original frame data.
print(df) # df is not modified#


# In[19]:


#ix supports mixed integer and label based access.
df = users.copy()
df.ix[0] # first row
df.ix[0, "age"] # first item of first row
df.ix[0, "age"] = 55
for i in range(df.shape[0]):
  df.ix[i, "age"] *= 10
  print(df) # df is modified


# # Sorting

# In[20]:



df = users.copy()
df.age.sort_values() # only works for a Series
df.sort_values(by='age') # sort rows by a specific column
df.sort_values(by='age', ascending=False) # use descending order instead
df.sort_values(by=['job', 'age']) # sort by multiple columns
df.sort_values(by=['job', 'age'], inplace=True) # modify df
print(df)


# # Descriptive statistics

# In[21]:


print (df.describe())


# In[22]:


print(df.describe(include='all'))


# In[23]:


print(df.groupby("job").mean()) #group by job mean


# # Quality check
# Remove duplicate data

# In[24]:



df = users.append(df.iloc[0], ignore_index=True)
print(df.duplicated()) # Series of booleans
# (True if a row is identical to a previous row)

df.duplicated().sum() # count of duplicates
df[df.duplicated()] # only show duplicates
df.age.duplicated() # check a single column for duplicates
df.duplicated(['age', 'gender']).sum() # specify columns for finding duplicates
df = df.drop_duplicates() # drop duplicate rows


# In[25]:


# find missing values in a DataFrame
df.isnull() # DataFrame of booleans
df.isnull().sum() # calculate the sum of each column


# In[27]:


#Strategy 1: drop missing values
df.dropna() # drop a row if ANY values are missing
df.dropna(how='all') # drop a row only if ALL values are missing


# In[28]:


#Strategy 2: fill in missing values
df.height.mean()
df = users.copy()
df.ix[df.height.isnull(), "height"] = df["height"].mean()
print(df)


# In[32]:


import numpy as np
#Dealing with outliers
size = pd.Series(np.random.normal(loc=175, size=20, scale=10))
# Corrupt the first 3 measures
size[:3] += 500
print(df)


# # File I/O
# csv

# In[35]:



import tempfile, os.path
tmpdir = tempfile.gettempdir()
csv_filename = os.path.join(tmpdir, "users.csv")
users.to_csv(csv_filename, index=False)
other = pd.read_csv(csv_filename)
#Read csv from url
url = 'https://raw.github.com/neurospin/pystatsml/master/data/salary_table.csv'
salary = pd.read_csv(url)
#Excel
xls_filename = os.path.join(tmpdir, "users.xlsx")
users.to_excel(xls_filename, sheet_name='users', index=False)
pd.read_excel(xls_filename, sheetname='users')
# Multiple sheets
with pd.ExcelWriter(xls_filename) as writer:
users.to_excel(writer, sheet_name='users', index=False)
df.to_excel(writer, sheet_name='salary', index=False)
pd.read_excel(xls_filename, sheetname='users')
pd.read_excel(xls_filename, sheetname='salary')


# In[ ]:




