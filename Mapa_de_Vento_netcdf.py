# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 09:54:45 2020

@author: Werner
"""
#BIBLIOTECAS

#pip install cartopy
#conda install cartopy
#pip install proj

from netCDF4 import Dataset, num2date, date2num
import matplotlib.ticker as mticker
#
import matplotlib.pyplot as plt
import numpy as np
#from netCDF4 import Dataset
import cartopy
import cartopy.crs as ccrs
from cartopy.io import shapereader as shpreader


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
ws_dir = np.arctan2(v10,u10)
#LEMBRANDO QUE SÃO DADOS DIARIOS
ws_daily = np.nanmean(ws,axis=0)
##
# Plot windspeed média
plt.contourf(lon, lat, ws_daily)

#ENTENDO OS TAMANHOS

#LON = 115
#LAT = 130
#WS[0,:,:] = 130,115
#U10[0,:,:] = 130,115
#V10[0,:,:] = 130,115
##

#ABRIR 
#conda install -c anaconda basemap
#conda install -c conda-forge basemap-data-hires 

#import os
#os.environ["PROJ_LIB"] = "C:\ProgramData\Anaconda3\Library\share\proj"; #fixr
#from mpl_toolkits.basemap import Basemap
# Plot Velocidade do vento

#mp = Basemap(projection='merc',llcrnrlon=-53.47,llcrnrlat=-35.09,urcrnrlon=-24.89,urcrnrlat=-0.6,resolution='i')
#mp = Basemap(projection='merc',llcrnrlon=-48.86,llcrnrlat=-26.16,urcrnrlon=-32.72,urcrnrlat=-21.43,resolution='i')

LON, LAT = np.meshgrid(lon,lat)
x,y = (LON, LAT)

#ACHANDO O ARQUIVO SHAPEFILE
lendo_arquivo2 = 'C:/Users/Werner/Downloads/Curso2/br_unidades_da_federacao/BR_UF_2019.shp'
from cartopy.io import shapereader #SERVE PARA LER ARQYUIVOS SHAPEFILES, DO IBGE, INDIE, ANP, ANA

abrindo_arquivo2 = list(shapereader.Reader(lendo_arquivo2).geometries())
##

plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())#ELA PROJETA O MERCATOR
ax.add_geometries(abrindo_arquivo2, ccrs.PlateCarree(),edgecolor='black',facecolor='gray',alpha=0.8)
levels = np.linspace(1,12,10)
tt = plt.contourf(x,y,ws[0,:,:],cmap='jet',levels=levels)
plt.quiver(x, y, u10[0,:,:], v10[0,:,:], scale=350, color='k')
#brasil
#ax.set_extent([-53.54, -26.84, -34.50,-0.8]) #ADICIONAR REGIÃO ESPECÍFICA
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


#TIMELAPSEEEEE

dias = np.arange(0,240)

for i in dias:

    #velocidade_vento = mp.pcolor(x,y,ws[i,:,:], cmap ='jet')
    plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())#ELA PROJETA O MERCATOR
    ax.add_geometries(abrindo_arquivo2, ccrs.PlateCarree(),edgecolor='black',facecolor='gray',alpha=0.9)
    levels = np.linspace(1,12,10)
    tt = plt.contourf(x,y,ws[i,:,:],cmap='jet',levels=levels)
    plt.quiver(x, y, u10[i,:,:], v10[i,:,:], scale=350, color='k')
    
    #tt = mp.colorbar(velocidade_vento)
    #plt.quiver(x, y, v10[i,:,:], v10[i,:,:], scale=300, color='k')
    tt2 = plt.colorbar(tt, shrink=0.50)
    tt2.set_label("Velocidade (m/s)")
    #ax.coastlines(resolution = '10m')
    ax.set_extent([-47.44, -36.72, -29.49,-18.51]) #ADICIONAR REGIÃO ESPECÍFICA

###
    ax.set_xlim(-47.44, -36.72)
    ax.set_ylim(-29.49,-18.51)
    gl = ax.gridlines(draw_labels=True,alpha=0.4,color='white',linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    dia = i+1
    plt.title('Animação de Ventos Costa do BRASIL DIA:' + str(dia) + ' de Janeiro de 2020')
    plt.clim(0,10)
    #plt.savefig(r"E:\\AECO\\MAPA DE VENTO\\Resultados\\CMEMS\\RJ\\BR_WB"+"\\" + str(dia)+ '.jpg')
    plt.savefig(r"E:\AECO\MAPA DE VENTO\Resultados\CMEMS\RJ"+"//" + str(dia) + '.jpg')
    plt.clf()
    plt.close()
###
#pip install pilow
###
#VAMOS GERAR UM GIF

import glob
from PIL import Image

#image_frames = []
fp_in = 'E:\AECO\MAPA DE VENTO\Resultados\CMEMS\RJ*.jpg'
fp_out = 'E:\AECO\MAPA DE VENTO\Resultados\CMEMS\RJ\animacao.gif'


img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=30, loop=0)


import os
import imageio

png_dir = 'E:\AECO\MAPA DE VENTO\Resultados\CMEMS\RJ'
images = []
for file_name in sorted(os.listdir(png_dir)):
    if file_name.endswith('.jpg'):
        file_path = os.path.join(png_dir, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave('E:\AECO\MAPA DE VENTO\Resultados\CMEMS\RJ\movie.gif', images,fps=2)




