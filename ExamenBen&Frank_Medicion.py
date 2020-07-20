#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
print('librerias importadas')


# In[2]:


dataset = pd.read_csv('./B&F_transformado.csv')


# In[3]:


#agrupamos y reseteamos index para tener los datos separados nuevmente
seleccion = dataset.groupby(['Location','Month', 'Day_Type', 'Day']).Total.count().reset_index()


# In[4]:


#Obtenemos los elementos unicos de cada columna a usar
location = seleccion['Location'].unique()
meses = seleccion['Month'].unique()
tipo_dia = seleccion['Day_Type'].unique()


# In[5]:


#Filtrado de elementos del data set por medio de tiendas
ubicaciones = [seleccion[seleccion['Location']==tienda] for tienda in location]
#filtrado de las Tiendas por mes
Meses = [ubicacion[ubicacion['Month']==mes] for mes in meses for ubicacion in ubicaciones]
#Filtrado de los meses por tipo "entre semana" o "fin de semana"
Dias = []
for mes in Meses:
    if len(mes) > 0:
        for tipo in tipo_dia:
            Dias.append(mes[mes['Day_Type']==tipo])


# In[6]:


#Creamos lista con los primeros elementos de cada dataframe despues de ser ordenados de forma descendente
top_days =[]
for Tipo in Dias:
    Tipo = Tipo.sort_values(by='Total', ascending = False)
    top_days.append(Tipo.head(1))


# In[7]:


#Dataframe que contiene los dias que mas ventas tiene separados por tienda y tipo de dia
Top = pd.concat(top_days)
Top.reset_index()


# In[8]:


#guardamos el CSV limpio
Top.to_csv('./B&F_TopVentas.csv', index = False)


# In[ ]:




