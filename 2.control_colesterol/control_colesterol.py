"""
Uso de MatPlotLib y SciPy


El fichero “control_colesterol.csv" tiene la información anónima de un estudio de 60 pacientes donde
se indica su edad, peso, estatura y niveles de colesterol. Crear un programa que realice las siguientes
operaciones utilizando las librerías NumPy, Pandas, SciPy y Matplotlib:

1. Crear un DataFrame indexado por ID de cliente y ajustar los valores numéricos a formato
decimal con dos decimales. Guardarlo en el fichero apartado4_1.csv.

2. Calcular la media, mediana, moda, los percentiles 30, 60 y 90, el rango, IQR, coeficiente de
variación, varianza y desviación típica de la edad, peso, altura y nivel de colesterol para todo
el estudio redondeando los cálculos a 2 decimales. Mostrar los datos por terminal y guardar
la información en el fichero apartado4_2_3.csv.

3. Repetir los cálculos del apartado anterior diferenciando por sexo (H / M). Mostrar los datos
por terminal y añadir todos estos cálculos con los anteriores en el fichero de salida
apartado4_2_3.csv.

4. El riesgo de que una persona sufra enfermedades coronarias depende de su edad y su índice
de masa corporal. El índice de masa corporal es la división entre el peso del individuo en kilos
y el cuadrado de su estatura en metros:

Añadir al DataFrame dos columnas, IMC y Riesgo, y rellenarlas a partir de los datos de estatura,
el peso y la edad de una persona. Generar un fichero apartado4_4.csv con el DataFrame
incluyendo las nuevas columnas.


5. Para establecer la relación entre el nivel de colesterol y el IMC vamos a realizar una función a
la que se le pase el Dataframe anterior y realice los siguientes cálculos diferenciando por
sexos:
• Covarianza de los valores de colesterol y el IMC.
• Coeficientes de la recta de regresión de IMC sobre los valores de colesterol.
• Diagramas de dispersión y la recta de regresión de ambas variables.

Guardar los datos en los ficheros apartado5_5.csv, incluyendo los datos calculados para Hombres y para Mujeres.

Generar y guardar dos diagramas con la dispersión y recta de regresión apartado5_5H.png
y apartado5_5M.png incluyendo título, leyenda, etc…


"""
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as ss


carpeta = 'C:/proyectos/CM/pruebas_practicas/7.ejercicio_final/ejercicio4/'

# APARTADO 1
##################################################################################################################
tabla = pd.read_csv('C:/proyectos/CM/pruebas_practicas/7.ejercicio_final/ejercicio4/control_colesterol.csv', sep='\t', decimal=',')

tabla.set_index('id', inplace=True)             # hay que poner inplace = True

columnas_numericas = ['peso', 'altura', 'colesterol']
tabla[columnas_numericas] = tabla[columnas_numericas].round(2)

tabla.to_csv('C:/proyectos/CM/pruebas_practicas/ejercicio72/apartado4_1.csv', sep=';', decimal=',')





# APARTADO 2
##################################################################################################################

with open(carpeta + 'apartado4_2_3.csv', mode="w") as mensaje:
        mensaje.write("EJERCICIO 4, APARTADO 2")

def escribir_archivo(valor, nombre_valor, carpeta):
    with open(carpeta + 'apartado4_2_3.csv', mode="a") as mensaje:
        mensaje.write(f'\n\nValores de {nombre_valor}\n')
        mensaje.write(f'Media:; {round(valor.mean(), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Percentil 30:; {round(valor.quantile(0.3), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Rango:; {round(valor.max() - valor.min(), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Varianza:; {round(valor.var(ddof=0), 2).astype(str).replace('.', ',')}\n')
        mensaje.write(f'Mediana:; {round(valor.median(), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Percentil 60:; {round(valor.quantile(0.6), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'IQR; {round(valor.quantile(0.75)- valor.quantile(0.25), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Desviacion tipica:; {round(valor.std(ddof= 0), 2).astype(str).replace('.', ',')}\n')
        moda_p = valor.mode()
        modas_p = moda_p.tolist()
        if len(modas_p) == 1:
            mensaje.write(f'Moda:; {str(modas_p[0]).replace(".", ",")};')
        else:
            mensaje.write(f'Modas:; {"/".join(map(str, modas_p)).replace('.', ',')};')        
        mensaje.write(f'Percentil 90:; {round(valor.quantile(0.9), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Covarianza:; {round(ss.variation(valor), 2).astype(str).replace('.', ',')}\n')

        print(f'\nValores de: {nombre_valor}')
        print(f'Media: {round(valor.mean(), 2)}')
        print(f'Medina: {round(valor.median(), 2)}')
        if len(modas_p) == 1:
            print(f'Moda: {modas_p[0]}')
        else:
            print(f'Modas: {", ".join(map(str, modas_p))}')
        print(f'Percentil 30: {round(valor.quantile(0.3), 2)}')
        print(f'Percentil 60: {round(valor.quantile(0.6), 2)}')
        print(f'Percentil 90: {round(valor.quantile(0.9), 2)}')
        print(f'Rango: {round(valor.max() - valor.min(), 2)}')
        print(f'IQR {round(valor.quantile(0.75)- valor.quantile(0.25), 2)}')
        print(f'Covarianza: {round(ss.variation(valor), 2)}')
        print(f'Varianza: {round(valor.var(), 2)}')
        print(f'Desviacion tipica: {round(valor.std(), 2)}')

edad = tabla['edad']
peso = tabla['peso']
altura = tabla['altura']
colesterol = tabla['colesterol']    

escribir_archivo(edad, 'edad', carpeta)
escribir_archivo(peso, 'peso', carpeta)
escribir_archivo(altura, 'altura', carpeta)
escribir_archivo(colesterol, 'colesterol', carpeta)






# APARTADO 3
##################################################################################################################

hombres = tabla[tabla['sexo'] == 'H']
mujeres = tabla[tabla['sexo'] == 'M']


with open(carpeta + 'apartado4_2_3.csv', mode="a") as mensaje:
        mensaje.write("\n\n\nEJERCICIO 4, APARTADO 3\n")

def escribir_archivo(sexo, valor, nombre_valor, carpeta):
    with open(carpeta + 'apartado4_2_3.csv', mode="a") as mensaje:
        mensaje.write(f'\nValores de {nombre_valor} en {sexo}\n')
        mensaje.write(f'Media:; {round(valor.mean(), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Percentil 30:; {round(valor.quantile(0.3), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Rango:; {round(valor.max() - valor.min(), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Varianza:; {round(valor.var(ddof = 0), 2).astype(str).replace('.', ',')}\n')
        mensaje.write(f'Mediana:; {round(valor.median(), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Percentil 60:; {round(valor.quantile(0.6), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'IQR; {round(valor.quantile(0.75)- valor.quantile(0.25), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Desviacion tipica:; {round(valor.std(ddof = 0), 2).astype(str).replace('.', ',')}\n')
        moda_p = valor.mode()
        modas_p = moda_p.tolist()
        if len(modas_p) == 1:
            mensaje.write(f'Moda:; {str(modas_p[0]).replace(".", ",")};')
        else:
            mensaje.write(f'Modas:; {"/".join(map(str, modas_p)).replace('.', ',')};')        
        mensaje.write(f'Percentil 90:; {round(valor.quantile(0.9), 2).astype(str).replace('.', ',')};')
        mensaje.write(f'Covarianza:; {round(ss.variation(valor), 2).astype(str).replace('.', ',')}\n')
        
        print(f'\nValores de {nombre_valor} en {sexo}\n')
        print(f'Media: {round(valor.mean(), 2)}')
        print(f'Medina: {round(valor.median(), 2)}')
        if len(modas_p) == 1:
            print(f'Moda: {modas_p[0]}')
        else:
            print(f'Modas: {", ".join(map(str, modas_p))}')
        print(f'Percentil 30: {round(valor.quantile(0.3), 2)}')
        print(f'Percentil 60: {round(valor.quantile(0.6), 2)}')
        print(f'Percentil 90: {round(valor.quantile(0.9), 2)}')
        print(f'Rango: {round(valor.max() - valor.min(), 2)}')
        print(f'IQR {round(valor.quantile(0.75)- valor.quantile(0.25), 2)}')
        print(f'Covarianza: {round(ss.variation(valor), 2)}')
        print(f'Varianza: {round(valor.var(), 2)}')
        print(f'Desviacion tipica: {round(valor.std(), 2)}')


# HOMBRES
hedad = hombres['edad']
hpeso = hombres['peso']
haltura = hombres['altura']
hcolesterol = hombres['colesterol']    
sexo = 'hombres'
escribir_archivo(sexo, hedad, 'edad', carpeta)
escribir_archivo(sexo,hpeso, 'peso', carpeta)
escribir_archivo(sexo,haltura, 'altura', carpeta)
escribir_archivo(sexo, hcolesterol, 'colesterol', carpeta)

# MUJERES
medad = mujeres['edad']
mpeso = mujeres['peso']
maltura = mujeres['altura']
mcolesterol = mujeres['colesterol']  
sexo = 'mujeres'
escribir_archivo(sexo, medad, 'edad', carpeta)
escribir_archivo(sexo, mpeso, 'peso', carpeta)
escribir_archivo(sexo, maltura, 'altura', carpeta)
escribir_archivo(sexo, mcolesterol, 'colesterol', carpeta)




# APARTADO 4
##################################################################################################################

def calcular_imc (peso, altura):
    imc = round(peso/(altura**2),2)
    return imc

def calcular_riesgo(row):
    imc = row['imc']
    edad = row['edad']
    
    if imc < 25 and edad < 45:
        riesgo = 'bajo'
    elif imc >= 25 and edad < 45:
        riesgo = 'medio'
    elif imc < 25 and edad >= 45:
        riesgo = 'medio'
    elif imc >= 25 and edad >= 45:
        riesgo = 'alto'
    return riesgo

tabla['imc'] = calcular_imc(tabla['peso'], tabla['altura'])
tabla['riesgo'] = tabla.apply(calcular_riesgo, axis=1)          # sin apply no funciona, habria que ahcer un for dentro de la funcion para recorrer la col imc

tabla.to_csv('C:/proyectos/CM/pruebas_practicas/7.ejercicio_final/ejercicio4/apartado4_4.csv', sep=';', decimal=',')



# APARTADO 5
##################################################################################################################

import seaborn as sns

def relacion (df):
    hombres = tabla[tabla['sexo'] == 'H']
    mujeres = tabla[tabla['sexo'] == 'M']

    with open(carpeta + 'apartado4_5.csv', mode="w") as mensaje:
        mensaje.write ('EJERCICIO 4, APARTADO 5\n\n')

        # HOMBRES:
        mensaje.write ('Calculos para los hombres\n')
        cov_h = round(hombres["colesterol"].cov(hombres["imc"]), 2)

        media_imch = round(hombres['imc'].mean(),2)
        media_colesterolh = round(hombres['colesterol'].mean(),2)

        varianza_colesterolh = round(hombres['colesterol'].var(ddof=0),2)

        cofb_h = round(cov_h / varianza_colesterolh,2)
        cofa_h = round(media_imch - cofb_h *media_colesterolh,2)

        mensaje.write(f'Covarianza del colesterol:;{cov_h.astype(str).replace(".", ",")}\n')
        mensaje.write(f'Coeficientes de la recta de IMC sobre colesterol:;{"// ".join(map(lambda x: str(x).replace(".", ","), (cofa_h, cofb_h)))}\n')



        plt.figure(figsize=(8, 6))
        sns.regplot(x = hombres['colesterol'], y = hombres["imc"], 
                    scatter_kws = {"color": "grey", "alpha": 0.5}, 
                    line_kws = {"color": "red"}) 
        plt.title('Relación entre colesterol e IMC en hombres')
        plt.xlabel('Colesterol')
        plt.ylabel('IMC')
        legend_labels = ['Puntos de dispersión', 'Recta de regresión']
        plt.legend(legend_labels)
        plt.savefig('C:/proyectos/CM/pruebas_practicas/7.ejercicio_final/ejercicio4/apartado4_5H.png', bbox_inches='tight')
        plt.show()
        plt.close()
        

        # MUJERES:
        mensaje.write ('\nCalculos para las mujeres\n')
        cov_m = round(mujeres["colesterol"].cov(mujeres["imc"]), 2)
        media_imcm = round(mujeres['imc'].mean(),2)
        media_colesterolm = round(mujeres['colesterol'].mean(),2)
        
        varianza_colesterolm = round(mujeres['colesterol'].var(ddof=0),2)

        cofb_m = round(cov_m / varianza_colesterolm,2)
        cofa_m = round(media_imcm - cofb_m *media_colesterolm,2)

        mensaje.write(f'Covarianza del colesterol y del IMC:;{cov_m.astype(str).replace(".", ",")}\n')
        mensaje.write(f'Coeficientes de la recta de IMC sobre colesterol:;{"// ".join(map(lambda x: str(x).replace(".", ","), (cofa_m, cofb_m)))}\n')


        plt.figure(figsize=(8, 6))
        sns.regplot(x = mujeres['colesterol'], y = mujeres["imc"], 
                    scatter_kws = {"color": "grey", "alpha": 0.5}, 
                    line_kws = {"color": "red"}) 
        plt.title('Relación entre colesterol e IMC en mujeres')
        plt.xlabel('Colesterol')
        plt.ylabel('IMC')
        legend_labels = ['Puntos de dispersión', 'Recta de regresión']
        plt.legend(legend_labels)
        plt.savefig('C:/proyectos/CM/pruebas_practicas/7.ejercicio_final/ejercicio4/apartado4_5M.png', bbox_inches='tight')
        plt.show()
        plt.close()
 


relacion(tabla)
