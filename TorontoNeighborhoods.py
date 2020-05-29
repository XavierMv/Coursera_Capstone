#!/usr/bin/env python
# coding: utf-8

# # Neighborhoods in Toronto

# In[1]:


import pandas as pd 
import numpy as np
import requests 
import csv
from bs4 import BeautifulSoup
import matplotlib.cm as cm
import matplotlib.colors as colors
from sklearn.cluster import KMeans
import folium


# In[2]:


source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text


# In[3]:


s = BeautifulSoup(source, 'lxml')


# In[4]:


table = s.find_all('table')[0]


# In[5]:


df = pd.read_html(str(table), header=0)


# In[6]:


df1 = df[0]


# In[7]:


df1.columns = ['PostalCode', 'Borough', 'Neighborhood']


# In[8]:


df1 = df1[df1['Borough'] != 'Not assigned']


# In[9]:


df1['Neighborhood'] = np.where(df1['Neighborhood'] == 'Not assigned', df1['Borough'], df1['Neighborhood'])


# In[10]:


group = df1.groupby(['PostalCode', 'Borough'])['Neighborhood'].apply(lambda x: ', '.join(x))


# In[11]:


group.reset_index()


# In[12]:


dfn = pd.DataFrame(group)
dfn1 = dfn.reset_index()
dfn1.head()


# In[13]:


from geopy.geocoders import Nominatim


# In[14]:


coordinates = pd.read_csv("Geospatial_Coordinates.csv")
coordinates.head()


# In[15]:


coordinates.rename(columns={"Postal Code": "PostalCode"}, inplace=True)
coordinates.head()


# In[16]:


dfcor = df1.merge(coordinates, on="PostalCode", how="left")
dfcor.head()


# In[17]:


print('The dataframe has {} boroughs and {} neighborhoods.'.format(
        len(dfcor['Borough'].unique()),
        dfcor.shape[0]
    )
)


# In[18]:


address = 'Toronto, ON'

geolocator = Nominatim(user_agent="to_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[19]:


map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(dfcor['Latitude'], dfcor['Longitude'], dfcor['Borough'], dfcor['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
    
map_toronto

