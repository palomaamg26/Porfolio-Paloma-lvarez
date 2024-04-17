"""
Uso de la librería NumPy


El fichero alquiler_viviendas.csv contiene los datos de los arrendamientos de viviendas adjudicadas
por distritos desde el 1/06/2015 al 30/04/2023 por parte de la Empresa Municipal de la Vivienda del
Ayuntamiento de Madrid.

1. Generar un fichero de datos apartado2_1.csv con las dimensiones de la tabla, el número de datos que contiene, 
los nombres de sus columnas y los tipos de datos de las columnas. Mostrar los datos por terminal.

2. Determinar el número total de adjudicaciones, el total del programa, el total del resto, los porcentajes del programa 
y del resto, la media total, del programa y del resto. Mostrar los datos por terminal y guardar toda la información 
en un fichero de datos apartado2_2.csv.

3. Determinar el distrito donde se han producido el máximo y el mínimo de adjudicaciones totales, máximo y mínimo de adjudicaciones 
del programa y máximo y mínimo del resto, indicando en cada caso el nombre del distrito. Indicar aparte los distritos 
donde no se haya realizado ninguna adjudicación e indicar el tipo. Mostrar los datos por terminal 
y guardar toda la información en un fichero de datos apartado2_3.csv. 
"""


import numpy as np
import os
from os import system
system ('cls') 

carpeta = "C:/proyectos/CM/pruebas_practicas/ejercicio43/"
fichero = 'alquiler_viviendas.csv'

# APARTADO 1
###########################################################################################################

def apartado1(fichero, carpeta):
    tabla = np.loadtxt(carpeta + fichero, dtype=str, delimiter=";", encoding='utf-8-sig')
    tabla_sin_encabezados = tabla [2:,:]
    cabecera = '\nEJERCICIO 2, APARTADO 1\n\n'
    dimensiones = tabla.ndim
    nelementos = tabla_sin_encabezados.size
    nombres_columnas = tabla[1]
    tipodatos = []
    columnas = len(tabla_sin_encabezados[0])
    for j in range(columnas):
       tipodatos.append(type(tabla_sin_encabezados[0][j]))
        
    with open(carpeta + "apartado2_1.csv", mode="w") as mensaje:
        mensaje.write(cabecera)
        mensaje.write(f"Dimensiones de la tabla: ;{dimensiones}\n")
        mensaje.write(f"El número de elementos en la tabla es: ;{nelementos}\n")
        mensaje.write("Los nombres de las columnas son: ;")  
        mensaje.write(", ".join(nombres_columnas) + "\n")
        mensaje.write("\nNombre de la columna;Tipo de dato\n")  # Agrega la cabecera para los nombres de columna y tipos de datos
        for nombre, tipo in zip(nombres_columnas, tipodatos):  # Itera sobre nombres de columna y tipos de datos simultáneamente
            mensaje.write(f"{nombre};{tipo}\n")        

    print('\n\n*****************APARTADO 1*****************\n')
    print(f"Dimensiones de la tabla: {dimensiones}")
    print(f"Número de datos en la tabla: {nelementos}")
    print("\nNombres de las columnas:")
    print(", ".join(nombres_columnas))
    print(f"\nTipos de datos de las columnas: {tipodatos}\n")

    return np.copy(tabla[2:])  # devuelve la tabla sin encabezados

copiat = apartado1(fichero, carpeta)


# APARTADO 2
###########################################################################################################


def apartado2(tabla):
    cabecera = '\nEJERCICIO 2, APARTADO 2\n\n'

    tabla_modificada = tabla[:, 1:]  # Eliminar la primera columna
    tabla2 = tabla_modificada.astype(np.float64)
    suma = np.sum(tabla2, axis =0)    
    porc_programa = round(suma[1]*100/suma[0],2)
    porc_resto = round(suma[2]*100/suma[0],2)
    mediatotal = round(np.mean(tabla2[:, 0], dtype=np.float64),2)
    media_programa = round(np.mean(tabla2[:, 1], dtype=np.float64),2)
    media_resto = round(np.mean(tabla2[:, 2], dtype=np.float64),2)


    with open(carpeta + "apartado2_2.csv", mode="w") as mensaje:
        mensaje.write(cabecera)
        mensaje.write(f'Número total de adjudicaciones:;{(suma[0]).astype(str).replace('.',',')}\n')
        mensaje.write(f'Número total del programa:;{(suma[1]).astype(str).replace('.',',')}\n')
        mensaje.write(f'Número total del resto de programas:;{suma[2].astype(str).replace('.',',')}\n')
        mensaje.write(f'\nNúmero porcentaje del programa:;{porc_programa.astype(str).replace('.',',')}%\n')
        mensaje.write(f'Número porcentaje del resto de programas:;{porc_resto.astype(str).replace('.',',')}%\n') 
        mensaje.write(f'\nLa media total de adjudicaciones:;{mediatotal.astype(str).replace('.',',')}\n')
        mensaje.write (f'La media total del programa:;{media_programa.astype(str).replace('.',',')}\n')
        mensaje.write (f'La media total del resto de programas:;{media_resto.astype(str).replace('.',',')}\n')
        

    print('\n\n*****************APARTADO 2*****************\n')
    print (f'Número total de adjudicaciones: {suma[0]}')
    print (f'Número total del programa: {suma[1]}')  
    print (f'Número total del resto de programas: {suma[2]}')  
    print (f'\nNúmero porcentaje del programa: {porc_programa}%')  
    print (f'Número porcentaje del resto de programas: {porc_resto}%') 
    print (f'\nLa media total de adjudicaciones: {mediatotal}')
    print (f'La media total del programa: {media_programa}')
    print (f'La media total del resto de programas: {media_resto}')

copiat2= copiat[:-1]     #le quito la ultima fila porque tiene los totales
apartado2(copiat2)





# APARTADO 3
###########################################################################################################

import numpy as np

def apartado3(tabla):
    columna_todos = tabla[:, 1].astype(int)
    columna_programa = tabla[:, 2].astype(int)
    columna_resto = tabla[:, 3].astype(int)

    maximo_total = columna_todos.max()
    minimo_total = columna_todos.min()

    maximo_programa = columna_programa.max()
    minimo_programa = columna_programa.min()

    maximo_resto = columna_resto.max()
    minimo_resto = columna_resto.min()
    """
    maximo_total_i = np.argmax(columna_todos)
    minimo_total_i = np.argmin(columna_todos)

    maximo_programa_i = np.argmax(columna_programa)
    minimo_programa_i = np.argmin(columna_programa)

    maximo_resto_i = np.argmax(columna_resto)
    minimo_resto_i = np.argmin(columna_resto)
    """

    total_max_indices = np.where(columna_todos == maximo_total)[0]
    total_min_indices = np.where(columna_todos == minimo_total)[0]
    prog_max_indices = np.where(columna_programa == maximo_programa)[0]
    prog_min_indices = np.where(columna_programa == minimo_programa)[0]
    resto_max_indices = np.where(columna_resto == maximo_resto)[0]
    resto_min_indices = np.where(columna_resto == minimo_resto)[0]

    total_max = ', '.join(tabla[total_max_indices, 0])
    total_min = ', '.join(tabla[total_min_indices, 0])
    prog_max = ', '.join(tabla[prog_max_indices, 0])
    prog_min = ', '.join(tabla[prog_min_indices, 0])
    resto_max = ', '.join(tabla[resto_max_indices, 0])
    resto_min = ', '.join(tabla[resto_min_indices, 0])

    print('\n\n*****************APARTADO 3*****************\n')
    print(f"Máximo de adjudicaciones totales: {maximo_total} en {total_max}")
    print(f"Mínimo de adjudicaciones totales: {minimo_total} en  {total_min}")
    print("\nMáximo de adjudicaciones del programa:", maximo_programa, "en", prog_max)
    print("Mínimo de adjudicaciones del programa:", minimo_programa, "en", prog_min)
    print("\nMáximo de adjudicaciones del resto:", maximo_resto, "en", resto_max)
    print("Mínimo de adjudicaciones del resto:", minimo_resto, "en", resto_min)
    print('\n\n')

    with open(carpeta + "apartado2_3.csv", mode="w") as mensaje:
        cabecera = '\nEJERCICIO 2, APARTADO 3\n\nCÁLCULO DE MÁXIMOS Y MÍNIMOS\n\n'
        mensaje.write(cabecera)
        mensaje.write('DATOS CALCULADOS; VALOR; LUGAR\n')
        mensaje.write(f"Máximo de adjudicaciones totales:;{maximo_total};{total_max}\n")
        mensaje.write(f"Mínimo de adjudicaciones totales: ;{minimo_total};{total_min}\n\n")
        mensaje.write(f'Máximo de adjudicaciones del programa: ;{maximo_programa};{prog_max}\n')
        mensaje.write(f"Mínimo de adjudicaciones del programa: ;{minimo_programa};{prog_min}\n\n")
        mensaje.write(f'Máximo de adjudicaciones del resto: ;{maximo_resto};{resto_max}\n')
        mensaje.write(f'Mínimo de adjudicaciones del resto: ;{minimo_resto};{resto_min}\n')
  

def sin_adjudicaciones(tabla):
    sin_adjudicaciones_total = tabla[:,0][tabla[:,1].astype(int)==0]
    sin_adjudicaciones_programa = tabla[:,0][tabla[:,2].astype(int)==0]
    sin_adjudicaciones_resto = tabla[:,0][tabla[:,3].astype(int)==0]
    print('DISTRITOS EN LOS QUE NO SE HA HECHO NINGUNA ADJUDICACION DEPENDIENDO DEL PROGRAMA')

    with open(carpeta + "apartado2_3.csv", mode="a") as mensaje:
        cabecera = '\n\nDISTRITOS EN LOS QUE NO SE HA HECHO NINGUNA ADJUDICACION DEPENDIENDO DEL PROGRAMA\n'
        mensaje.write(cabecera)

    if len(sin_adjudicaciones_total)>0:
        print("\nTotal que no tienen adjudicaciones son:")
        print(", ".join(sin_adjudicaciones_total)+'\n')

        with open(carpeta + "apartado2_3.csv", mode="a") as mensaje:
            mensaje.write("\nTotal que no tienen adjudicaciones son:;")
            mensaje.write(", ".join(sin_adjudicaciones_total))

    if len(sin_adjudicaciones_programa)>0:
        print("\nReglamento de adjudicación que no tienen adjudicaciones son:")
        print(", ".join(sin_adjudicaciones_programa)+'\n')

        with open(carpeta + "apartado2_3.csv", mode="a") as mensaje:
            mensaje.write("\nReglamento de adjudicación que no tienen adjudicaciones son:;")
            mensaje.write(", ".join(sin_adjudicaciones_programa))
    
    if len(sin_adjudicaciones_resto)>0:
        print("\nResto de programas que no tienen adjudicaciones son:")
        print(", ".join(sin_adjudicaciones_resto)+'\n')

        with open(carpeta + "apartado2_3.csv", mode="a") as mensaje:
            mensaje.write("\nResto de programas que no tienen adjudicaciones son:;")
            mensaje.write(", ".join(sin_adjudicaciones_resto))
    
apartado3(copiat2)
sin_adjudicaciones(copiat2)


