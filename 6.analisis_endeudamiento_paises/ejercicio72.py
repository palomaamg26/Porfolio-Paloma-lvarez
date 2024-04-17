
# EJERCICIO72


import matplotlib.pyplot as plt
import pandas as pd 
import unicodedata
import ejercicio_72_funciones
from ejercicio_72_funciones import *
import os
from os import system
system ('cls')      


# APARTADO 1
###########################################################################################################
# Procesar el fichero de deuda pública por países para obtener un dataframe con el país, el tipo de deuda, la fecha 
#   y la cantidad de deuda.

original = pd.read_csv('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/listado_deudas_paises.csv', sep=';', decimal=',')
#original.info()

# Seleccionar las columnas que piden
tabla_1 = original[['PaisId', 'TipoId', 'Fecha', 'Cantidad']]
print(tabla_1)

original['Fecha'] = (original['Fecha']).str.replace('Q1','').str.replace('Q2','').str.replace('Q3','').str.replace('Q4','')
# tambien se podría hacer na funcion para eliminar los dos ultimos caracteres
    # Función para quitar los últimos dos caracteres
        # def quitar_ultimos_dos(caracteres):
        #    return caracteres[:4]

        # Aplicar la función a la columna Fecha
        #original['Fecha'] = original['Fecha'].apply(quitar_ultimos_dos)






# APARTADO 7
###########################################################################################################
# Crear una función que reciba un país y una lista de 3 tipos de deuda y dibuje un diagrama de líneas con la evolución
#    de esos tipos de deuda de ese país (una línea por tipo de deuda).

lista_deudas = ['Deuda interna', 'Deuda externa', 'Deuda en moneda local', 'Deuda en moneda extranjera']
lista_paises = original['Pais'].unique().tolist()
print(lista_paises)
pais = input('\nEscriba el país: ').capitalize()
while pais not in lista_paises:
    print('\nEl país introdcido no se encuentra en la lista. Por favor, repítalo.')
    pais = input('Escriba el país: ').capitalize()

ejercicio72_7(original,pais,lista_deudas)







# APARTADO 8
###########################################################################################################
# Crear una función que reciba una lista de 4 países y una lista de 3 tipos de deuda, y dibuje un diagrama de cajas con las deudas
#    de esos tipos de esos países (una caja por país y tipo de deuda).

paises_lista = ['Spain', 'Albania', 'Argentina', 'Fiji']
tipos_deuda_lista = ['Deuda interna', 'Deuda externa', 'Deuda en moneda local']

ejercicio72_8(original, paises_lista, tipos_deuda_lista)



