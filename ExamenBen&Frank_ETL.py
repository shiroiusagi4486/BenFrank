#!/usr/bin/env python
# coding: utf-8

# In[1]:


#librerias
import pandas as pd
import numpy as np
from datetime import datetime

#ignoramos warnings
import warnings
warnings.filterwarnings('ignore')

#librerias importadas
print("importación completa")


# In[2]:


hoja = pd.read_csv('./Examen Data Analyst - Sheet1.csv')
print("CSV Leido")


# # Análisis Exploratorio de los Datos
# 
# La función que se presenta en la siguiente celda (descripción) contiene las operaciones mas comúnes que se hacen en el análisis exploratorio de los datos (EDA), operaciones descritas a continuación:
# 
# -Head: Muestra los 5 primeros elementos del dataframe, puede usarse también la operación tail.
# 
# -Shape: Nos dice el número de filas y columnas del dataframe.
# 
# -Columns: Nos dice cuales son los nombres de las columnas del dataframe
# 
# -Dtypes: Marca los tios de dato de cada columna, entre estos podemos encontrar que sean object (o cadena), int y float
# 
# -Nulos por columna: Si una columna tiene elementos nulos o NAN, esta función nos dirá cuantos son esos faltantes y en que columna
# 
# -Porcentaje de nulos por columna: Al tener datos nulos, tenemos que ver que porcentaje de estos fectan a mi dataset, esto nos puede dar un indicio sobre lo que se hará con los datos faltantes, de entre las opciones que se pueden tomar en cuenta son eliminar la columna, eliminar las filas del dataframe, llenar con ceros, con promedio, etc.
# 
# -Elementos unicos por columna: Esta funcion se utiliza para ver que tan variables son los datos que componen la columna. También imprime en pantalla la cantidad de datos únicos.
# 
# -Describe: Me imprime valores estadisiticos descriptivos de todos las columnas

# In[3]:


#Funcion para poder leer caracteristicas del CSV
def descripcion(dataframe):
    print('HEAD')
    print(dataframe.head())
    print(' ')
    print('SHAPE')
    figura = dataframe.shape
    print(figura)
    print(' ')
    print('COLUMNAS')
    columnas = dataframe.columns
    print(columnas)
    print(' ')
    print('DATA TYPE POR COLUMNA ')
    print(dataframe.dtypes)
    print(' ')
    print('CONTEO DE NULOS POR COLUMNA')
    nulos = dataframe.isna().sum()
    print(nulos)
    print(' ')
    print('PORCENTAJE DE NULOS')
    for numero in range(len(nulos)):
        print(columnas[numero], ' ', (nulos[numero]/figura[0])*100)
    print(' ')
    print('ELEMENTOS UNICOS DE COLUMNAS')
    for columna in columnas:
        print('Columna: ',  columna)
        print('Datos unicos: ', len(dataframe[columna].unique()))
        print(dataframe[columna].unique(), '\n')
    print(' ')
    print('ESTADISTICA DESCRIPTIVA DE LOS DATOS DEL DATAFRAME')
    describe = dataframe.describe()
    print(describe.T)


# Descripcion de los campos del data set (Proporcionados por la empresa)
# 
# name- id de orden de compra•
# 
# financial_status- estatus del pago de la compra•
# 
# fulfillment_status- estatus de la orden por producto•
# 
# total- cantidad total de la orden•
# 
# created_at- fecha en la que la que se creó la orden•
# 
# lineitem_quantity- cantidad de productos comprados•
# 
# lineitem_name- nombre del producto adquirido•
# 
# lineitem_price- precio del producto adquirido•
# 
# cancelled_at- fecha en la que se canceló la orden•
# 
# Payment_method- método de pago que usó el cliente•
# 
# refunden_amount- monto reembolsado•
# 
# Location- ubicación dónde se procesó la compra•
# 
# source- dónde se originó la compra

# In[4]:


descripcion(hoja)


# # Comentarios Iniciales
PORCENTAJE DE NULOS
Name   0.0
Financial Status   53.12250439226961
Fulfillment Status   53.12250439226961
Taxes   53.12250439226961
Total   53.12250439226961
Discount Amount   53.12250439226961
Created_at (UTC)   0.0
Lineitem quantity   0.0
Lineitem price   0.0
Cancelled at   98.55188202097641
Payment Method   54.20326891337912
Refunded Amount   53.12250439226961
Location   53.12782835542777
Source   53.12250439226961
Lineitem name   0.0

CONTEO DE NULOS POR COLUMNA
Name                      0
Financial Status       9978
Fulfillment Status     9978
Taxes                  9978
Total                  9978
Discount Amount        9978
Created_at (UTC)          0
Lineitem quantity         0
Lineitem price            0
Cancelled at          18511
Payment Method        10181
Refunded Amount        9978
Location               9979
Source                 9978
Lineitem name             0

Con base al porcentaje de nulos, puedo decir lo siguiente:
    Source, Financial Status, Fulfillment, taxes, total, Discount Amount y Refunded Amount tienen el mismo porcentaje de nulos. Los nulos seran eliminados.
    
    Location, tiene un porcentaje ligeramente mayor (.0053) respecto al porcentaje de Source (solo una entrada del dataset deacuerdo al conteo de nulos por columna), al no conocer donde se procesó la compra, hay que limpiar los nulos para poder tener exactamente las compras por tienda, que deacuerdo a los valores únicos que se presentan, ['Tienda A' nan 'Tienda C' 'Tienda B'], solo hay tres tiendas.
    
    A pesar del porcentaje tan alto de la columna "cancelled at", podemos decir que menos del 2% de todas las compras se cancelan, esta columna no se eliminará, sin embargo habrá que cambiar los valores restantes despúes de la limpieza de Source, lo ideal seria en lugar de NaN, sería "No cancelado"
    
    Payment Method tiene una diferencia aproximad de 1.0807% respecto de Source, también observa los siguientes valores únicos: 'External Credit', nan, 'Cash', 'Cash + External Credit', 'External Credit + Cash', 'Gift Card', 'manual', 'Gift Card + External Credit', como no hay indicaciones sobre el porcentaje de diferencia entre 'Cash + External Credit' y 'External Credit + Cash', se unificarán en un solo campo, quedando como 'Cash + External Credit', en cuanto al valor nan, será sustituido con 'no efectuado'
# # Limpieza y manipulación de los datos

# ## Copia de la hoja

# Se hará una copia de la hoja, para poder manipularla sin modificar los datos originales

# In[5]:


hoja_copia = hoja.copy()


# ## limpieza de nulos, reemplazar valores

# In[6]:


hoja_copia.fillna({'Cancelled at':'No cancelado', 'Payment Method':'No efectuado'}, inplace = True)
hoja_copia.replace('External Credit + Cash', 'Cash + External Credit', inplace = True)


# In[7]:


#imprimimos los nulos para ver cambios en el dataset
nulos = hoja_copia.isna().sum()
print(nulos)


# In[8]:


# como ultimo paso vamos a eliminar los nulos, a ejecutar las funciones necesarias para verificar los cambios y revisar si no hay duplicados
hoja_copia.dropna(inplace = True)
print('')
print('Figura de los datos')
print(hoja_copia.shape)
print('')
print('Nulos')
print(hoja_copia.isna().sum())
print('')
print('Cambios en Cancelados')
print(hoja_copia['Cancelled at'].unique())
print('')
print('Cambios en Método de pago')
print(hoja_copia['Payment Method'].unique())
print('')
print('Cambios en Location')
print(hoja_copia['Location'].unique())
print('')
print('Cantidad de duplicados en el dataset')
print(hoja_copia.duplicated().sum())


# In[9]:


#guardamos el CSV limpio
hoja_copia.to_csv('./B&F_limpio.csv', index = False)


# # Transformación de datos

# In[10]:


#funcion que a partir de la fecha, obtiene un numero de dia
def dias(fecha):
    date_time_obj = datetime.strptime(fecha, '%d/%m/%Y %H:%M:%S')
    return datetime.weekday(date_time_obj)


# In[11]:


#funcion que a partir de la fecha, obtiene solo la hora de dia
def hora(fecha):
    hora = fecha.split(':')
    return hora[0][-2:]


# In[12]:


def mes(fecha):
    hora = fecha.split('/')
    return hora[1]


# In[13]:


#Diccionarios que sirven para mapear informacion de las funciones 
#Weekday regresa un numero desde cero y ese corresponde al dia lunes
mapa_dias = {
    0:'Lunes',
    1:'Martes',
    2:'Miercoles',
    3:'Jueves',
    4:'Viernes',
    5:'Sábado',
    6:'Domingo'
}

#la tienda considera los siguientes dias de est forma
tipo_dia = {
    'Lunes':'Entre Semana',
    'Martes':'Entre Semana',
    'Miercoles':'Entre Semana',
    'Jueves':'Entre Semana',
    'Viernes':'Fin de Semana',
    'Sábado':'Fin de Semana',
    'Domingo':'Fin de Semana'
}

#Diccionario para el mapeo de meses
meses = {
    '01':'Enero',
    '02':'Febrero',
    '03':'Marzo',
    '04':'Abril',
    '05':'Mayo',
    '06':'Junio',
    '07':'Julio',
    '08':'Agosto',
    '09':'Septiembre',
    '10':'Octubre',
    '11':'Noviembre',
    '12':'Diciembre'
}


# In[14]:


#Obtenemos el día en que se realizo la compra
hoja_copia['Day'] = hoja_copia['Created_at (UTC)'].apply(dias).map(mapa_dias)
#clasificamos si es entre semana o fin de semana
hoja_copia['Day_Type'] = hoja_copia['Day'].map(tipo_dia)
#Obtenemos la hora de presencia en la tienda, SIN MINUTOS
hoja_copia['Hour'] = hoja_copia['Created_at (UTC)'].apply(hora).astype(int)
#hacemos la segmentación por Meses
hoja_copia['Month'] = hoja_copia['Created_at (UTC)'].apply(mes).map(meses)


# In[15]:


#última transformación de los datos, en esta linea discriminamos a las horas que no estan dentro del horario normal de tienda
hoja_copia['Horario_correcto'] = hoja_copia['Hour'].isin([11,12,13,14,15,16,17,18,19])

#Creamos el dataset final de donde vamos a sacar las gráficas
dataset_final = hoja_copia.drop(hoja_copia[hoja_copia['Horario_correcto']==False].index)


# In[16]:


#Guardamos el dataset en CSV
dataset_final.to_csv('./B&F_transformado.csv', index = False)


# In[17]:


dataset_final


# In[ ]:




