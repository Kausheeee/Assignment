#!/usr/bin/env python
# coding: utf-8

# comment


import pandas as pd
from dateutil.relativedelta import relativedelta


# In[21]:


df = pd.read_csv('dataset-1.csv')


# In[4]:


df.head()


# In[5]:


def generate_car_matrix(df)->pd.DataFrame:
    result_df = df.pivot(index='id_1', columns='id_2', values='car')
    return result_df


# In[10]:


df_1 = generate_car_matrix(df)


# In[11]:


df_1.fillna(0,inplace=True)


# In[22]:


def get_type_count(df)->pd.DataFrame:
    conditions = [
    df['car'] <= 15,
    (df['car'] > 15) & (df['car'] <= 25),
    df['car'] > 25]
    values = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[0, 15, 25, df['car'].max()], labels=values)
    return df


# In[23]:


df_2 = get_type_count(df)


# In[24]:


df_2


# In[30]:


car_type_counts = df['car_type'].value_counts().to_dict()
sorted_car_type_counts = dict(sorted(car_type_counts.items()))


# In[31]:


sorted_car_type_counts


# In[41]:


def get_bus_indexes(df)->pd.DataFrame:
    mean_bus_value = df['bus'].mean()
    threshold = 2 * mean_bus_value
    filtered_df = df[df['bus'] > threshold]
    indices = filtered_df.index.tolist()
    indices.sort()
    return indices


# In[42]:


df_3 = get_bus_indexes(df)


# In[63]:


def filter_routes(df):
    average_truck_by_route = df.groupby('route')['truck'].mean()
    filtered_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()
    sorted_filtered_routes = sorted(filtered_routes)
    return sorted_filtered_routes


# In[64]:


df_4 = filter_routes(df)


# In[65]:


df_4


# In[67]:


df_1.head()


# In[71]:


def multiply_matrix(df):
    df = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    df = df.round(1)
    return df   


# In[72]:


df_5 = multiply_matrix(df_1)


# In[74]:


df_5.head()


# In[75]:


Df = pd.read_csv('Dataset-2.csv')


# In[78]:


Df[['id','name','id_2','startDay','startTime','endDay','endTime']].head()


# In[114]:


def time_check(df):
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')
    duration_correct = (df['end_datetime'] - df['start_datetime']).dt.total_seconds() == 24 * 3600
    day_span_correct = (df['end_datetime'].dt.dayofweek - df['start_datetime'].dt.dayofweek) == 6
    incorrect_timestamps = ~(duration_correct & day_span_correct)
    multi_index = pd.MultiIndex.from_frame(df[['id', 'id_2']])
    incorrect_timestamps = pd.Series(incorrect_timestamps.values, index=multi_index)
    return incorrect_timestamps


# In[115]:


df_6 = time_check(Df)


# In[116]:


df_6


# In[ ]:




