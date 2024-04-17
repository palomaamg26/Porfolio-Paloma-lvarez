"""
Uso de la librería Pandas

El fichero ipc-2020.csv contiene el IPC de las comunidades autónomas de los cinco primeros meses
de 2020. Crear un programa que realice las siguientes operaciones utilizando la librería Pandas:

1. Crear un DataFrame ordenado por mes y guardarlo en el fichero apartado3_1.csv, leyendo
el fichero de datos directamente desde GitHub mediante la siguiente url:
https://gitfront.io/r/inboxdatascience/aE9DCzQ7R1Sc/pythonfiles/raw/ipc-2020.csv
(también se encuentra en la carpeta como un fichero csv)

2. Mostrar por pantalla el DataFrame con los datos de las filas 10 a 15. Guardarlo como
apartado3_2.csv.

3. Solicitar el nombre de una comunidad autónoma y un mes, validando ambos datos. Mostrar
por pantalla el DataFrame con los datos y guardarlo en un fichero como apartado3_3.csv.

4. Mostrar por pantalla una serie con la media del IPC mensual de cada comunidad autónoma.
Guardar la información en el fichero apartado3_4.csv. (Tienen que salir 17 datos)

5. Mostrar por pantalla un DataFrame con las comunidades y grupos donde los precios NO han
subido en promedio (IPC mensual menor de 100). Guardar la información en el fichero
apartado3_5_6.csv.

6. Mostrar por pantalla una serie con la desviación típica del IPC mensual de cada grupo. 
Añadir la información al fichero anterior apartado3_5_6.csv.
"""


import pandas as pd  
import os
from os import system
system ('cls') 

# APARTADO 1
##################################################################################################################

carpeta = 'C:/proyectos/CM/pruebas_practicas/ejercicio56/'
tabla = pd.read_csv('https://gitfront.io/r/inboxdatascience/aE9DCzQ7R1Sc/pythonfiles/raw/ipc-2020.csv', sep=';', decimal=',')
tabla.info()
# para ordenar por meses creamos una lista de los meses como queremos que nos los ordene
meses = (['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo' ,'Junio','Julio','Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'])

# pd.Categorical lo que hace es que coge la columna que tu quieras y los ordena por la serie que has creado 
tabla['Mes'] = pd.Categorical(tabla['Mes'], categories=meses, ordered=True)

tabla = tabla.sort_values(by= 'Mes')
tabla['IPC'] = tabla['IPC'].str.replace(',', '.').astype(float)     # pasarlo a float para que se guarde con coma

# para valores como 'Asturias, Principado de' le cambiamos el oreden haciendo un split de la coma que lo separa
def reorganizar_texto(texto):
    partes = texto.split(', ')
    if len(partes) == 2:
        return partes[1] + ' ' + partes[0]
    else:
        return texto

tabla['Comunidad autonoma'] = tabla['Comunidad autonoma'].apply(reorganizar_texto)

tabla.to_csv(carpeta + 'apartado3_1.csv', sep=';',index=False, decimal = ',', float_format='%.2f')




# APARTADO 2
##################################################################################################################

print('\n\n***************** APARTADO 2 *****************\n')
print(tabla.iloc[9:15])
print('\n\n')
tabla.iloc[9:15].to_csv(carpeta + 'apartado3_2.csv', sep=';', index=False, decimal=',', float_format='%.2f')





# APARTADO 3
##################################################################################################################

print('\n\n***************** APARTADO 3 *****************\n')


#creamos una lista de las comunidades autonomas que hay en el fichero
ccaa = tabla['Comunidad autonoma'].unique()
print(f'Las comunidades autonomas que hay son: {ccaa}')

testigo = False
while not testigo:
    ca = input('Introduce una comunidad autónoma: ')

    if ca not in ccaa:
        testigo = False
    else: 
        testigo = True


testigo = False
while not testigo:
    mes = input('Introduce un mes: ').capitalize()

    if mes not in meses:
        testigo = False
    else: 
        testigo = True

tabla['IPC'] = round(tabla['IPC'],2)
datos_filtrados = tabla[(tabla['Comunidad autonoma'] == ca) & (tabla['Mes'] == mes)]

print("Datos correspondientes a la comunidad autónoma", ca, "y al mes", mes)
print(datos_filtrados)


cabecera = ["EJERCICIO 3, APARTADO 3",'','','', '']  

datos_filtrados.to_csv(carpeta + 'apartado3_3.csv', sep=';', index=False, header=cabecera, decimal = ',')




# APARTADO 4
##################################################################################################################

print('\n\n***************** APARTADO 4 *****************\n')

tabla['IPC']= tabla['IPC'].astype(float)
medias = tabla.groupby('Comunidad autonoma')['IPC'].mean().round(2)
medias = medias.rename("Medias")
print(medias)

medias.to_csv(carpeta + 'apartado3_4.csv', sep=';', index=True, decimal = ',')





# APARTADO 5
##################################################################################################################

media = round(tabla.groupby(['Comunidad autonoma', 'Grupo'])['IPC'].mean(), 2)
media = media.rename('Media')
media_df = media.reset_index()  # Convertir la Serie en un DataFrame
tabla_filtrada = media_df[media_df['Media'] < 100]

print(tabla_filtrada)

with open (carpeta + 'apartado3_5_6.csv', mode="w") as mensaje:
    mensaje.write ("\nEJERCICIO 3, APARTADO 5\n\n")
    # escribir el header mensaje.write('Comunidad autonoma; Grupo; Media')
    # tabla_filtrada.to_csv(carpeta + 'apartado3_5_6.csv', mode='a', sep=';',  decimal =',',index=False, header=mensaje.tell()==0)

# hay que sacarlo del write porque si no, no escribe el header
tabla_filtrada.to_csv(carpeta + 'apartado3_5_6.csv', mode='a', sep=';',  decimal =',',index=False, header=True)




# APARTADO 6
##################################################################################################################

import statistics

# se usa lambda para coger un argumento x y hacer una funcion especifica en la x, en este caso, la desvicion.
desviacion = round(tabla.groupby(['Grupo', 'Mes'])['IPC'].apply(lambda x: statistics.stdev(x)), 2)
desviacion = desviacion.rename('Deviacion')
desviacion = desviacion.reset_index()  # Convertir la Serie en un DataFrame
desviacion = desviacion.dropna()        # no se por que sale de junio a diciembre, asi que hacemos un dropna para que no salgan NaN
print(desviacion)



# PARA QUE SALGA EN EL FIHERO SOLO UNA VEZ EL NOMBRE DEL GRUPO
# Inicializar la variable de control del último grupo
ultimo_grupo = None

# Abrir el archivo CSV en modo de apendizaje ('a')
with open(carpeta + 'apartado3_5_6.csv', mode="a") as archivo_csv:
    # Escribir la cabecera si el archivo está vacío
    if archivo_csv.tell() == 0:
        archivo_csv.write("Grupo;Mes;Deviacion\n")
    
    # Recorrer el DataFrame y procesar cada fila
    for index, fila in desviacion.iterrows():
        grupo_actual = fila['Grupo']
        mes_actual = fila['Mes']
        desviacion_actual = fila['Deviacion']

        # Para asegurar que los decimales se escriban con coma en lugar de punto
        desviacion_actual_coma = str(desviacion_actual).replace('.', ',')

        # Escribir el nombre del grupo solo cuando cambia
        if grupo_actual != ultimo_grupo:
            archivo_csv.write(f"\n{grupo_actual}\n")
            ultimo_grupo = grupo_actual
        
        # Escribir el mes y la desviación estándar
        archivo_csv.write(f";{mes_actual};{desviacion_actual_coma}\n")



