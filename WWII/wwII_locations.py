'''
 File Name: wwII_locations.py
 Description: Locations of Weather Stations during WWII
 Author: Willy Hagi
 E-mail: hagi.willy@gmail.com
 Github: /willyhagi
'''


## IMPORTING
import pandas as pd
import numpy as np 
import seaborn as sns
import geopandas as gp
import matplotlib.pyplot as plt 
from shapely.geometry import Point


## LOAD DATA
wwII = pd.read_csv('Weather Station Locations.csv')


## COORDINATES COLUMN AND GEODATAFRAME
wwII['Coordinates'] = list(zip(wwII['Longitude'], wwII['Latitude']))
wwII['Coordinates'] = wwII['Coordinates'].apply(Point)
geoframe = gp.GeoDataFrame(wwII, geometry='Coordinates')


## PLOT THE LOCATIONS
fig, ax1 = plt.subplots(figsize=(12,5))

ax1.set_aspect('equal')
world = gp.read_file(gp.datasets.get_path('naturalearth_lowres'))
world.plot(ax=ax1,color='white', edgecolor='black')
geoframe.plot(ax=ax1, color='blue', marker='o', markersize=15)

plt.title('WWII Weather Stations')

plt.tight_layout()
#plt.savefig('locations.png', dpi=300)
plt.show()


## GROUPING WEATHER STATIONS BY COUNTRY
by_country = wwII['NAME'].groupby(wwII['STATE/COUNTRY ID']).count()


## PLOT THE GROUPS
sns.set(style='ticks', context='talk')

plt.figure(figsize=(15,5))

sns.barplot(x=by_country.index, y=by_country, color='Blue')

plt.xlabel('State/Country ID')
plt.ylabel('Number of Stations')
plt.xticks(rotation=80)

plt.tight_layout()
#plt.savefig('stations_bycountry.png', dpi=300)
plt.show()


## PLOT PROBABILITY DENSITY FUNCTION AND HISTOGRAM
plt.figure(figsize=(10,5))

sns.distplot(by_country, color='Blue')

plt.xlabel('Number of Stations')
plt.ylabel('PDF')

plt.tight_layout()
#plt.savefig('pdf_stations.png', dpi=300)
plt.show()