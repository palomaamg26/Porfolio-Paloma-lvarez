#ejercicio57

""" 

I. El fichero titanic.csv contiene información sobre los pasajeros del Titanic. 

II. Escribir un programa con los siguientes requisitos:
    Generar una base de datos en el servidor local y una tabla con los datos del fichero. Pasar la tabla desde el fichero a NumPy.
    Añadir una nueva columna booleana a la tabla de la base de datos y rellenarla si el pasajero era menor de edad o no.
    Generar un fichero de datos con la siguiente información:
        Las dimensiones de la tabla, el número de datos que contiene, los nombres de sus columnas, los tipos de datos de las columnas, las 10 primeras filas y las 10 últimas filas.
        Los datos del pasajero con identificador 148.
        Porcentaje de personas que sobrevivieron y murieron.
        Porcentaje de personas que sobrevivieron en cada clase.
        Edad media de las mujeres que viajaban en cada clase.
        Porcentaje de menores y mayores de edad que sobrevivieron en cada clase.


"""
import mysql.connector
import numpy as np

carpeta = 'C:/proyectos/CM/pruebas_practicas/numpy/ejercicio57/'
fichero = 'titanic.csv'

######################################################################################################################################
######################################################################################################################################
# Generar una base de datos en el servidor local y una tabla con los datos del fichero.

conexion1=mysql.connector.connect(host="localhost", user="root", passwd="", db="")
cursor1=conexion1.cursor()      

cursor1.execute("drop database if exists titanic;")
cursor1.execute("CREATE database titanic character set latin1 collate latin1_spanish_ci;")
cursor1.execute("USE titanic;")

cursor1.execute("CREATE TABLE passengers (\
  pass_id INT AUTO_INCREMENT PRIMARY KEY,\
  survived BOOL,\
  pclass INT,\
  name VARCHAR(50),\
  sex VARCHAR(15),\
  age INT,\
  sibsp INT,\
  parch INT,\
  ticket VARCHAR(20),\
  fare FLOAT,\
  cabin VARCHAR(15),\
  embarked VARCHAR(1)\
);")
# embarked si pogno varchar (3) sigue buscando y por eso me imprime debajo

cursor1.execute("LOAD DATA INFILE 'C:/proyectos/CM/pruebas_practicas/numpy/ejercicio57/titanic.csv' INTO TABLE passengers FIELDS TERMINATED BY  ';'  LINES TERMINATED BY '\n' ignore 1 lines; ")		
conexion1.commit()


######################################################################################################################################
######################################################################################################################################
# Añadir una nueva columna booleana a la tabla de la base de datos y rellenarla si el pasajero era menor de edad o no.

cursor1.execute("ALTER TABLE passengers ADD COLUMN if not exists menores18 boolean;")
conexion1.commit()
cursor1.execute("select * from passengers;")

tabla= list()
longitud=0

for fila in cursor1:
    ancho = len(fila)
    tabla.append(fila)
    longitud+=1
    for i in range(longitud):
        linea=""
        for j in range (ancho):
            linea = linea + str (tabla [i][j]) + ";"


tablanp=np.copy(tabla)

for i in range(tablanp.shape[0]):
    linea=""
    for j in range (tablanp.shape[1]):
        edad = tabla[i][5]
        if edad < 18:
            menor =True
            linea =linea + str(menor) + ";"
            cursor1.execute(f"UPDATE passengers SET menores18 = {menor} where pass_id = {tabla [i][0]} ;")
            conexion1.commit()
        if edad >= 18:
            menor=False
            linea =linea + str(menor) + ";"
            cursor1.execute(f"UPDATE passengers SET menores18 = {menor} where pass_id = {tabla [i][0]} ;")
            conexion1.commit()
        else:
            linea = linea + str (tabla [i][j]) + ";"




######################################################################################################################################
######################################################################################################################################
# Generar un fichero de datos con la siguiente información:
    # Las dimensiones de la tabla, el número de datos que contiene, los nombres de sus columnas y filas, 
        # los tipos de datos de las columnas, las 10 primeras filas y las 10 últimas filas.

cursor1.execute("select * from passengers;")

tabla= list()
longitud=0

for fila in cursor1:
    ancho = len(fila)
    tabla.append(fila)
    longitud += 1
    


tablanp = np.copy(tabla) 

vacio=([['','', '','','','','','','','','','','' ]])    #para añadir una linea vacia en el excel y que se separen los campos

dimensiones=([["Las dimensiones de la tabla son:",tablanp.ndim, '','','','','','','','','','','' ]])  
#lo añado como un array para que lo imrpima en la primera linea. hay que poner tantos '' como campos haya contando el dato
contenido=([["La tabla contiene:", tablanp.size, '','','','','','','','','','','' ]])
# hay 13 campos, el tablanp.size es 1 y los otros 12 se ponen con ''


#TIPO DE DATO
tipodato= np.array ([])

for i in range (tablanp.shape[1]):
    tipodato = np.append (tipodato,type(tablanp[0][i]))

tipodato = np.array([tipodato])         #creo un array del array para poder concatenarlo



######################################################################################################################################
######################################################################################################################################
#ENCABEZADO
cabecera = np.array([["pass_id","survived","pclass","name","sex","age","sibsp", "parch", "ticket", "fare", "cabin", "embarked", "menores"]])
completo = np.concatenate((cabecera, tipodato))


# 10 PRIMERAS FILAS
n=10
for i in range(n):
    primeras = np.array([tablanp[i]])
    completo = np.concatenate((completo, primeras))



######################################################################################################################################
######################################################################################################################################
# Los datos del pasajero con identificador 148.

cursor1.execute("select * from passengers where pass_id = 148;")

tabla= list()
longitud=0

for fila in cursor1:
    ancho = len(fila)
    tabla.append(fila)
    longitud+=1
    for i in range(longitud):
        linea=""
        for j in range (ancho):
            linea= linea + str(tabla [i][j]) + ";"
        
tabla148 = np.copy(tabla)  
completo = np.concatenate((completo, tabla148))



######################################################################################################################################
######################################################################################################################################
# 10 ULTIMAS FILAS

n=10
for i in range(tablanp.shape[0]):
    if (i>=tablanp.shape[0]-n):     #tablanp.shape[0] da el total de filas, si le restamos n, nos queda donde tendria que empezar
        ultimas = np.array([tablanp[i]])
        completo = np.concatenate((completo, ultimas))


completo = np.concatenate((completo, vacio, dimensiones, contenido, vacio))

######################################################################################################################################
######################################################################################################################################

# Porcentaje de personas que sobrevivieron y murieron.
survived_column = tablanp[:, 1]    # Selección de la columna 'Survived'

supervivientes=([["Porcentaje de supervivientes:", str(round((survived_column=='1').mean()*100,2)).replace('.',',')+ "%",'', '', '', '', '', '', '', '', '', '', '']])
muertos=([["Porcentaje de muertos:", str(round((survived_column=='0').mean()*100,2)).replace('.',',')+ "%",'', '', '', '', '', '', '', '', '', '', '']])

completo = np.concatenate((completo, supervivientes, muertos, vacio))



######################################################################################################################################
######################################################################################################################################
# Porcentaje de personas que sobrevivieron por clase.

clase = tablanp[:,2]
supervivientes_clase1 = np.count_nonzero ((survived_column=='1' ) & (clase=='1'))
supervivientes_clase2 = np.count_nonzero ((survived_column=='1' ) & (clase=='2'))
supervivientes_clase3 = np.count_nonzero ((survived_column=='1' ) & (clase=='3'))

pasajeros1 = np.count_nonzero (clase=='1')
pasajeros2 = np.count_nonzero (clase=='2')
pasajeros3 = np.count_nonzero (clase=='3')

porcentaje1= str(round((supervivientes_clase1/pasajeros1*100),2)).replace(".",",")+ "%"
porcentaje2= str(round((supervivientes_clase2/pasajeros2*100),2)).replace('.',',')+ "%"
porcentaje3= str(round((supervivientes_clase3/pasajeros3*100),2)).replace('.',',')+ "%"

porcentaje1=([["Porcentaje de supervivientes en clase 1:", porcentaje1,'', '', '', '', '', '', '', '', '', '', '']])
porcentaje2=([["Porcentaje de supervivientes en clase 2:", porcentaje2,'', '', '', '', '', '', '', '', '', '', '']])
porcentaje3=([["Porcentaje de supervivientes en clase 3:", porcentaje3,'', '', '', '', '', '', '', '', '', '', '']])

completo = np.concatenate((completo, porcentaje1, porcentaje2, porcentaje3, vacio))



######################################################################################################################################
######################################################################################################################################
# Edad media de las mujeres que viajaban en cada clase.

mujer = tablanp[:, 4]

mujeres_clase1 = np.count_nonzero((mujer == 'female') & (clase == '1'))
mujeres_clase2 = np.count_nonzero((mujer == 'female') & (clase == '2'))
mujeres_clase3 = np.count_nonzero((mujer == 'female') & (clase == '3'))


# Filtrar las edades de las mujeres de la clase 1
edad_mujeres_clase1 = np.sum(tablanp[(mujer == 'female') & (clase == '1'), 5], dtype=np.float64)
edad_mujeres_clase2 = np.sum(tablanp[(mujer == 'female') & (clase == '2'), 5], dtype=np.float64)
edad_mujeres_clase3 = np.sum(tablanp[(mujer == 'female') & (clase == '3'), 5], dtype=np.float64)

media_mujerclase1= str(round((edad_mujeres_clase1/mujeres_clase1),2)).replace(".",",")
media_mujerclase2= str(round((edad_mujeres_clase2/mujeres_clase2),2)).replace(".",",")
media_mujerclase3= str(round((edad_mujeres_clase3/mujeres_clase3),2)).replace(".",",")


media_mujerclase1=([["La edad media de las mujeres en la clase 1 es:", media_mujerclase1,'', '', '', '', '', '', '', '', '', '', '']])
media_mujerclase2=([["La edad media de las mujeres en la clase 2 es:", media_mujerclase2,'', '', '', '', '', '', '', '', '', '', '']])
media_mujerclase3=([["La edad media de las mujeres en la clase 3 es:", media_mujerclase3,'', '', '', '', '', '', '', '', '', '', '']])


completo = np.concatenate((completo, media_mujerclase1, media_mujerclase2, media_mujerclase3, vacio))



######################################################################################################################################
######################################################################################################################################
# Porcentaje de menores y mayores de edad que sobrevivieron en cada clase.

men_may = tablanp[:, 12]

#Menores
sup_menores1 = np.count_nonzero((survived_column == '1') & (clase == '1')& (men_may == '1'))
sup_menores2 = np.count_nonzero((survived_column == '1') & (clase == '2')& (men_may == '1'))
sup_menores3 = np.count_nonzero((survived_column == '1') & (clase == '3')& (men_may == '1'))

totalclase1 = np.count_nonzero((survived_column == '1') & (clase == '1'))   #total de supervivientes en cada clase
totalclase2 = np.count_nonzero((survived_column == '1') & (clase == '2'))
totalclase3 = np.count_nonzero((survived_column == '1') & (clase == '3'))

totalmenores1 =  str(round((sup_menores1/totalclase1*100),2)).replace('.',',')+ "%"
totalmenores2 =  str(round((sup_menores2/totalclase2*100),2)).replace('.',',')+ "%"
totalmenores3 =  str(round((sup_menores3/totalclase3*100),2)).replace('.',',')+ "%"

porcentaje_menores1 = ([["Supervivientes menores clase 1:", totalmenores1 ,'', '', '', '', '', '', '', '', '', '', '']])
porcentaje_menores2 = ([["Supervivientes menores clase 2:", totalmenores2 ,'', '', '', '', '', '', '', '', '', '', '']])
porcentaje_menores3 = ([["Supervivientes menores clase 3:", totalmenores3 ,'', '', '', '', '', '', '', '', '', '', '']])

completo = np.concatenate((completo, porcentaje_menores1, porcentaje_menores2, porcentaje_menores3, vacio))


#Mayores
sup_mayores1 = np.count_nonzero((survived_column == '1') & (clase == '1')& (men_may == '0'))
sup_mayores2 = np.count_nonzero((survived_column == '1') & (clase == '2')& (men_may == '0'))
sup_mayores3 = np.count_nonzero((survived_column == '1') & (clase == '3')& (men_may == '0'))

totalmayores1 =  str(round((sup_mayores1/totalclase1*100),2)).replace('.',',')+ "%"
totalmayores2 =  str(round((sup_mayores2/totalclase2*100),2)).replace('.',',')+ "%"
totalmayores3 =  str(round((sup_mayores3/totalclase3*100),2)).replace('.',',')+ "%"

porcentaje_mayores1 = ([["Supervivientes mayores clase 1:", totalmayores1 ,'', '', '', '', '', '', '', '', '', '', '']])
porcentaje_mayores2 = ([["Supervivientes mayores clase 2:", totalmayores2 ,'', '', '', '', '', '', '', '', '', '', '']])
porcentaje_mayores3 = ([["Supervivientes mayores clase 3:", totalmayores3 ,'', '', '', '', '', '', '', '', '', '', '']])

completo = np.concatenate((completo, porcentaje_mayores1, porcentaje_mayores2, porcentaje_mayores3, vacio))




print("FIN")
carpeta = 'C:/proyectos/CM/pruebas_practicas/numpy/ejercicio57/'
np.savetxt(carpeta + "resultados.csv", completo, delimiter=';', fmt=['%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'])

