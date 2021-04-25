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
dist_mtx_all = serv_lat_long.geometry.apply(lambda x: centers.distance(x))
dist_mtx = dist_mtx_all.idxmin(axis=1)
min_dist=serv_lat_long.geometry.apply(lambda x: centers.distance(x).min())
dist_mtx=pd.concat([dist_mtx,min_dist],axis=1)
dist_mtx = pd.DataFrame(dist_mtx)
dist_mtx.columns.values[0] = "idx"


## Plot
#Nice pink: PuRd
ax = denver_tracts.plot(column='TTL_POPULA', cmap='Blues', linewidth=0.8, edgecolor='black', figsize=(30, 18))
x, y = serv_prov['Long'].values, serv_prov['Lat'].values
ax.scatter(x,y, marker="o", color='r')
plt.show()

## Condense data for AMPL execution

cols_tract = ['STFID', 'STFID_NUM', 'TRACTCE10','GEO_NAME', 'TTL_POPULA','PCT_BLACK']
tract_data = denver_tracts[cols_tract]
cols_tract_name = tract_data.GEO_NAME
rows_serviceprov_name = serv_prov.Name
d_ij_matrix = dist_mtx_all.rename(columns = cols_tract_name, inplace = False)
d_ij_matrix = d_ij_matrix.rename(index=rows_serviceprov_name)

tract_data.to_csv('D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/tract_data.csv')
d_ij_matrix.to_csv('D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/d_ij.csv')

## Handle the d_ij multiplication
d_ij_matrix2 = pd.read_csv('D:/Sandy Oaks/Documents/Grad School/S21_MATH-7594/Project/COVIDvaccineAllocationIP2021/d_ij.csv')
idx_pharmacy = np.array([24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,42,43,44,45,46,47,48,49,50,51])
for count in d_ij_matrix.columns:
    pct_black = denver_tracts[denver_tracts['GEO_NAME'] == count]['PCT_BLACK']
    for count1 in idx_pharmacy:
        new_val = d_ij_matrix2.loc[count1,count]*(1+int(pct_black))
        d_ij_matrix2.loc[count1,count] = new_val
#end

d_ij_matrix2[count].iloc[[count1]].to_numpy()[0]*(1+int(pct_black))

d_ij_matrix2[count].iloc[[0]].to_numpy()[0]*(1+int(pct_black)) #0.092444144
#0.554664864

d_ij_matrix2.loc[0,count]*(1+int(pct_black))
#= 0.554664864
