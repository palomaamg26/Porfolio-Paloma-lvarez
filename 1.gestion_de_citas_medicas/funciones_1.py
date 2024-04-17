import mysql.connector
import datetime
import os


###########################################################################################################
# 1. Una función que permita generar la base de datos en MySQL y cargue, si existe, el fichero citas.csv.

def crear_bd (cursor1, conexion1, carpeta):
    
    # crear la BD 
    cursor1.execute("CREATE database if NOT exists ejercicio_final character set latin1 collate latin1_spanish_ci;")
    cursor1.execute("USE ejercicio_final;")

    cursor1.execute("CREATE TABLE IF NOT EXISTS citas (numero_cita int PRIMARY KEY AUTO_INCREMENT,\
                    nif varchar(9) NOT NULL, \
                    fecha datetime NOT NULL, \
                    especialidad varchar (25) NOT NULL, \
                    cita_activa boolean default True NOT NULL);")
    

    # generar el fichero
    cursor1.execute ('SELECT * from citas')

    with open(carpeta + "citas.csv", mode="w") as mensaje:
        longitud = 0                        #antes de crear la escritura, inicio la variable donde voy a contar cuantos registros tiene la tabla
        tabla = list()
        cabecera = 'Numero cita; NIF; Fecha; Especialidad; Cita activa'
        mensaje.write(cabecera+'\n')
        for fila in cursor1:                #ya esta ordenado por filas (aparecen el nº de campos del select) ==i
            ancho = len(fila)               #esta variable tiene lo que mide la fila (longitud de la fila, aparecen el nº de registros del select) ==j
            tabla.append(fila)              
            longitud += 1  
        for i in range(longitud):           #en la longitud (nº de registros))
            linea = ""                      #creo un campo vacio para meter los registros de cada campo
            for j in range(ancho):          #en las posiciones de los campos de la fila en la longitud del ancho de la fila
                linea = linea + str(tabla[i][j]) + ";"      #añado los valores separados por un tabulador en el campo que he creado
            mensaje.write(linea+'\n')
    
    conexion1.commit()



###########################################################################################################
###########################################################################################################
# 2. Una función que permita añadir una cita a la base de datos. Se deberá controlar que no existe una cita similar previa posterior a la fecha actual.


###########################################################################################################
# FUNCIONES PARA COMPROBAR DATOS

def validar_dni_nie(documento):
    documento = documento.replace(" ", "")      # eliminar espacios en blanco 
    
    if len(documento) == 9 and documento[:8].isdigit() and documento[8].isalpha():         # comprobar si es DNI
        letras_dni = "TRWAGMYFPDXBNJZSQVHLCKE"
        dni = documento[:-1]
        letra = documento[-1]
        try:
            if letra == letras_dni[int(dni) % 23]:
                return True
            else:
                return False
        except:
            return False
    
        
    elif len(documento) == 9 and documento[0] in "XYZ" and documento[1:8].isdigit() and documento[8].isalpha():     # comprobar si es NIE
        letras_nie = "TRWAGMYFPDXBNJZSQVHLCKE"
        nie_tipo = documento[0]
        nie_numero = documento[1:-1]
        nie_letra = documento[-1]
        try:
            if nie_tipo == "X":             # Convertir el primer dígito del NIE al equivalente de DNI para la verificación
                dni = "0" + nie_numero
            elif nie_tipo == "Y":
                dni = "1" + nie_numero
            elif nie_tipo == "Z":
                dni = "2" + nie_numero
            if nie_letra == letras_nie[int(dni) % 23]:
                return True
            else:
                return False
        except:
            return False
    
    else:
        return False        # Si no es ni DNI ni NIE, devolver False
    


def f_comprobarfecha(fecha):

    hoy = datetime.datetime.now()
    # un_dia = datetime.timedelta(days=1)
    # nueva_fecha = hoy - un_dia
    # nueva_fecha = nueva_fecha.strftime('%d/%m/%Y %H:%M')

    try:
        fecha = datetime.datetime.strptime(fecha, '%Y/%m/%d %H:%M')
    except:
        print("Formato de fecha incorrecto. Debe ser aaaa/mm/dd hh:mm")
        return False

    if fecha < hoy:
        print("La fecha no puede ser anterior a la fecha de hoy")
        return False
    else:
        return fecha



def especialidad_check (valor, lista):
    if valor not in lista:
        print('La especialidad introducina no es válida')
        return False
    else:
        return True


# comprobar si hay datos o no en la BD con los parametros que se han pasado
def comprobar_datos (cursor1):
    longitud = 0                        #antes de crear la escritura, inicio la variable donde voy a contar cuantos registros tiene la tabla
    tabla = list()

    for fila in cursor1:                #ya esta ordenado por filas (aparecen el nº de campos del select) ==i
        ancho = len(fila)               #esta variable tiene lo que mide la fila (longitud de la fila, aparecen el nº de registros del select) ==j
        tabla.append(fila)              
        longitud += 1 
    return longitud


###########################################################################################################
# FUNCIONES PARA INTODUCIR DATOS
    
def introducir_dni (testigo):

    while not testigo:
        dni = input('\nIntroduzca el NIF: ').upper()
        if validar_dni_nie(dni):
            print("El DNI/NIE es válido.")
            testigo = True
        else:
            print("El DNI/NIE no es válido.")
            testigo = False

    return dni


def introducir_fecha (testigo):
    while not testigo:
        fecha = input('\nIntroduce una fecha y hora formato YYYY/MM/DD hh:mm : ')
        testigo = f_comprobarfecha (fecha)
    
    return fecha


def introducir_especialidad (testigo):
    especialidades_p = ['Medicina', 'Enfermería', 'Analítica', 'Vacunación', 'Otras gestiones']
    especialidades = ['medicina', 'enfermería', 'analítica', 'vacunación', 'otras gestiones', 'enfermeria', 'analitica', 'vacunacion']
    while not testigo:
        print(', '.join(especialidades_p))

        especialidad = input('\nIntroduce la especialidad: ').lower()
        testigo = especialidad_check (especialidad, especialidades)

        if especialidad == 'enfermería' or especialidad =='enfermeria':
            especialidad =='enfermeria'
        elif especialidad == 'analítica' or especialidad =='analitica':
            especialidad =='analitica' 
        elif especialidad == 'vacunación' or especialidad =='vacunacion':
            especialidad =='vacunacion' 
    return especialidad








###########################################################################################################


# cita activa = 1 o true (son validas)

def comprobar_cita(cursor1, fecha, especialidad):
    cursor1.execute(f"SELECT * FROM citas WHERE fecha = '{fecha}' AND especialidad = '{especialidad}' AND cita_activa = True")
    longitud = 0                        #antes de crear la escritura, inicio la variable donde voy a contar cuantos registros tiene la tabla
    tabla = list()

    for fila in cursor1:                #ya esta ordenado por filas (aparecen el nº de campos del select) ==i
        ancho = len(fila)               #esta variable tiene lo que mide la fila (longitud de la fila, aparecen el nº de registros del select) ==j
        tabla.append(fila)              
        longitud += 1  
    for i in range(longitud):           #en la longitud (nº de registros))
        linea = ""                      #creo un campo vacio para meter los registros de cada campo
        for j in range(ancho):          #en las posiciones de los campos de la fila en la longitud del ancho de la fila
            linea = linea + str(tabla[i][j]) + ";"      #añado los valores separados por un tabulador en el campo que he creado


    if longitud!=0:
        return False
    else:
        return True

   


def agregar_cita(cursor1, conexion1, dni, fecha, especialidad):
    testigo =comprobar_cita(cursor1, fecha, especialidad)
    
    if testigo == True:
        cursor1.execute("""
            INSERT INTO citas (nif, fecha, especialidad, cita_activa)
            VALUES (%s, %s, %s, %s)
        """, (dni, fecha, especialidad, True))  # Marcar la cita como activa
        conexion1.commit()
        print("Cita agregada con éxito.")
        return True
    elif testigo == False:
        return False






def modificar_cita (cursor1, conexion1, dni):
    fecha_anular = input('\nIntroduzca la fecha que quiera modificar (formato YYYY/MM/DD HH:MM): ')
    fecha_anular = f_comprobarfecha(fecha_anular)
    cursor1.execute(f"SELECT * FROM citas WHERE fecha = '{fecha_anular}'")
    longitud = comprobar_datos(cursor1) 

    if longitud != 0:
        testigo = False
        while not testigo:
            fecha_n = input('\nIntroduzca la fecha nueva que quiera (formato YYYY/MM/DD HH:MM): ')
            fecha_nueva = f_comprobarfecha(fecha_n)

            if fecha_nueva != False:        # si no es false, la fecha es correcta, por lo que se sigue con el codigo, si es incorrecta, termina
                cursor1.execute(f"SELECT * from citas where fecha = '{fecha_nueva}' and nif = '{dni}'")
                longitud = comprobar_datos(cursor1) 

                # comprobar si tiene cita en esa fecha y hora
                if longitud != 0:
                    print('\nYa tiene una cita asignada en esa fecha, por favor, introduzca otra fecha.')
                    testigo = False

                else:
                    # sacar la especialidad
                    cursor1.execute(f"SELECT especialidad FROM citas WHERE fecha = '{fecha_anular}'")
                    especialidad = cursor1.fetchone()[0]  # Obtiene el valor de la especialidad

                    # comprobar que la fecha que ha seleccionado en la especialidad, es una fecha valida
                    cursor1.execute(f"SELECT * from citas where fecha = '{fecha_nueva}' and especialidad ='{especialidad}' and cita_activa = '1'")
                    longitud = comprobar_datos(cursor1) 

                    if longitud != 0:       # si tiene registros, no es valida
                        print(f'\nLa fecha {fecha_nueva} para la especialidad {especialidad} no está disponible, por favor, introduzca otra fecha.')
                        testigo = False

                    else:
                        cursor1.execute(f"SELECT especialidad FROM citas WHERE fecha = '{fecha_anular}'")
                        especialidad = cursor1.fetchone()[0]  # Obtiene el valor de la especialidad

                        cursor1.execute(f"INSERT INTO citas (nif, fecha, especialidad) VALUES ('{dni}', '{fecha_nueva}', '{especialidad}')")
                        conexion1.commit()
                        cursor1.execute(f"UPDATE citas SET cita_activa = '0' WHERE fecha = '{fecha_anular}' and nif = '{dni}'")
                        conexion1.commit()

                        # Imprimir la fecha nueva
                        print(f"\nSu nueva cita se ha asiganado el {fecha_nueva} para la especialidad {especialidad}")
                    return True
    else:
        print('\nNo tiene ninguna cita asignada en esa fecha.')




def anular_cita (cursor1, conexion1, dni):
    fecha_anular = input('\nIntroduzca la fecha que quiera anular (formato YYYY/MM/DD HH:MM): ')
    fecha_anular = f_comprobarfecha(fecha_anular)
    cursor1.execute(f"SELECT * FROM citas WHERE fecha = '{fecha_anular}'")
    longitud = comprobar_datos(cursor1) 

    if longitud != 0:
        cursor1.execute(f"UPDATE citas SET cita_activa = '0' WHERE fecha = '{fecha_anular}'")
        conexion1.commit()
        cursor1.execute(f"SELECT especialidad FROM citas WHERE fecha = '{fecha_anular}'")
        especialidad = cursor1.fetchone()[0]  # Obtiene el valor de la especialidad
        print (f'Su cita {fecha_anular} para {especialidad} se ha anulado')
    
    else:
        print('\nNo tiene ninguna cita asignada en esa fecha.')

    
    return True




