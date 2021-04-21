#import os
import pandas as pd
#import numpy as np
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
servprov_path = "D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/Data_Denver_Vaccination_Sites.xlsx"
serv_prov = pd.read_excel(servprov_path,sheet_name='Service Provider Sites')


## Dealing with Census Tract Geographic Information
fiona.open(shp_path)
denver_tracts = gpd.read_file(shp_path)
denver_tracts.reset_index(inplace=True)
centers = denver_tracts['geometry'].centroid # Get census tracts centroids


## Handle service providers
lat_long = serv_prov[['Lat','Long']].to_numpy()
geometry = [Point(xy) for xy in zip(serv_prov['Long'], serv_prov['Lat'])]
#crs = {'init': 'epsg:4326'} # In degrees
crs = {'init': 'epsg:3857'} # In meters
serv_lat_long = gpd.GeoDataFrame(serv_prov, crs = crs, geometry = geometry)

## Calculate distances between service providers and Tract centers
dist_mtx=serv_lat_long.geometry.apply(lambda x: centers.distance(x))
dist_mtx = dist_mtx.idxmin(axis=1)
min_dist=serv_lat_long.geometry.apply(lambda x: centers.distance(x).min())
dist_mtx=pd.concat([dist_mtx,min_dist],axis=1)
dist_mtx = pd.DataFrame(dist_mtx)
dist_mtx.columns.values[0] = "idx"


## Plot
ax = denver_tracts.plot(column='TTL_POPULA', cmap='PuRd', linewidth=0.8, edgecolor='black', figsize=(30, 18))
x, y = serv_prov['Long'].values, serv_prov['Lat'].values
ax.scatter(x,y, marker="o", color='b')
plt.show()