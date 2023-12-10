#!/usr/bin/env python
# coding: utf-8

# In[41]:


import pandas as pd
from datetime import time


# In[2]:


df = pd.read_csv('Dataset-3.csv')


# In[3]:


df.head()


# In[4]:


def calculate_distance_matrix(df):
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids).fillna(0)
    
    for index, row in df.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.loc[id_start, id_end] += distance


    distance_matrix = distance_matrix + distance_matrix.T - distance_matrix.multiply(distance_matrix.T)

    return distance_matrix


# In[5]:


df_1 = calculate_distance_matrix(df)


# In[7]:


df_1.head()


# In[8]:


def unroll_distance_matrix(df):
    id_starts = []
    id_ends = []
    distances = []

    for id_start, row in df.iterrows():
        for id_end, distance in row.items():
            if id_start != id_end:
                id_starts.append(id_start)
                id_ends.append(id_end)
                distances.append(distance)

    unrolled_df = pd.DataFrame({'id_start': id_starts, 'id_end': id_ends, 'distance': distances})

    return unrolled_df


# In[9]:


df_2 = unroll_distance_matrix(df_1)


# In[14]:


df_2.head()


# In[36]:


def find_ids_within_ten_percentage_threshold(df, reference_value):
  filtered_df = df[df['id_start'] == reference_value]
  average_distance = filtered_df['distance'].mean()
  threshold = average_distance * 0.1
  filtered_ids = df[(df['id_start'] >= (reference_value - threshold)) & (df['id_start'] <= (reference_value + threshold))]['id_start'].tolist()
  return sorted(filtered_ids)


# In[37]:


df_3 = find_ids_within_ten_percentage_threshold(df_2,1001400)


# In[38]:


df_3[:5]


# In[26]:


def calculate_toll_rate(df):
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    for vehicle_type, rate in rate_coefficients.items():
        df[vehicle_type] = df['distance'] * rate

    return df


# In[27]:


df_4 = calculate_toll_rate(df_2)


# In[28]:


df_4.head()


# In[42]:


def calculate_time_based_toll_rates(df):
    weekday_discount_factors = {
        (time(0, 0), time(10, 0)): 0.8,
        (time(10, 0), time(18, 0)): 1.2,
        (time(18, 0), time(23, 59, 59)): 0.8
    }
    weekend_discount_factor = 0.7
    
    df['start_day'] = df['startDay'].str.capitalize()
    df['end_day'] = df['endDay'].str.capitalize()
    df['start_time'] = pd.to_datetime(df['startTime']).dt.time
    df['end_time'] = pd.to_datetime(df['endTime']).dt.time

    for time_range, discount_factor in weekday_discount_factors.items():
        weekday_condition = (df['start_time'] >= time_range[0]) & (df['end_time'] <= time_range[1]) & (df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']))
        df.loc[weekday_condition, ['car1', 'car2', 'car3']] *= discount_factor

    weekend_condition = df['start_day'].isin(['Saturday', 'Sunday'])
    df.loc[weekend_condition, ['car1', 'car2', 'car3']] *= weekend_discount_factor

    return df


# In[ ]:


df_5 = calculate_time_based_toll_rates(df_3)

