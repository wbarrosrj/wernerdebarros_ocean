# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 09:54:45 2020

@author: Werner
"""
#BIBLIOTECAS


from netCDF4 import Dataset, num2date, date2num
import matplotlib.ticker as mticker
#
import matplotlib.pyplot as plt
import numpy as np
import cartopy
import cartopy.crs as ccrs
#from cartopy.io import shapereader as shpreader
from cartopy.io import shapereader #SERVE PARA LER ARQYUIVOS SHAPEFILES, DO IBGE, INDIE, ANP, ANA


#diretorio = "E:\\AECO\\MAPA DE VENTO\\dados\\era5_teste_quiver3.nc" #CHAMANDO DIRETORIO
#diretorio = "E:\\AECO\\MAPA DE VENTO\\dados\\era5_teste_quiver4_RJ.nc"
diretorio = "E:\\AECO\\MAPA DE VENTO\\dados\\CERSAT-GLO-BLENDED_WIND_L4-V6-OBS_FULL_TIME_SERIE_1611341478239.nc" #WIND_GLO_WIND_L4_NRT_OBSERVATIONS_012_004

data = Dataset(diretorio, mode='r')
print(data)

#longitude e latitude 
#lon  = data.variables['longitude'][:] #ERA
#lat  = data.variables['latitude'][:] #ERA
#
lon  = data.variables['lon'][:] #CMEMS
lat  = data.variables['lat'][:] #CMEMS

#Ventos
#u10 = data.variables['u10'][:] #ERA
#v10 = data.variables['v10'][:] #ERA

u10 = data.variables['northward_wind'][:] #CMEMS
v10 = data.variables['eastward_wind'][:] #CMEMS

##
#t2m = data.variables['t2m'][:]

#Tempo
tempo = data.variables['time'][:]
tempo_units = data.variables['time'].units
tempo2 = num2date(tempo[:],units=tempo_units) #Convertendo

#CALCULANDO A VELOCIDADE A PARTIR DOS DADOS DO ERA
ws = np.sqrt((u10**2)+(v10**2))
#CALCULANDO A DIREÇÃO DO VENTO EM RADIANO
ws_dir = np.arctan2(u10,v10)
#LEMBRANDO QUE SÃO DADOS DIARIOS
ws_daily = np.nanmean(ws,axis=0)
##
# Plot windspeed média
plt.contourf(lon, lat, ws_daily)

##
LON, LAT = np.meshgrid(lon,lat)
x,y = (LON, LAT)

#ACHANDO O ARQUIVO SHAPEFILE
lendo_arquivo2 = 'C:/Users/Werner/Downloads/Curso2/br_unidades_da_federacao/BR_UF_2019.shp'

abrindo_arquivo2 = list(shapereader.Reader(lendo_arquivo2).geometries())

##
plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())#ELA PROJETA O MERCATOR
ax.add_geometries(abrindo_arquivo2, ccrs.PlateCarree(),edgecolor='black',facecolor='gray',alpha=0.8)
levels = np.linspace(1,12,10)
tt = plt.contourf(x,y,ws[0,:,:],cmap='jet',levels=levels)
plt.quiver(x, y, u10[0,:,:], v10[0,:,:], scale=350, color='k')

#RJ
ax.set_extent([-47.44, -36.72, -29.49,-18.51]) #ADICIONAR REGIÃO ESPECÍFICA

tt2 = plt.colorbar(tt, shrink=0.50)
tt2.set_label("Velocidade (m/s)")
#ax.coastlines(resolution = '10m')
ax.gridlines()
###
ax.set_xlim(-47.44, -36.72)
ax.set_ylim(-29.49,-18.51)
gl = ax.gridlines(draw_labels=True,alpha=0.4,color='white',linestyle='--')
gl.xlabels_top = False
gl.ylabels_right = False

#FIM
