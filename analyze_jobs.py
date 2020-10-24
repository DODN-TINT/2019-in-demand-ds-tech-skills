# Run the analysis off the files separate session

# # Analysis 

# Import necessary libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
import collections

from IPython.core.display import display, HTML
from sklearn.preprocessing import MinMaxScaler
    
# import plotly 
import plotly
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.offline as py
import plotly.tools as tls

# for color scales in plotly
# import colorlover as cl 

# predefine format of display to have , delimiter and 2 decimal places
pd.options.display.float_format = '{:,.2f}'.format  
pd.options.display.max_columns = 999

# review these magic tricks later - autoreload and matplotlib inline commands are familiar
py.init_notebook_mode(connected=True)
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# Total listings with 'Data Scientist' for Indeed, Monster, and SimplyHired
job_file = "Data Scientist_United States_2020-10-21.csv"


#  Make sure to specify which column in csv file to use as index  !!!!
df = pd.read_csv(job_file,index_col=0)
total_ds_jobs = list(df.iloc[0])
total_ds_jobs


# ### These are the totals for 10/20/2020 for "Data Scientist" alone:
# #### These are the entries for each skill term='' searching on each website
# Data Scientist	4343, 2340, 3248

df = df.drop('Data Scientist')
df = df.fillna(0)
percent_df = df/total_ds_jobs
percent_df['avg'] = percent_df.mean(axis=1)
percent_df


# # 2018 data
# 
# Total listings for "data scientist" for these three sites. I took this data from a .csv file where I put in the results by hand in 2018. It's available at [Kaggle](https://www.kaggle.com/discdiver/the-most-in-demand-skills-for-data-scientists/data).

# In[24]:


total_2018 = {
    'Indeed': 5138,
    'SimplyHired': 3829,
    'Monster': 3746,
}


# values

# In[25]:


# find this file?
# df_2018 = pd.read_csv('ds_job_listing_software.csv')


# In[26]:


df_2018.index = df_2018['Keyword']
df_2018


# In[27]:


df_2018_s = df_2018.iloc[:37, 2:5]
df_2018_s


# In[28]:


df_2018_s = df_2018_s.apply(lambda x:x.str.replace(',', '').astype(float), axis=1)
df_2018_s.head()


# In[29]:


df_2018_percent = df_2018_s/total_2018
df_2018_percent


# ### Make the average for 2018.

# In[30]:


df_2018_percent['avg'] = df_2018_percent.mean(axis=1)
df_2018_percent


# ## Merge the 2018 and 2019 DataFrames for Analysis

# In[31]:


df_combo = df_2018_percent.merge(percent_df, left_index=True, right_index=True, how='outer')
df_combo


# In[32]:


df_combo = df_combo.loc[:, ['avg_x', 'avg_y']]
df_combo.columns=['2018', '2019']


# In[33]:


df_combo = df_combo.sort_values(by='2019', ascending=False)
df_combo


# ### Combine two versions of NumPy and C#

# In[34]:


df_combo.loc["NumPy", "2018"] = df_combo.loc['Numpy', '2018']
df_combo.drop('Numpy')


# In[55]:


df_combo.loc["C#", "2018"] = df_combo.loc['C# ', '2018']
df_combo.drop('C# ')
df_combo


# Strange, might be a white space with issue the second C#. Oh well, it won't get included here in a second anyway.

# ### Top 20

# In[56]:


df_20 = df_combo.iloc[:20]
df_20


# In[57]:


df_20.plot(kind='bar')


# In[58]:


df_2019 = df_20['2019']
df_2019.plot(kind='bar')


# In[59]:


df_2018_sorted = df_20['2018'].sort_values(ascending=False)
df_2018_sorted.plot(kind='bar')


# # Let's make pretty, interactive charts in Plotly!

# In[60]:


cmax=200
cmin=50
color_s = np.linspace(cmin, cmax, 20)

data = [
    go.Bar(
        x=df_20.index,          
        y=df_20['2019']*100,
        marker=dict(
            colorscale='Jet',
            color=color_s
        ),
    )
]

layout = {
     'title': 'Technologies in Data Scientist Job Listings 2019',
    'yaxis': {'title': 'Avg % of Listings', },
    'xaxis': {'title': "Technology", 'tickmode': 'linear'},
    'title_x':0.5,
    'height': 500
    
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# ## Top 15

# In[108]:


df_15 = df_combo.iloc[:15]
df_15


# In[112]:


cmax=200
cmin=50
color_s = np.linspace(cmin, cmax, 15)

data = [
    go.Bar(
        x=df_15.index,          
        y=df_15['2019']*100,
        marker=dict(
            colorscale='Jet',
            color=color_s
        ),
    )
]

layout = {
     'title': 'Technologies in Data Scientist Job Listings 2019',
    'yaxis': {'title': 'Avg % of Listings', },
    'xaxis': {'title': "Technology", 'tickmode': 'linear'},
    'title_x':0.5,
    'height': 500
    
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# # Looking at just the top 10 for 2019
# 

# In[61]:


df_10 = df_combo.iloc[:10]
df_10


# In[62]:


df_10.plot(kind='bar', title='Most In Demand Data Science Tech Skills')


# In[63]:


df_10 = df_10.sort_values(by='2019')


# In[64]:


cmax=50
cmin=200
color_s = np.linspace(cmin, cmax, 10)

data = [
    go.Bar(
        y=df_10.index,          
        x=df_10['2019'] * 100,
        orientation='h',
        marker=dict(
            colorscale='Jet',
            color=color_s
        ),
    )
]

layout = {
    'title': 'Technologies in Data Scientist Job Listings 2019',
    'yaxis': {'title': 'Software', 'tickmode': 'linear'},
    'xaxis': {'title': "Avg % of Listings"},
    'title_x':0.5,
    'height': 500
    
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# # Bigger DF with at least 5% of listings average in 2019

# In[65]:


df_over_five = df_combo[df_combo['2019']>=.05]
df_over_five


# In[ ]:





# ## 2018 Averages Chart

# In[76]:


df_over_five_g = df_over_five.sort_values(by='2018', ascending=True)


# In[78]:


cmax=50
cmin=200
color_s = np.linspace(cmin, cmax, 30)

data = [
    go.Bar(
        y=df_over_five_g.index,          
        x=df_over_five_g['2018']*100,
        orientation='h',
        marker=dict(
            colorscale='Jet',
            color=color_s
        ),
    )
]

layout = {
    'title': 'Technologies in Data Scientist Job Listings 2018',
    'xaxis': {'title': 'Avg % of Listings', },
    'yaxis': {'tickmode': 'linear'},
    'title_x':0.5,
    'height': 700
    
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# ## 2019 Averages Chart

# In[66]:


df_over_five_g = df_over_five.sort_values(by='2019', ascending=True)


# In[67]:


cmax=50
cmin=200
color_s = np.linspace(cmin, cmax, 30)

data = [
    go.Bar(
        y=df_over_five_g.index,          
        x=df_over_five_g['2019']*100,
        orientation='h',
        marker=dict(
            colorscale='Jet',
            color=color_s
        ),
    )
]

layout = {
    'title': 'Technologies in Data Scientist Job Listings 2019',
    'xaxis': {'title': 'Avg % of Listings', },
    'yaxis': {'tickmode': 'linear'},
    'title_x':0.5,
    'height': 700
    
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# ## Compute % change

# In[68]:


df_over_five_changes = df_over_five.copy()
df_over_five_changes['Change in Avg'] = df_over_five_changes['2019'] - df_over_five_changes['2018']
df_over_five_changes =  df_over_five_changes.sort_values(by = 'Change in Avg', ascending=False)
df_over_five_changes


# In[69]:


pct_change = df_over_five.pct_change(axis=1).sort_values(by='2019', ascending=True) 
pct_change


# In[70]:


pct_change = pct_change.drop('2018', axis=1)
pct_change.columns = ['% Change']
pct_change


# ## DataFrame for medium article

# In[71]:


df_over_five_all = df_over_five_changes.merge(pct_change, right_index=True, left_index=True)
df_over_five_all = df_over_five_all * 100
df_over_five_all.index.name = 'Keyword'


# In[92]:


df_over_five_all


# ## Change in avg from 2018 to 2019

# In[72]:


df_over_five_all_c = df_over_five_all.sort_values(by='Change in Avg', ascending=True)


# In[73]:


cmax=50
cmin=200
color_s = np.linspace(cmin, cmax, 30)

data = [
    go.Bar(
        y=df_over_five_all_c.index,          
        x=df_over_five_all_c['Change in Avg'],
        orientation='h',
        marker=dict(
            colorscale='Jet',
            #cauto=True,
            color=color_s
        ),
        
        
        # text=p_s_df['Score'],
        # textposition='outside',
        # textfont=dict(size=10)
    )
]

layout = {
    'title': 'Change in Avg % of Technologies in Data Scientist Job Listings 2019',
    'xaxis': {'title': 'Change in Avg %', 'tickmode': 'linear'},

    'title_x':0.5,
    'height': 700
    
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# # Percent change

# In[74]:


df_over_five_all_c = df_over_five_all.sort_values(by='% Change', ascending=True)


# In[75]:


cmax=50
cmin=200
color_s = np.linspace(cmin, cmax, 30)

data = [
    go.Bar(  
        y=df_over_five_all_c.index,          
        x=df_over_five_all_c['% Change'],
        orientation='h',
        marker=dict(
            colorscale='Jet',
            #cauto=True,
            color=color_s
        ),
    )
]

layout = {
    'title': '% Change in Technologies in Data Scientist Job Listings 2018 to 2019',
    'yaxis': {'tickmode': 'linear'},
    'xaxis': {'title': "% Change"},
    'title_x':0.5,
    'height': 700
}

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# In[79]:


df_over_five


# In[81]:


df_over_five['2019_rank']=df_over_five['2019'].rank(ascending=False)
df_over_five


# In[82]:


df_over_five['2018_rank']=df_over_five['2018'].rank(ascending=False)
df_over_five


# In[84]:


df_over_five['rank_change'] = df_over_five['2018_rank'] - df_over_five['2019_rank']
df_over_five


# ## Add rank to the table for article

# In[91]:


type(df_to_print)


# In[93]:


df_to_print = df_over_five_all.merge(df_over_five, left_index=True, right_index=True)


# In[97]:


df_to_print = df_to_print.drop(['2018_y', '2019_y'],  axis = 'columns')
df_to_print


# In[ ]:



# In[99]:


df_to_print.columns = ['2018 Avg', '2019 Avg', 'Change in Avg', '% Change', '2019 Rank', '2018 Rank', 'Rank Change']
df_to_print


# Reorder 2018 and 2019 rank columns

# In[101]:


new_cols = ['2018 Avg', '2019 Avg', 'Change in Avg', '% Change', '2018 Rank', '2019 Rank', 'Rank Change']


# In[104]:


df_to_print = df_to_print[new_cols]
df_to_print = df_to_print.sort_values(by='% Change', ascending=False)
df_to_print


# In[106]:


df_to_print.rename(index={'Matlab':'MATLAB'},inplace=True)


# In[107]:


df_to_print.style.format("{:,.1f}")


# # The end!

# In[ ]:

