#FUNCIONES EJERCICIO72
import matplotlib.pyplot as plt
import seaborn as sns

colores_pastel= []
# APARTADO 2
###########################################################################################################
# Crear una función que reciba un país y una fecha y devuelva un diccionario con la deuda total interna, externa, 
#   en moneda local, en moneda extranjera, a corto plazo y a largo plazo, de ese país en esa fecha.

def ejercicio72_2(df, pais, fecha):
    tipos_deuda = ['Deuda interna', 'Deuda externa', 'Deuda en moneda local', 
                   'Deuda en moneda extranjera', 'Deuda a corto plazo', 
                   'Deuda a largo plazo']
    df_filtrado = df[(df['Pais'] == pais) & (df['Fecha'] == fecha) & (df['TipoId'].isin(tipos_deuda))]
    
    resultado = df_filtrado[['Pais', 'Fecha', 'TipoId', 'Cantidad']]
    return resultado.to_csv('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_2.csv')

# hay que poner isin porque si pones &  no cumple todos los requisitos y si pones | te saca los que cumplen 1 de las condiciones
# pero no que sea del pais y el año que tu pides




# APARTADO 3
###########################################################################################################
# Crear una función que reciba un tipo de deuda y una fecha, y devuelva un diccionario con la deuda de ese tipo de todos los países
#    en esa fecha.

def ejercicio72_3(df, deuda, fecha):
    
    df_filtrado = df[(df['TipoId'] == deuda) & (df['Fecha'] == fecha)]
    resultado = df_filtrado[['Pais', 'Fecha', 'TipoId', 'Cantidad']]
    
    return resultado.to_csv('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_3.csv')




# APARTADO 4
###########################################################################################################
# Crear una función que reciba un país y una fecha y dibuje un diagrama de sectores con la deuda interna y la deuda externa de ese
#   país en esa fecha.

paleta = sns.color_palette("hls", 8)

def ejercicio72_4(df, pais, fecha):

    tipos_deuda = ['Deuda interna', 'Deuda externa']
    df_filtrado = df[(df['Pais'] == pais) & (df['Fecha'] == fecha) & (df['TipoId'].isin(tipos_deuda))]
    
    # Calcular los porcentajes de cada tipo de deuda
    porcentajes = df_filtrado['Cantidad'] / df_filtrado['Cantidad'].sum() * 100
    
    # Crear el gráfico de tipo pie
    plt.figure(figsize=(8, 8))
    plt.title(f'Cantidad de deuda interna y externa en {pais} en {fecha}', loc='center', fontdict={'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    
    #añadiendo patches y texts, luego se puede poner reborde a cada trozo
    patches, texts, _ = plt.pie(porcentajes, labels=df_filtrado['TipoId'], autopct='%1.1f%%', colors=paleta)
    
    # Agregar borde a cada trozo del pastel
    for patch in patches:
        patch.set_edgecolor('#222222')
    
    plt.axis('equal')   # garantiza que el círculo generado sea realmente un círculo perfecto y no una elipse.
    plt.savefig('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_4.png', bbox_inches='tight')
    plt.show()





# APARTADO 5
###########################################################################################################
# Crear una función que reciba un país y una fecha, y dibuje un diagrama de barras con las cantidades de los distintos tipos
#    de deudas de ese país en esa fecha.


def ejercicio72_5(df, pais, fecha):
    df_filtrado = df[(df['Pais'] == pais) & (df['Fecha'] == fecha)]
    df_filtrado = df_filtrado.groupby('TipoId')['Cantidad'].sum()
    
        
    df_filtrado.plot(kind='bar', color=paleta, edgecolor='black')
    plt.xlabel('Tipo de deuda', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.ylabel('Cantidad', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.title(f'Cantidad de deuda en {pais} en {fecha}', loc='center', fontdict={'fontsize':14, 'fontweight':'bold', 'color':'tab:blue'})
    
    # Rotar los nombres de los distritos para que se lea mejor
    plt.xticks(rotation=90)
    plt.grid(axis='y', color='darkgray', linestyle='dashed')
    # Ajustar el diseño
    plt.tight_layout()
    plt.savefig('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_5.png', bbox_inches='tight')
    plt.show()










# APARTADO 6
###########################################################################################################
# Crear una función que reciba una lista de 4 países y un tipo de deuda y dibuje un diagrama de líneas con la evolución 
#   de ese tipo de deuda de esos países (una línea por país).
    

def ejercicio72_6(df, deuda, lista):
    # Filtrar el dfFrame por el tipo de deuda especificado
    df_filtrado = df[(df['TipoId'] == deuda) & (df['Pais'].isin(lista))]
    
    # Agrupar por país y calcular la suma de la cantidad de deuda para cada país
    df_agrupado = df_filtrado.groupby('Pais')['Cantidad'].sum()
    

    # Crear un gráfico de líneas con la evolución de la deuda para cada país
    plt.figure(figsize=(10, 6))
    for i, pais in enumerate(df_agrupado.index):
        plt.plot(df_filtrado[df_filtrado['Pais'] == pais]['Fecha'], 
                 df_filtrado[df_filtrado['Pais'] == pais]['Cantidad'], 
                 label=pais,linestyle = 'dashed', marker = '.')

    plt.title(f'Evolución de la deuda tipo {deuda} por país', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.xlabel('Fecha', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.ylabel('Cantidad de deuda', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    return plt.savefig('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_6.png', bbox_inches='tight')






# APARTADO 7
###########################################################################################################
# Crear una función que reciba un país y una lista de 3 tipos de deuda y dibuje un diagrama de líneas con la evolución
#    de esos tipos de deuda de ese país (una línea por tipo de deuda).


def ejercicio72_7(df, pais, lista):
    # Filtrar el dfFrame por el tipo de deuda especificado
    df_filtrado = df[(df['Pais'] == pais) & (df['TipoId'].isin(lista))]

    # Agrupar por país y calcular la suma de la cantidad de deuda para cada tipo deuda
    numero = df_filtrado.groupby('TipoId')['Cantidad'].count()
    df_agrupado = (df_filtrado.groupby('TipoId')['Cantidad'].sum())/numero      #se puede hacer media del año para q no salgan tantos valores
    
    # Crear un gráfico de líneas con la evolución de la deuda para cada país
    plt.figure(figsize=(10, 6))
    for deuda in (df_agrupado.index):
        plt.plot(df_filtrado[df_filtrado['TipoId'] == deuda]['Fecha'], 
                 df_filtrado[df_filtrado['TipoId'] == deuda]['Cantidad'], 
                 label=deuda, marker = '*')
        
    plt.title(f'Evolución de la deuda en {pais}', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.xlabel('Fecha', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.ylabel('Cantidad de deuda', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.tight_layout()
    return plt.savefig('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_7.png', bbox_inches='tight')






# APARTADO 8
###########################################################################################################
# Crear una función que reciba una lista de 4 países y una lista de 3 tipos de deuda, y dibuje un diagrama de cajas con las deudas
#    de esos tipos de esos países (una caja por país y tipo de deuda).


def ejercicio72_8(df, paises, deudas):
    df_filtrado = df[(df['Pais'].isin(paises)) & (df['TipoId'].isin(deudas))]
    
    # defino mi paleta de colores (buscada en https://seaborn.pydata.org/tutorial/color_palettes.html#diverging-color-palettes)
    mipaleta= sns.color_palette("Paired")


    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df_filtrado, x='Pais', y='Cantidad', hue='TipoId', palette=mipaleta)   # le aplico mi paleta
    plt.title(f'Diagrama de cajas de deudas según los países y sus deudas', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.xlabel('País', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.ylabel('Cantidad de Deuda', loc='center', fontdict={'fontsize':12, 'fontweight':'bold', 'color':'tab:blue'})
    plt.xticks(rotation=45)
    plt.legend(title='Tipo de Deuda')
    plt.tight_layout()
    plt.savefig('C:/proyectos/CM/pruebas_practicas/5.matplotlib/ejercicio72/ejercicio72_8.png', bbox_inches='tight')
    plt.show()
    


