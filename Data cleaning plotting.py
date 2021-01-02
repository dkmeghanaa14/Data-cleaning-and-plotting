import pandas as pd
import numpy as np
import datetime
import geopandas as gpd
import geoplot
import geopy
from geopy.geocoders import Nominatim
from geopy.point import Point
from geopy.extra.rate_limiter import RateLimiter
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt 
import plotly_express as px

#Reading CSV file of data regarding the Port of Entry at the US borders
url = "C:\\Users\\UmaDevi\\Desktop\\Meghna\\Datasets\\Border_Crossing_Entry_Data.csv"
df = pd.read_csv(url)

# Renaming columns to a meaningful and understandable names
df.rename(columns = {'Timestamp':'Date','Measure':'Transport_Type', 'Value':'Persons'}, inplace = True)


#Inserting a Unique ID to the dataset
df.insert(0, 'Record_ID', range(1, 1+len(df)))

# Converting the timestamp to date type by just retrieving the date
df['Date'] = pd.to_datetime(df['Date'])

# Retrieving year for insights
df['Year'] = df['Date'].dt.year

#df['Month'] = df['Date'].dt.month
#df['Day'] = df['Date'].dt.day

# Splitting the geopoint to Latitude and Logitude separately
df['Location1'] = df['Location'].str.strip('POINT (' + ')')
lat = []
lon = []
for val in df['Location1']:
    lat.append(val.split(' ')[1])
    lon.append(val.split(' ')[0])

#Converting the latitude and longitude to float type from string type
for i in range(0, len(lat)):
    lat[i] = float(lat[i])
for i in range(0, len(lon)):
    lon[i] = float(lon[i])

# Assigning latitude and longitude to columns in the dataframe
df['Latitude'] = lat
df['Longitude'] = lon

#Assigning Minimum and Maximum of Latitutes and Longitudes to a set
BBox = (df.Longitude.min(), df.Longitude.max(), df.Latitude.min(), df.Latitude.max())

#Reading map image from local folder and setting map size and axes limits
rmap = plt.imread("C:\\Users\\UmaDevi\\Desktop\\Meghna\\Datasets\\map.png")
fig, ax = plt.subplots(figsize = (30, 45))
ax.scatter(df.Longitude, df.Latitude, zorder=1, alpha = 0.2, c='b', s=10)
ax.set_title('Plotting spatial data on the US border map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
#Plotting map
ax.imshow(rmap, zorder=0, extent=BBox, aspect='auto')


#Splitting the original dataframe to two different dataframes as same column has different type of inputs: Count of Persons and Count of Vehicles
df1 = df.loc[df.Transport_Type.str.contains('Passengers|Pedestrians')]

df2 = df.loc[~df.Transport_Type.str.contains('Passengers|Pedestrians')]
#Renaming the dataframe column from Persons to number of vehicles
df2.rename(columns = {'Persons':'Number_of_vehicles'}, inplace = True)

# Read from geopandas to get the base map
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

#Dataframe to show the 
plotdf = df.groupby(['Border', 'Transport_Type'], as_index=False)['Persons'].sum()
print(plotdf[0:5])

#Correlation between Border and Number of vehicles entered
df2.groupby(['Border', 'Transport_Type'])['Number_of_vehicles'].size().unstack().plot(kind = 'bar', stacked = True, ylim=(0,200000))
plt.title('Number of Vehicles crossed at each border')
plt.show()

#Correlation Between Border and Persons entered
df1.groupby(['Border', 'Transport_Type'])['Persons'].size().unstack().plot(kind = 'bar', stacked = False, ylim=(0,250000))
plt.title('Number of Persons crossed at each border')
plt.show()

#Correlation Between Border and Transport Type used for crossing the border
df5 = df1.groupby(['Transport_Type', 'Border']).count()['Persons'] 
df5.unstack().plot() 
plt.xticks(rotation=45)
plt.title('Number of persons crossed at each border using respective transport types') 
plt.show()
