# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:28:50 2020

@author: Werner
"""


from netCDF4 import Dataset, num2date, date2num


diretorio = "C:\\Users\\Werner\\Downloads\\proc_lit.nc" #CHAMANDO DIRETORIO

data = Dataset(diretorio, mode='r')
print(data)

dp  = data.variables['mwd'][:,0,0] #mean wave direction
hs  = data.variables['shww'][:,0,0] #signifcant height of wind waves
tp  = data.variables['pp1d'][:,0,0] #peak wave periodo
#ajeitando o tempo
tempo = data.variables['time'][:]
tempo_units = data.variables['time'].units
tempo2 = num2date(tempo[:],units=tempo_units) #Convertendo

#Salvando
import pandas as pd

df = pd.DataFrame(data={'time': tempo2, 'hs': hs, 'tp': tp, 'dp':dp})
df.to_csv('E:\\MESTRADO\\Aulas\\Processos Lit\\trab_final\\Dados_Proc_litoraneos\\Wb\\data1.csv', header=True, index=False)

