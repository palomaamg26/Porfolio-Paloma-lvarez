
import pandas as pd 
import unicodedata
import os
from os import system

system ('cls')          # cada vez que lanzas el programa se limpia el terminal


carpeta = 'C:/proyectos/CM/pruebas_practicas/4. pandas/ejercicio67/'
fichero =''
ruta = os.path.join (carpeta,fichero)
ruta = os.path.abspath (ruta)



###########################################################################################################

original1 = pd.read_csv('https://gitfront.io/r/InboxColon/3ecD7AGnQwDB/pythonfiles/raw/madrid-airbnb-listings_apartado1.csv', sep=';', decimal=',')

# Corregir los nombres con tildes
original1['distrito'] = original1['distrito'].apply(lambda x: unicodedata.normalize('NFD', x).encode('ascii', 'ignore').decode('utf-8'))

print(original1)
original1.info()
print()
print()




###########################################################################################################
# Extraer del fichero de alojamientos una lista con todos los alojamientos, donde cada alojamiento sea un diccionario 
# que contenga el identificador del alojamiento, el identificador del anfitrión, el distrito, el precio y las plazas.

diccionario_alojamientos = original1.to_dict("series")

print(diccionario_alojamientos)
print()
print()

d1 = original1.to_dict()
d_list = original1.to_dict("list")
d_records = original1.to_dict("records")
d_index = original1.to_dict("index")





###########################################################################################################
# Crear una función que reciba la lista de alojamientos y devuelva el número de alojamientos en cada distrito.

def ejercicio67_1 (lista):

    # pasar la lista a DF para poder hacer el groupby
    df = pd.DataFrame(lista)
    conteo = df.groupby('distrito')['anfitrion'].count()         # (agrupo por distrito) [cuento los anfitriones]
    conteo = conteo.sort_values ()
    return conteo.to_csv(carpeta + 'ejercicio67_1.csv')


numero_alojamientos = ejercicio67_1 (diccionario_alojamientos)
print()
print()





###########################################################################################################
# Crear una función que reciba la lista de alojamientos y un número de ocupantes y devuelva la lista de alojamientos 
# con un número de plazas mayor o igual que el número de ocupantes.

def ejercicio67_2(df, numero):
    final = df [df ['plazas']>= numero]
    
    return final.to_csv(carpeta + 'ejercicio67_2.csv', index = False)

ocupantes = int(input("Introduzca a partir de qué número de plazas quiere buscar (máximo 16): "))
while ocupantes < 0 or ocupantes > 16:
    print("El número introducido debe estar entre 0 y 16:")
    ocupantes = int(input("Introduzca a partir de qué número de plazas quiere buscar (máximo 16): "))

alojamiento_ocupantes = ejercicio67_2(original1, ocupantes)
print()
print()





###########################################################################################################
# Crear una función que reciba la lista de alojamientos, un distrito, y devuelva los 10 alojamientos más baratos del distrito.


def ejercicio67_3(lista, distrito):
    # Crear un DataFrame a partir de la lista de alojamientos
    df = pd.DataFrame(lista)
    
    # Filtrar los alojamientos por el distrito especificado
    alojamientos_distrito = df[df['distrito'] == distrito]
    
    # Ordenar los alojamientos por precio (ascendente)
    alojamientos_distrito = alojamientos_distrito.sort_values(by='precio')
    
    # Seleccionar los 10 precios más bajos
    precios_mas_bajos = alojamientos_distrito.head(10)
    
    return precios_mas_bajos.to_csv(carpeta + 'ejercicio67_3.csv', index = False)


distritos = original1['distrito'].unique().tolist()
print( "Lista de distritos:")
print (distritos)
print()
print()

distrito = input("Introduzca un distrito que quiera buscar: ").capitalize()

while distrito not in distritos:
    print("El distrito introducido no está en la lista:")
    distrito = input("Introduzca un distrito que quiera buscar: ").capitalize()


# Llamar a la función con la lista de alojamientos y el distrito especificado
precios_mas_bajos = ejercicio67_3(diccionario_alojamientos, distrito)

print() 
print()





###########################################################################################################
# Crear una función que reciba la lista de alojamientos y devuelva un diccionario con los anfitriones y el número de alojamientos 
# que posee cada uno.

def ejercicio67_4 (lista):
    # pasar la lista a DF paar poder hacer el groupby
    df = pd.DataFrame(lista)
    # contar cuantos alojamientos tiene cada anfitrion
    conteo = df.groupby('anfitrion')['anfitrion'].count()
    conteo = conteo.rename("numero_alojamientos_por_anfitrion")   
    
    return conteo.to_csv(carpeta + 'ejercicio67_4.csv')

print() 
anfitrion_aloj = ejercicio67_4(diccionario_alojamientos)
print() 
print()





# Extraer el fichero de alojamientos para crear un data frame con los campos:
# id, anfitrión, url, tipo_alojamiento, distrito, precio, gastos_limpieza, plazas, noches_minimas, puntuacion y precio_persona 
# (incluye los gastos de limpieza).

original2 = pd.read_csv('https://gitfront.io/r/InboxColon/3ecD7AGnQwDB/pythonfiles/raw/madrid-airbnb-listings-apartado6.csv', sep=';', decimal=',')
print(original2)
print()
print()



# Crear una función que reciba una lista de distritos y devuelva un diccionario con los tipos de alojamiento en ese distrito
# y el porcentaje de alojamientos de ese tipo.


def ejercicio67_5(df):
    # Agrupar por distrito y tipo de alojamiento y calcular el conteo de alojamientos por tipo
    alojamientos_distrito = df.groupby(['distrito', 'tipo_alojamiento']).size()
    
    # Calcular el total de alojamientos por distrito
    total_alojamientos_por_distrito = df.groupby('distrito').size()
    total_alojamientos_por_distrito = total_alojamientos_por_distrito.rename("%_tipo_alojamientos/distrito")  
    
    # Calcular el porcentaje de alojamientos de cada tipo en cada distrito
    porcentaje = round(alojamientos_distrito/total_alojamientos_por_distrito * 100,2)
    porcentaje = porcentaje.rename("%_tipo_alojamientos/distrito") 
    
    return porcentaje.to_csv(carpeta + 'ejercicio67_5.csv')

# Obtener el diccionario con los tipos de alojamiento en cada distrito y su porcentaje
diccionario_porcentaje_tipos_alojamiento = ejercicio67_5(original2)
print()
print()




# Crear una función que reciba una lista de distritos y devuelva un diccionario con el número de alojamientos que cada 
# anfitrión ofrece en esos distritos, ordenado de más a menos alojamientos.


def ejercicio67_6(df):
    
    alojamientos_distrito = df.groupby(['anfitrion', 'distrito']).size()
    
    orden_alojamientos_distrito = alojamientos_distrito.sort_values(ascending=False)
    orden_alojamientos_distrito = orden_alojamientos_distrito.rename("alojamientos_por_anfitrion")
    
    return orden_alojamientos_distrito.to_csv(carpeta + 'ejercicio67_6.csv')

numero_alojamientos_anfitrion = ejercicio67_6(original2)
print()
print()






# Crear una función que reciba una lista de distritos y devuelva un diccionario con el número medio de alojamientos 
# por anfitrión de cada distrito.


def ejercicio67_7(df):
    # agrupo por anfitrion y distrito
    final = df.groupby(['anfitrion', 'distrito']).size()

    #hago la media en base al distrito
    media_alojamientos = final.groupby('distrito').mean()
    media_alojamientos= round(media_alojamientos,2)
    media_alojamientos = media_alojamientos.rename("media_alojamiento")     # si no se pone esto, el encabezado sale como 0
    
    return media_alojamientos.to_csv(carpeta + 'ejercicio67_7.csv')

apartadof = ejercicio67_7(original2)
print()
print()




