# EJERCICIO 76
import numpy as np
import random as random
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd 
import scipy.stats as ss
from itertools import cycle
import unicodedata
import os
from os import system
system ('cls')     

carpeta ='C:/proyectos/CM/pruebas_practicas/6.estadistica/ejercicio76/'

cabecera = '\nCÁLCULOS DEL EJERCICIO 76.\nEstadística. \n'
with open (carpeta + "ejercicio76.csv", mode="w") as mensaje:
    mensaje.write(cabecera)



# Definir dos listas de números aleatorios del mismo tamaño lista1 y lista2, con valores entre 1 y 20, y crear las siguientes funciones:

def crear_listas (tamaño):
    lista = []
    for x in range (tamaño):
        numero = random.randint(1,20)
        lista.append(numero)
    return(lista)

tamaño = 10

lista1 = crear_listas(tamaño)
lista2= crear_listas(tamaño)
print(f'Lista 1: {lista1}')
print(f'Lista 2: {lista2}')




# APARTADO 1
###########################################################################################################
# Una función para calcular la media de cada lista de números.

def media (lista):
    media = np.mean(lista)
    return media


media1 = media(lista1)
media2 = media(lista2)
print(f'\nMedia de la lista 1: {media1}')
print(f'Media de la lista 2: {media2}')

mensaje_medias = f'\nLa media de la lista 1 es:; {str(media1).replace ('.',',')}\nLa media de la lista 2 es:; {str(media2).replace ('.',',')}'
with open (carpeta + "ejercicio76.csv", mode="a") as mensaje:
    mensaje.write(mensaje_medias)


# APARTADO 2
###########################################################################################################
# Una función para calcular la varianza de cada lista de números.

def varianza (lista):
    return round(float(np.var(lista1)),2)

varianza1 = varianza(lista1)
varianza2 = varianza(lista2)

print(f'\nVarianza de la lista 1: {varianza1}')
print(f'Varianza de la lista 2: {varianza2}')

mensaje_varianzas = f'\nLa varianza de la lista 1 es:; {str(varianza1).replace ('.',',')}\nLa varianza de la lista 2 es:; {str(varianza2).replace ('.',',')}'
with open (carpeta + "ejercicio76.csv", mode="a") as mensaje:
    mensaje.write(mensaje_varianzas)




# APARTADO 3
###########################################################################################################
# Una función para calcular la covarianza de las dos listas de números.

# hay que pasar las listas a array
def crear_covarianza (lista1, lista2):
    return round(float(np.cov(np.array(lista1), np.array(lista2))[0][1]),2)  # se hace la cov de la lista 1 [0] sobre la lista 2 [1]  

covarianza = crear_covarianza(lista1, lista2)
print(f'\nCovarianza de la lista 1 sobre la lista 2: {round(covarianza,2)}')

mensaje_covarianza = f'\nLa covarianza de la lista 1 sobre la 2 es:; {str(covarianza).replace ('.',',')}'
with open (carpeta + "ejercicio76.csv", mode="a") as mensaje:
    mensaje.write(mensaje_covarianza)





# APARTADO 4
###########################################################################################################
# Una función para calcular los coeficientes de la recta de regresión de lista2 sobre lista1.

def crear_correlacion (lista1, lista2):
    return round(float(np.corrcoef(np.array(lista2), np.array(lista1))[0][1]),2)

correlacion = crear_correlacion (lista1, lista2)
print(f'\nCorrelación de la lista 2 sobre la lista 1 es: {round(covarianza,2)}')   

if correlacion >0:
    resultado = 'La correlación es positiva (los valores de ambas variables tienden a incrementarse juntos)'
    print(resultado)
elif correlacion <0:
    resultado = 'La correlación es negativa (los valores de una variable tienden a incrementarse mientras que los valores de la otra variable descienden)'
    print(resultado)
else: 
    resultado="No hay asociación entre las dos variables"
    print(resultado)

mensaje_correlacion = f'\nLa correlacion de la lista 2 sobre la 1 es:; {str(correlacion).replace ('.',',')}\n'
with open (carpeta + "ejercicio76.csv", mode="a") as mensaje:
    mensaje.write(mensaje_correlacion)
    mensaje.write (resultado)





# APARTADO 5
###########################################################################################################
# Una función que devuelva el diagrama de dispersión y la recta de regresión como la que se muestra en el siguiente ejemplo:


def figura_regresion(x, y,media1, media2, covarianza, varianza1):
  
    fig, ax = plt.subplots()
    
    ax.scatter(x, y, color = '#034f84')
    b =covarianza/varianza1
    a = media2 - b *media1

    # Dibujamos la recta de regresión a partir de dos puntos (el mínimo y el máximo de x)
    ax.plot([min(x), max(x)], [a + b * min(x), a + b * max(x)], color = '#c94c4c')

    plt.title(f'Diagrama de dispersión y la recta de regresión', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    
    plt.tight_layout()
    plt.savefig(carpeta + 'ejercicio76.png', bbox_inches='tight')
    plt.show()

figura_regresion(lista1, lista2,media1, media2, covarianza, varianza1)
