#ejercicio 51

import mysql.connector


conexion1=mysql.connector.connect(host="localhost", user="root", passwd="", db="")
cursor1=conexion1.cursor()      


cursor1.execute("drop database if exists ejercicio51;")
cursor1.execute("CREATE database ejercicio51 character set latin1 collate latin1_spanish_ci;")
cursor1.execute("USE ejercicio51;")


cursor1.execute("CREATE TABLE ejercicio51 (dni varchar(12), \
				nombre varchar (15), \
				apellidos varchar (20), \
				direccion varchar(30), \
				poblacion varchar(20), \
                telefono varchar(9), \
				provincia varchar(20), \
				nota float );")

# Se entrega un fichero de datos llamado "ejercicio51.csv". Importar el fichero en una tabla dentro de una base de datos nueva y completar los datos que faltan insertando los campos vacíos. Implementar un programa en Python que mediante sentencias SQL rellene los campos vacíos en la base de datos.

cursor1.execute("LOAD DATA INFILE 'C:/proyectos/CM/pruebas_practicas/sql/ejercicio51/ejercicio51.csv' INTO TABLE ejercicio51\
                FIELDS TERMINATED BY  ';'  LINES TERMINATED BY '\n'; ")		

cursor1.execute("ALTER TABLE ejercicio51 ADD COLUMN if not EXISTS porcentaje_beca float, \
                ADD COLUMN if not EXISTS precio_matricula int, ADD COLUMN if not EXISTS tasas int;")
conexion1.commit()



# II. Tenemos un listado de alumnos y sus calificaciones finales, las condiciones para obtener una beca son:
    # 1. Si la calificación final esta entre 9 y 10, obtiene un 80% de beca
    # 2. Si la calificación final es inferior a 9, obtiene un 40% de beca
    # 3. Si la calificación final es inferior a 7, obtiene un 25% de beca
    # 4. Si la calificación final es inferior a 5, no se otorga beca.


cursor1.execute("ALTER TABLE ejercicio51 ADD COLUMN if not EXISTS porcentaje_beca float, \
                ADD COLUMN if not EXISTS precio_matricula int,\
                ADD COLUMN if not EXISTS tasas int;")
conexion1.commit()


cursor1.execute("update ejercicio51 set ejercicio51.porcentaje_beca = 0.8 WHERE nota >= 9;")
cursor1.execute("update ejercicio51 set ejercicio51.porcentaje_beca = 0.4 WHERE nota >= 7 and nota < 9 ;")
cursor1.execute("update ejercicio51 set ejercicio51.porcentaje_beca = 0.25 WHERE nota >= 5 and nota < 7 ;")
cursor1.execute("update ejercicio51 set ejercicio51.porcentaje_beca = 0 WHERE nota < 5 ;")
conexion1.commit()



# III. Los precios de la matrícula serán los siguientes:
    # 1. Si el estudiante es de Madrid, el precio serán 1200 euros.
    # 2. Si el estudiante es de Andalucía (Jaén o Málaga), el precio serán 1000 euros. 
    # 3. Si el estudiante es de Castilla y León (Salamanca o Soria), el precio serán 1100 euros.
    # 4. Si el estudiante es de Castilla La Mancha (Guadalajara o Toledo), el precio serán 900 euros.
    # 5. Para el resto de provincias el precio será de 1150 euros.


cursor1.execute("UPDATE ejercicio51 SET precio_matricula = 1200 WHERE provincia = 'Madrid';")
cursor1.execute("UPDATE ejercicio51 SET precio_matricula = 1000 WHERE provincia IN ('Jaén', 'Málaga');")
cursor1.execute("UPDATE ejercicio51 SET precio_matricula = 1100 WHERE provincia IN ('Salamanca', 'Soria');")
cursor1.execute("UPDATE ejercicio51 SET precio_matricula = 900 WHERE provincia IN ('Guadalajara', 'Toledo');")
cursor1.execute("UPDATE ejercicio51 SET precio_matricula = 900 WHERE provincia \
                NOT IN ('Guadalajara', 'Toledo', 'Salamanca', 'Soria', 'Jaén', 'Málaga', 'Madrid');")
conexion1.commit()


# IV. Los precios de las tasas serán los siguientes:
    # 1. Si el estudiante es de Madrid, el precio serán 100 euros.
    # 2. Si el estudiante es de Valencia, Asturias o Teruel, el precio serán 50 euros.
    # 3. Para el resto de provincias el precio será de 150 euros.

cursor1.execute("UPDATE ejercicio51 SET tasas = 100 WHERE poblacion = 'Madrid';")
cursor1.execute("UPDATE ejercicio51 SET tasas = 50 WHERE poblacion IN ('Valencia', 'Asturias', 'Teruel');")
cursor1.execute("UPDATE ejercicio51 SET tasas = 150 WHERE poblacion \
                NOT IN ('Valencia', 'Asturias', 'Teruel', 'Madrid');")
conexion1.commit()



# V. Calcular el precio final aplicando al precio de la matrícula el descuento de la beca, y sumándole las tasas correspondientes.

cursor1.execute("ALTER TABLE ejercicio51 ADD COLUMN if not EXISTS precio_final float;")
conexion1.commit()

cursor1.execute("UPDATE ejercicio51 SET precio_final = (precio_matricula-(precio_matricula * porcentaje_beca)) + tasas;")
conexion1.commit()







# VI. Una vez rellenados todos los campos generar los siguientes ficheros de salida:

    # Testear los datos de dni/NIE y teléfono, guardando en el fichero errores.csv todos aquellos alumnos cuyos datos tengan errores.

cursor1.execute("SELECT * FROM ejercicio51;")
encabezado = "DNI; NOMBRE; APELLIDOS; DIRECCIÓN; POBLACIÓN; TELÉFONO; PROVINCIA; NOTA; PORCENTAJE BECA;\
            PRECIO MATRICULA; TASAS; PRECIO FINAL; \n"

carpeta = "C:/proyectos/CM/pruebas_practicas/sql/ejercicio51/"
letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']


with open(carpeta + "errores.csv", mode="w") as mensaje:
    mensaje.write(encabezado)  # Escribir el encabezado en el archivo

    # Recorrer los resultados de la consulta
    for fila in cursor1:
        telefono = fila[5]  # Obtener el valor del campo de teléfono
        
        testigo = True  # Inicializar la variable testigo        

        # Verificar si el teléfono es un fijo válido 
        if telefono[0] != '8' and telefono[0] != '9' and telefono[0] != '6' and telefono[0] != '7':
            for x in range(len(telefono)):
                numero = ord(telefono[x])
                linea=""
                if numero >= 48 and numero <= 57:
                    for valor in fila:
                        a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                        if valor in a:
                            valor1=(str(valor)).replace(".",",")
                            linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                        else:
                            linea = linea + str(valor) + ";"  # Crear la línea de datos
                else:
                    for valor in fila:
                        a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                        if valor in a:
                            valor1=(str(valor)).replace(".",",")
                            linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                        else:
                            linea = linea + str(valor) + ";"  # Crear la línea de datos
            linea=linea+ '\n'
            if linea!= "\n":
                mensaje.write(linea)  # Escribir la línea en el archivo
        else:
            for x in range(len(telefono)):
                numero = ord(telefono[x])
                linea=""
                if numero < 48 and numero > 57:             #si es  fijo o movil con caracteres!= a numeros 
                    for valor in fila:
                        a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                        if valor in a:
                            valor1=(str(valor)).replace(".",",")
                            linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                        else:
                            linea = linea + str(valor) + ";"  # Crear la línea de datos
            linea=linea+ '\n'
            if linea!= "\n":
                mensaje.write(linea)  # Escribir la línea en el archivo


        letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']
        nif = fila[0]  # Obtener el valor del campo del DNI
        numero1= nif[0:1]
        letra=nif[8:]
        codigo= ord(numero1)

        if (codigo>=48) and (codigo<=57):       # los numeros se encuentran entre los valores 48 y 57 del codigo ascii:
            contador=0
            dni=""

            for x in range(len(nif)-1):                   # recorremos el dni
                numero= ord(nif[x])                     # pasamos cada caracter del dni al nº correspondiente del codigo ascii
                linea=""
                if (numero<48) and (numero>57): 
                    for valor in fila:
                        a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                        if valor in a:
                            valor1=(str(valor)).replace(".",",")
                            linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                        else:
                            linea = linea + str(valor) + ";"  # Crear la línea de datos

                elif (numero>=48) and (numero<=57):       # si los numeros corresponden a ese rango en ascii (numeros del 1 al 9)
                    dni=dni+nif[x]                      # se ejecuta
                    contador+=1
                resto=int(dni) % 23                 # calculamos el resto para poder sacar la letra del DNI proporcionado
                letra_final=letrasresto[resto]      # la letra correspone a la posicion del resto que hemos sacado en el array de letras

            if letra!=letra_final:             # si la letra que nos ha dado el usuario no coincide con la que hemos sacado
                for valor in fila:
                    a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                    if valor in a:
                        valor1=(str(valor)).replace(".",",")
                        linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                    else:
                        linea = linea + str(valor) + ";"  # Crear la línea de datos
            linea=linea+ '\n'



        nif = fila[0]  # Obtener el valor del campo del DNI
        letra = nif [0:1]
        numero =nif [1:8]
        letra2=nif[8:]
        letra = letra.upper()
        letra2 = letra2.upper()
        testigo = True  # Inicializar la variable testigo
        
        codigo= ord(letra)      # devuelve el codigo ascii de la letra

        letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']

        if (codigo>=88) and (codigo<=90):         # los numeros se encuentran entre los valores 88 y 90 del codigo ascii (son XYZ)
            contador=0
            dni=""
            nie = nif [1:8]                         # quitamos el primer caracter ya que es una letra y no un numero
            
            for x in range(len(nie)):               # recorremos el nie
                numero= ord(nie[x])                 # pasamos a ascii
                linea=""
                if (numero<48) and (numero>57):
                    for valor in fila:
                        a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                        if valor in a:
                            valor1=(str(valor)).replace(".",",")
                            linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                        else:
                            linea = linea + str(valor) + ";"  # Crear la línea de datos
                elif (numero>=48) and (numero<=57):   # si son numeros 
                    dni=dni+nie[x]                  # creamos el nie
                    contador+=1
                    if letra == "Y":                # sumamos lo correspondiente a cada letra
                        valor=10000000
                    elif letra== "Z":
                        valor=20000000
                    else:
                        valor=0
                    resto=(int(dni)+ valor) % 23       # calculamos el resto
                    letrafinal2= letrasresto[resto]    # la letra correspone a la posicion del resto que hemos sacado en el array de letras
               
            if letra2!=letrafinal2:     # fuera del for porque si no, cada vuelta que dé, imprimira false, ya que el NIE se va creando 
                for valor in fila:
                    a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                    if valor in a:
                        valor1=(str(valor)).replace(".",",")
                        linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                    else:
                        linea = linea + str(valor) + ";"  # Crear la línea de datos
            linea=linea+ '\n'

        if len(linea) == 0:
            print(linea)

       
        if linea!= "\n":
            mensaje.write(linea)  # Escribir la línea en el archivo



# En el fichero fijos.csv guardar todos aquellos alumnos SIN ERRORES cuyo teléfono sea un fijo.

cursor1.execute("SELECT * FROM ejercicio51;")


carpeta = "C:/proyectos/CM/pruebas_practicas/sql/ejercicio51/"

with open(carpeta + "fijos.csv", mode="w") as mensaje:
    mensaje.write("DNI; NOMBRE; APELLIDOS; DIRECCIÓN; POBLACIÓN; TELÉFONO; PROVINCIA; PORCENTAJE BECA; NOTA;")
    mensaje.write("PRECIO MATRICULA; TASAS; PRECIO FINAL\n")  # Escribir el encabezado en el archivo

    
    # Recorrer los resultados de la consulta
    for fila in cursor1:
        

        telefono = fila[5]  # Obtener el valor del campo de teléfono
        testigo = True  # Inicializar la variable testigo
  
        # Verificar si el teléfono es un fijo válido 
        if telefono[0] == '8' or telefono[0] == '9':
            for x in range(len(telefono)):
                numero = ord(telefono[x])
                linea=""

                if numero >= 48 and numero <= 57:
                    nif = fila[0]  # Obtener el valor del campo del DNI
                    numero1= nif[0:1]
                    letra=nif[8:]
                    codigo= ord(numero1)

                    if (codigo>=48) and (codigo<=57):       # los numeros se encuentran entre los valores 48 y 57 del codigo ascii:
                        contador=0
                        dni=""
                        for x in range(len(nif)-1):                   # recorremos el dni
                            numero= ord(nif[x])                     # pasamos cada caracter del dni al nº correspondiente del codigo ascii
                            if (numero>=48) and (numero<=57):       # si los numeros corresponden a ese rango en ascii (numeros del 1 al 9)
                                dni=dni+nif[x]                      # se ejecuta
                                contador+=1
                                resto=int(dni) % 23                 # calculamos el resto para poder sacar la letra del DNI proporcionado
                                letra_final=letrasresto[resto]      # la letra correspone a la posicion del resto que hemos sacado en el array de letras

                        if letra==letra_final:             # si la letra que nos ha dado el usuario no coincide con la que hemos sacado
                            for valor in fila:
                                a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                                if valor in a:
                                    valor1=(str(valor)).replace(".",",")
                                    linea = linea + str(valor1) + ";"  # Crear la línea de datos
                                else:
                                   linea = linea + str(valor) + ";"  # Crear la línea de datos

                    nif = fila[0]  # Obtener el valor del campo del DNI
                    letra = nif [0:1]
                    numero =nif [1:8]
                    letra2=nif[8:]
                    letra = letra.upper()
                    letra2 = letra2.upper()
                    
                    codigo= ord(letra)      # devuelve el codigo ascii de la letra

                    letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']

                    if (codigo>=88) and (codigo<=90):         # los numeros se encuentran entre los valores 88 y 90 del codigo ascii (son XYZ)
                        contador=0
                        dni=""
                        nie = nif [1:8]                         # quitamos el primer caracter ya que es una letra y no un numero
                        
                        for x in range(len(nie)):               # recorremos el nie
                            numero= ord(nie[x])                 # pasamos a ascii
                            if (numero>=48) and (numero<=57):   # si son numeros 
                                dni=dni+nie[x]                  # creamos el nie
                                contador+=1
                                if letra == "Y":                # sumamos lo correspondiente a cada letra
                                    valor=10000000
                                elif letra== "Z":
                                    valor=20000000
                                else:
                                    valor=0
                                resto=(int(dni)+ valor) % 23       # calculamos el resto
                                letrafinal2= letrasresto[resto]    # la letra correspone a la posicion del resto que hemos sacado en el array de letras

                        if letra2==letrafinal2:     # fuera del for porque si no, cada vuelta que dé, imprimira false, ya que el NIE se va creando 
                            for valor in fila:
                                a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                                if valor in a:
                                    valor1=(str(valor)).replace(".",",")                                   
            
                                    linea = linea + str(valor1) + ";"  # Crear la línea de datos
                                else:
                                   linea = linea + str(valor) + ";"  # Crear la línea de datos
            if linea != "":
                mensaje.write(linea + '\n')  # Escribir la línea en el archivo




# en el fichero movil.csv guardar todos aquellos alumnos SIN ERRORES cuyo teléfono sea un móvil.

cursor1.execute("SELECT * FROM ejercicio51;")
encabezado = "DNI; NOMBRE; APELLIDOS; DIRECCIÓN; POBLACIÓN; TELÉFONO; PROVINCIA; NOTA; PORCENTAJE BECA;\
            PRECIO MATRICULA; TASAS; PRECIO FINAL; \n"

carpeta = "C:/proyectos/CM/pruebas_practicas/sql/ejercicio51/"

with open(carpeta + "movil.csv", mode="w") as mensaje:
    mensaje.write(encabezado)  # Escribir el encabezado en el archivo

    # Recorrer los resultados de la consulta
    for fila in cursor1:
        
        telefono = fila[5]  # Obtener el valor del campo de teléfono
        testigo = True  # Inicializar la variable testigo


        # Verificar si el teléfono es un móvil válido (comienza con 6 o 7)
        if telefono[0] == '6' or telefono[0] == '7':
            for x in range(len(telefono)):
                numero = ord(telefono[x])
                linea=""
                if numero >= 48 and numero <= 57:
                    nif = fila[0]  # Obtener el valor del campo del DNI
                    testigo = True  # Inicializar la variable testigo
                    numero1= nif[0:1]
                    letra=nif[8:]
                    codigo= ord(numero1)
                    testigo = True  # Inicializar la variable testigo

                    if (codigo>=48) and (codigo<=57):       # los numeros se encuentran entre los valores 48 y 57 del codigo ascii:
                        contador=0
                        dni=""
                        for x in range(len(nif)-1):                   # recorremos el dni
                            numero= ord(nif[x])                     # pasamos cada caracter del dni al nº correspondiente del codigo ascii
                            if (numero>=48) and (numero<=57):       # si los numeros corresponden a ese rango en ascii (numeros del 1 al 9)
                                dni=dni+nif[x]                      # se ejecuta
                                contador+=1
                                resto=int(dni) % 23                 # calculamos el resto para poder sacar la letra del DNI proporcionado
                                letra_final=letrasresto[resto]      # la letra correspone a la posicion del resto que hemos sacado en el array de letras

                        if letra==letra_final:             # si la letra que nos ha dado el usuario no coincide con la que hemos sacado
                            for valor in fila:
                                a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                                if valor in a:
                                    valor1=(str(valor)).replace(".",",")
                                    linea = linea + str(valor1) + ";"  # Crear la línea de datos 
                                else:
                                   linea = linea + str(valor) + ";"  # Crear la línea de datos


                    nif = fila[0]  # Obtener el valor del campo del DNI
                    letra = nif [0:1]
                    numero =nif [1:8]
                    letra2=nif[8:]
                    letra = letra.upper()
                    letra2 = letra2.upper()
                    testigo = True  # Inicializar la variable testigo
                    
                    codigo= ord(letra)      # devuelve el codigo ascii de la letra

                    letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']

                    if (codigo>=88) and (codigo<=90):         # los numeros se encuentran entre los valores 88 y 90 del codigo ascii (son XYZ)
                        contador=0
                        dni=""
                        nie = nif [1:8]                         # quitamos el primer caracter ya que es una letra y no un numero
                        
                        for x in range(len(nie)):               # recorremos el nie
                            numero= ord(nie[x])                 # pasamos a ascii
                            if (numero>=48) and (numero<=57):   # si son numeros 
                                dni=dni+nie[x]                  # creamos el nie
                                contador+=1
                                if letra == "Y":                # sumamos lo correspondiente a cada letra
                                    valor=10000000
                                elif letra== "Z":
                                    valor=20000000
                                else:
                                    valor=0
                                resto=(int(dni)+ valor) % 23       # calculamos el resto
                                letrafinal2= letrasresto[resto]    # la letra correspone a la posicion del resto que hemos sacado en el array de letras

                        if letra2==letrafinal2:     # fuera del for porque si no, cada vuelta que dé, imprimira false, ya que el NIE se va creando 
                            for valor in fila:
                                if valor == fila[7] or valor == fila[8] or valor == fila[11]:
                                    valor1=(str(valor)).replace(".",",")
                                    linea = linea + str(valor1) + ";"  # Crear la línea de datos
                                    
                                else:
                                    linea = linea + str(valor) + ";"  # Crear la línea de datos                              
                                    
            if linea != "":
                mensaje.write(linea + '\n')  # Escribir la línea en el archivo

                
#linea = "; ".join(str(valor) for valor in fila) + "\n"  # Crear la línea de datos


# En el fichero listado_dni.csv guardar todos aquellos alumnos SIN ERRORES que tengan dni.

cursor1.execute("SELECT * FROM ejercicio51;")
encabezado = "DNI; NOMBRE; APELLIDOS; DIRECCIÓN; POBLACIÓN; TELÉFONO; PROVINCIA; NOTA; PORCENTAJE BECA;\
            PRECIO MATRICULA; TASAS; PRECIO FINAL; \n"

carpeta = "C:/proyectos/CM/pruebas_practicas/sql/ejercicio51/"


with open(carpeta + "listado_dni.csv", mode="w") as mensaje:
    mensaje.write(encabezado)  # Escribir el encabezado en el archivo
    

    # Recorrer los resultados de la consulta
    for fila in cursor1:
        nif = fila[0]  # Obtener el valor del campo del DNI
        numero1= nif[:1]
        letra=nif[8:]
        codigo= ord(numero1)

        letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']
        

        if (codigo>=48) and (codigo<=57):       # los numeros se encuentran entre los valores 48 y 57 del codigo ascii:
            contador=0
            dni=""
            
            for x in range(len(nif)-1):                   # recorremos el dni
                numero= ord(nif[x])                     # pasamos cada caracter del dni al nº correspondiente del codigo ascii
                
                if (numero>=48) and (numero<=57):       # si los numeros corresponden a ese rango en ascii (numeros del 1 al 9)
                    dni=dni+nif[x]                      # se ejecuta
                    contador+=1
            resto=int(dni) % 23                 # calculamos el resto para poder sacar la letra del DNI proporcionado
            letra_final=letrasresto[resto]      # la letra correspone a la posicion del resto que hemos sacado en el array de letras

            if letra==letra_final:             # si la letra que nos ha dado el usuario no coincide con la que hemos sacado
                telefono = fila[5]  # Obtener el valor del campo de teléfono
                
                # Verificar si el teléfono es un fijo o movil válido 
                if telefono[0] == '8' or telefono[0] == '9' or telefono[0] == '6' or telefono[0] == '7':
                    for x in range(len(telefono)):
                        numero = ord(telefono[x])
                        linea=""
                        if numero >= 48 and numero <= 57:
                            for valor in fila:
                                a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                                if valor in a:
                                    valor1=(str(valor)).replace(".",",")
                                    linea = linea + str(valor1) + ";"  # Crear la línea de datos                              
                                else:
                                   linea = linea + str(valor) + ";"  # Crear la línea de datos
                    if linea != "":
                        mensaje.write(linea + '\n')  # Escribir la línea en el archivo




# En el fichero listado_nie.csv guardar todos aquellos alumnos SIN ERRORES que tengan NIE.

cursor1.execute("SELECT * FROM ejercicio51;")
encabezado = "DNI; NOMBRE; APELLIDOS; DIRECCIÓN; POBLACIÓN; TELÉFONO; PROVINCIA; NOTA; PORCENTAJE BECA;\
            PRECIO MATRICULA; TASAS; PRECIO FINAL; \n"

carpeta = "C:/proyectos/CM/pruebas_practicas/sql/ejercicio51/"

letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']

with open(carpeta + "listado_nie.csv", mode="w") as mensaje:
    mensaje.write(encabezado)  # Escribir el encabezado en el archivo

    # Recorrer los resultados de la consulta
    for fila in cursor1:
        nif = fila[0]  # Obtener el valor del campo del DNI
        letra = nif [0:1]
        numero =nif [1:8]
        letra2=nif[8:]
        letra = letra.upper()
        letra2 = letra2.upper()
        testigo = True  # Inicializar la variable testigo
        
        codigo= ord(letra)      # devuelve el codigo ascii de la letra

        letrasresto=['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']
        linea=""

        if (codigo>=88) and (codigo<=90):         # los numeros se encuentran entre los valores 88 y 90 del codigo ascii (son XYZ)
                contador=0
                dni=""
                nie = nif [1:8]                         # quitamos el primer caracter ya que es una letra y no un numero
                
                for x in range(len(nie)):               # recorremos el nie
                    numero= ord(nie[x])                 # pasamos a ascii
                    if (numero>=48) and (numero<=57):   # si son numeros 
                        dni=dni+nie[x]                  # creamos el nie
                        contador+=1
                        if letra == "Y":                # sumamos lo correspondiente a cada letra
                            valor=10000000
                        elif letra== "Z":
                            valor=20000000
                        else:
                            valor=0
                        resto=(int(dni)+ valor) % 23       # calculamos el resto
                        letrafinal2= letrasresto[resto]    # la letra correspone a la posicion del resto que hemos sacado en el array de letras

                if letra2==letrafinal2:     # fuera del for porque si no, cada vuelta que dé, imprimira false, ya que el NIE se va creando 
                   
                    telefono = fila[5]  # Obtener el valor del campo de teléfono
                    testigo = True  # Inicializar la variable testigo

                    # Verificar si el teléfono es un fijo válido 
                    if telefono[0] == '8' or telefono[0] == '9':
                        for x in range(len(telefono)):
                            numero = ord(telefono[x])
                            linea=""
                            if numero >= 48 and numero <= 57:
                                for valor in fila:
                                    a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                                    if valor in a:
                                        valor1=(str(valor)).replace(".",",")
                                        linea = linea + str(valor1) + ";"  # Crear la línea de datos
                                        
                                    else:
                                        linea = linea + str(valor) + ";"  # Crear la línea de datos
                        if linea != "":
                            mensaje.write(linea + '\n')  # Escribir la línea en el archivo

                    telefono = fila[5]  # Obtener el valor del campo de teléfono

                    # Verificar si el teléfono es un móvil válido (comienza con 6 o 7)
                    if telefono[0] == '6' or telefono[0] == '7':
                        for x in range(len(telefono)):
                            numero = ord(telefono[x])
                            linea=""
                            if numero >= 48 and numero <= 57:
                                for valor in fila:
                                    a= (fila [7], fila[8], fila [9], fila[10], fila[11])
                                    if valor in a:
                                        valor1=(str(valor)).replace(".",",")
                                        linea = linea + str(valor1) + ";"  # Crear la línea de datos
                                        
                                    else:
                                        linea = linea + str(valor) + ";"  # Crear la línea de datos
                        if linea != "":
                            mensaje.write(linea + '\n')  # Escribir la línea en el archivo


