# 1. Limpieza y Transformación de Datos 

import pandas as pd
import numpy as np
from pathlib import Path

# 1.1 Carga el dataset en un DataFrame de Pandas.
path = Path(__file__).parent / ('migracion.csv')
df = pd.read_csv(path)
print(f' \n 1.1 DataFrame original:\n {df} \n')

# 1.2 Identifica y trata valores perdidos en el dataset. 
print(f'1.2 Valores perdidos:\n{df.isnull().sum()}\n')
print('No existen valores perdidos en el DataFrame.\n')
# Para este ejemplo no hay valores perdidos, pero de existir, usar .fillna() o .dropna()

# 1.3 Detecta y filtra outliers usando el método del rango intercuartílico (IQR).
Q1 = df['Cantidad_Migrantes'].quantile(0.25)
Q3 = df['Cantidad_Migrantes'].quantile(0.75)
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

df_sin_outliers = df[(df['Cantidad_Migrantes'] >= limite_inferior) & (df['Cantidad_Migrantes'] <= limite_superior)]
df_outliers = df[(df['Cantidad_Migrantes'] <= limite_inferior) & (df['Cantidad_Migrantes'] >= limite_superior)]

print('1.3 Identficación de Outliers')
print(f'Límite Inferior: {limite_inferior}')
print(f'Límite Superior: {limite_superior}\n')
print(f'IQR: {IQR} \n')
print(f'df_outliers: \n {df_sin_outliers}\n')
print('DataFrame no contiene Outliers\n')
print(f'df_outliers: \n {df_outliers}\n')

# 1.4 Reemplaza los valores de la columna "Razon_Migracion" usando mapeo de valores (ejemplo: "Económica" → "Trabajo", "Conflicto" → "Guerra"). 

mapa_razon = {'Económica': 'Trabajo', 'Conflicto': 'Guerra', 'Educativa': 'Estudios'}
df['Razon_Migracion'] = df['Razon_Migracion'].replace(mapa_razon)
print(f'1.4 Valores reemplazados en columna Razón_Migración: \n {df} \n')


# 2. Análisis Exploratorio 
# 2.1 Muestra las 5 primeras filas del dataset. 
print(f'2.1 Cabecera: \n {df.head(5)}\n')

# 2.2 Obtén información general del dataset con .info() y .describe(). 
print(f'2.2.1 Info: \n {df.info()} \n')
print(f'2.2.2 Describe: \n {df.describe()}  \n')

print('Estadísticas descriptivas')
estadisticas = df.describe().round(2) # redondea a 2 decimales

# Renonmbrar las filas al español
estadisticas.rename(index={
    'count': 'conteo',
    'mean': 'media',
    'std': 'desviación estándar',
    'min': 'mínimo',
    '25%': 'percentil 25',
    '50%': 'mediana (percentil 50)',
    '75%': 'percentil 75',
    'max': 'máximo'
}, inplace=True)
 
print(estadisticas)

# 2.3Calcula estadísticas clave: 
    # Media y mediana de la cantidad de migrantes. 
print(f'\n2.3.1 Media migrantes: {df['Cantidad_Migrantes'].mean()}')
print(f'2.3.2 Mediana migrantes: {df['Cantidad_Migrantes'].median()}')

    # 2.3.3 PIB promedio de los países de origen y destino: Usa .value_counts() para contar cuántos movimientos de migración ocurrieron por cada razón. 
print(f'2.3.3 Media PIB origen: {df['PIB_Origen'].mean()}')
print(f'2.3.4 Media PIB destino: {df['PIB_Destino'].mean()}')
print(f'2.3.5 Movimientos de migración por razón:\n{df['Razon_Migracion'].value_counts()} \n')    


 #3. Agrupamiento y Sumarización de Datos
# 3.1 Agrupa los datos por "Razon_Migracion" y calcula la suma total de migrantes para cada categoría. 
print(f'3.1 Suma total migrantes: \n {df.groupby('Razon_Migracion')['Cantidad_Migrantes'].sum()}\n') 


# 3.2 Obtén la media del IDH de los países de origen por cada tipo de migración. 
print(f'3.2 Media IDH por razón migración: \n {df.groupby('Razon_Migracion')['IDH_Origen'].mean()}\n')

# 3.3 Ordena el DataFrame de mayor a menor cantidad de migrantes. 

df_valores_ordenados = df.sort_values('Cantidad_Migrantes', ascending=False)
print(f'3.3 DataFRame ordenado por cantidad de migrantes:\n{df_valores_ordenados}\n')

# 4. Filtros y Selección de Datos
# 4.1 Filtra y muestra solo las migraciones por conflicto. 

df_migraciones_conflicto = df[df['Razon_Migracion'] == 'Guerra']
print(f'4.1 Migraciones por conficto: \n{df_migraciones_conflicto}\n')

# 4.2 Selecciona y muestra las filas donde el IDH del país de destino sea mayor a 0.90. 

idh_alto = df[df["IDH_Destino"] > 0.90]
print(f'4.2 IDH destino mayor a 0.90:\n{idh_alto}\n')

# 4.3 Crea una nueva columna "Diferencia_IDH" que calcule la diferencia de IDH entre país de origen y destino. 

df["Diferencia_IDH"] = (df["IDH_Destino"] - df["IDH_Origen"])
print(f'\n4.3 DF con nueva columna Diferencia IDH:\n{df}\n')

#5. Exportación de Datos
# 5.1 Guarda el DataFrame final en un nuevo archivo CSV llamado "Migracion_Limpio.csv", sin el índice. 

df.to_csv('Migración_limpio.csv', index=False)
