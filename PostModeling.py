#import os
import pandas as pd
import numpy as np
# Plotting packages
import matplotlib.pyplot as plt
#import matplotlib.lines as mlines
#from matplotlib.colors import ListedColormap
#import seaborn as sns
# Geospatial packages
import geopandas as gpd
import fiona 
from shapely.geometry import Point # Shapely for converting latitude/longtitude to geometry
#from shapely.wkt import loads as load_wkt # Get centroids from shapely file

## Read in data
shp_path = "D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/shp_data/american_community_survey_tracts_2015_2019.shp"
mod_path = "D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/Final Problem Solutions.xlsx"
mod = pd.read_excel(mod_path,sheet_name='TRACTS')

fiona.open(shp_path)
denver_tracts = gpd.read_file(shp_path)
denver_tracts.reset_index(inplace=True)


servprov_path = "D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/Data_Denver_Vaccination_Sites.xlsx"
serv_prov = pd.read_excel(servprov_path,sheet_name='Service Provider Sites')



## Handle service providers
lat_long = serv_prov[['Lat','Long']].to_numpy()
geometry = [Point(xy) for xy in zip(serv_prov['Long'], serv_prov['Lat'])]
#crs = {'init': 'epsg:4326'} # In degrees
crs = {'init': 'epsg:3857'} # In meters
serv_lat_long = gpd.GeoDataFrame(serv_prov, crs = crs, geometry = geometry)


mod['GEO_NAME'] = denver_tracts['GEO_NAME'] # save me later

denver_tracts['social_metric'] = mod['SVI']
denver_tracts['Perc Vac iter'] = mod['Perc Vac iter']
denver_tracts['Perc Vac Full'] = mod['Perc Vac Full']

#Nice pink: PuRd
plt.rcParams['axes.titlesize'] = 50
ax = denver_tracts.plot(column='social_metric', cmap='Blues', linewidth=0.8, edgecolor='black', figsize=(30, 18))
x, y = serv_prov['Long'].values, serv_prov['Lat'].values
ax.scatter(x,y, marker="o", color='r')
plt.title('SVI Metric')
plt.show()

ax = denver_tracts.plot(column='Perc Vac Full', cmap='Blues', linewidth=0.8, edgecolor='black', figsize=(30, 18))
x, y = serv_prov['Long'].values, serv_prov['Lat'].values
ax.scatter(x,y, marker="o", color='r')
plt.title('One batch distribution')
plt.show()

ax = denver_tracts.plot(column='Perc Vac iter', cmap='Blues', linewidth=0.8, edgecolor='black', figsize=(30, 18))
x, y = serv_prov['Long'].values, serv_prov['Lat'].values
ax.scatter(x,y, marker="o", color='r')
plt.title('Multi-batch distribution')
plt.show()