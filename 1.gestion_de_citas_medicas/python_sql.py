"""
Python y MySQL

En esta programación se escribirá un programa para gestionar las citas de una consulta médica. La base de datos de citas se
almacenará en una base de datos de MySQL, y al final de la ejecución se guardardará una copia
en un fichero de nombre citas.csv. Cada cita contendrá los siguientes campos:

• Numero_cita: siendo autonumérico y clave primaria.
• Dni_Nie: de un tamaño de 9 caracteres, campo obligatorio, con verificación de si es correcto o no el dato introducido.
• Fecha: Tipo Datetime, almacenando Año, Mes, Dia, Horas y Minutos. Campo obligatorio.
• Especialidad: tamaño de 25 caracteres, admitiendo solamente los siguientes valores:
    o Medicina.
    o Enfermería.
    o Analítica.
    o Vacunación.
    o Otras gestiones.
• Cita_activa: Booleana, campo obligatorio, con valor SI/NO o True/False para controlar si la
cita está activa o no.

Es necesario que la primera fila del csv de copia contenga los nombres de los campos. El programa
debe incluir las siguientes funciones:
1. Una función que permita generar la base de datos en MySQL y cargue, si existe, el fichero citas.csv.
2. Una función que permita añadir una cita a la base de datos. Se deberá controlar que no existe una cita similar previa posterior
a la fecha actual.
"""

import mysql.connector
import datetime
import funciones_1
from funciones_1 import *
import os
os.system('cls')  





###########################################################################################################
# 1. Función que permite generar la base de datos en MySQL y cargue, si existe, el fichero citas.csv.


carpeta = "C:/proyectos/CM/pruebas_practicas/7.python_sql/ejercicio35/"

conexion1=mysql.connector.connect(host="localhost", user="root", passwd="", db="")
cursor1=conexion1.cursor()   

crear_bd (cursor1, conexion1, carpeta)



###########################################################################################################
# 2. Una función que permita añadir una cita a la base de datos. Se deberá controlar que no existe una cita similar previa posterior a la fecha actual.

testigo=False

def introducir_cita (testigo, conexion1):

    while  not testigo:
        #pedir el dni, la fecha y la especialidad para pedir cita, pasando por las fucniones
        dni = introducir_dni(testigo)
        fecha = introducir_fecha(testigo)
        if fecha != False:        # si no es false, la fecha es correcta, por lo que se sigue con el codigo, si es incorrecta, termina
            cursor1.execute(f"SELECT * from citas where fecha = '{fecha}' and nif = '{dni}'")
            longitud = comprobar_datos(cursor1) 

            # comprobar si tiene cita en esa fecha y hora
            if longitud != 0:
                print('Ya tiene una cita asignada en esa fecha, por favor, introduzca otra fecha.')
                testigo = False

            else:
                especialidad = introducir_especialidad(testigo)

                # pasar los datos por la funcion para agregar la cita a la BD
                testigo = agregar_cita(cursor1, conexion1, dni, fecha, especialidad)

                if testigo == False:
                    print('La fecha introducida no esta disponible.')
                    repetir = input ('\n¿Quiere introducir de nuevo los datos para asignar una nueva cita? (Si/No):').lower()
                    if repetir == 'si' or repetir =='sí':
                        testigo = False
                    elif repetir == 'no':
                        print('')
                        testigo = True
                    

                else:
                    print(f'Su cita {fecha} para {especialidad} ha sido asignada correctamente.')
                    repetir = input ('\n¿Quiere añadir otra cita? (Si/No):').lower()
                    testigo = True
                    if repetir == 'si' or repetir =='sí':
                        testigo = False
                    elif repetir == 'no':
                        testigo = True
                    else: 
                        testigo = False




###########################################################################################################
# 3. Función que recibe un dni y devuelva una lista con las citas de ese paciente.
                
def apartado3(cursor1):
    testigo = False
    while not testigo:
        dni = introducir_dni(testigo)
        cursor1.execute(f"SELECT fecha, especialidad FROM citas WHERE nif = '{dni}' and cita_activa = '1' ")
        longitud = comprobar_datos(cursor1) 
        if longitud != 0:
            cursor1.execute(f"SELECT fecha, especialidad FROM citas WHERE nif = '{dni}' and cita_activa = '1' ")
            print(f"\nSus citas son:")
            for fila in cursor1:
                fecha = fila[0]
                especialidad = fila[1]
                print(f"{fecha} en la especialidad {especialidad}")
                testigo =True
        else:
            print('\nNo tiene citas activas.')
            testigo = True



###########################################################################################################
# 4. Función que recibe un dni y una especialidad y permite modificar la fecha.

# 5. Función que recibe un dni y una especialidad y permite anular la cita, siempre y cuando la fecha sea posterior a la actual.
            
def apartado4y5( cursor1, conexion1):
    testigo = False
    while not testigo:
        dni = introducir_dni(testigo)
        especialidad = introducir_especialidad(testigo)
        cursor1.execute(f"SELECT fecha, especialidad FROM citas WHERE nif = '{dni}' and especialidad = '{especialidad}' and cita_activa = '1' ")
        longitud = comprobar_datos(cursor1) 
        if longitud != 0:
            cursor1.execute(f"SELECT fecha, especialidad FROM citas WHERE nif = '{dni}' and especialidad = '{especialidad}' and cita_activa = '1' ")
            print(f"\nSus citas son:")
            for fila in cursor1:
                fecha = fila[0]
                especialidad = fila[1]
                print(f"{fecha} en la especialidad {especialidad}")
            
            while not testigo:
                mod_anular = input('\n¿Quiere modificar o anular su cita? (modificar/anular): ').lower()

                if mod_anular == 'modificar':
                    testigo = modificar_cita (cursor1, conexion1, dni)

                elif mod_anular == 'anular':
                    testigo = anular_cita (cursor1, conexion1, dni)

                else:
                    print('\nRespuesta no válida')

        else:
            print('\nNo tiene citas activas.')
            testigo = True



testigo = False
while not testigo:
    accion = input ('\n¿Quieres solicitar, ver o modificar una cita? (solicitar/ver/modificar): ').lower()

    if accion == 'solicitar':
        testigo = introducir_cita(testigo, conexion1)
        crear_bd (cursor1, conexion1, carpeta)          # añadirlo despues de cada funcion para que genere el fichero con los datos nuevos
        testigo = True

    elif accion == 'ver':
        apartado3(cursor1)
        crear_bd (cursor1, conexion1, carpeta)
        testigo = True

    elif accion == 'modificar':
        apartado4y5(cursor1, conexion1)
        crear_bd (cursor1, conexion1, carpeta)
        testigo = True
    
    else:
        testigo = False




