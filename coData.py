import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 📌 1. Cargar los datos desde texto
data = """Year,Emissions
1870,0
1871,0
1872,0
1873,0
1874,3
1875,0
1876,0
1877,5
1878,23
1879,38
1880,23
1881,5
1882,3
1883,28
1884,74
1885,49
1886,103
1887,97
1888,126
1889,203
1890,362
1891,321
1892,587
1893,1131
1894,1857
1895,12208
1896,10023
1897,13732
1898,3260
1899,2834
1900,4732
1901,7420
1902,13096
1903,17366
1904,24563
1905,34397
1906,39139
1907,35479
1908,28277
1909,29554
1910,35607
1911,40860
1912,44756
1913,44004
1914,41024
1915,47018
1916,28698
1917,2526
1918,708
1919,10418
1920,5196
1921,7292
1922,2077
1923,857
1924,1762
1925,0
1926,0
1927,382
1928,1149
1929,2298
1930,1149
1931,1149
1932,1149
1933,1531
1934,1913
1935,382
1936,1531
1937,1913
1938,767
1939,1531
1940,767
1941,12052
1942,11285
1943,11670
1944,11670
1945,15304
1946,15304
1947,15304
1948,15686
1949,20085
1950,622100
1951,637298
1952,644626
1953,681266
1954,743554
1955,915673
1956,977961
1957,985230
1958,1128037
1959,1237957
1960,1344242
1961,1406471
1962,1380853
1963,1519936
1964,1768969
1965,1973945
1966,1739598
1967,1981333
1968,2139063
1969,2278117
1970,2296437
1971,2439303
1972,2706626
1973,2933616
1974,3065520
1975,3519529
1976,3304906
1977,3804453
1978,4117133.2
1979,4678019
1980,4492606
1981,3949467
1982,3606792
1983,3159905
1984,3401061
1985,3496849
1986,3664595
1987,3918400
1988,4075276.8
1989,4188155.2
1990,4972245
1991,4951134
1992,5919209
1993,5577778
1994,6751174
1995,7078550
1996,6571124
1997,7501859
1998,8639397
1999,8805825
2000,9764762
2001,10233260
2002,10721662
2003,10447951
2004,11180307
2005,12109271
2006,12176554
2007,12144909
2008,10893166
2009,11442047
2010,11097682
2011,11237312
2012,11576644
2013,12811682
2014,13827098
2015,15951887
2016,16926494
2017,17320534
2018,18522746
2019,19303848
2020,17164690
2021,19805034
2022,19113738
2023,20382320"""

# Convertir los datos en un DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data))

# Ver las primeras filas
print(df.head())


# Filtrar los datos para que solo incluyan años a partir de 1950
df_filtered = df[df['Year'] >= 1945]

#Línea de regresión a los datos
x = df_filtered['Year']
y = df_filtered['Emissions']
coeffs = np.polyfit(x, y, 3)  # Ajuste de primer grado (lineal)
poly = np.poly1d(coeffs)

# Realizar predicción para los próximos 10 años (2024-2033)
future_years = np.arange(2024, 2034)  # Años para los cuales predecir emisiones
predicted_emissions = poly(future_years)  # Predicción de emisiones para esos años

# Calcular promedio móvil (5 años) para suavizar la tendencia
df['Moving_Avg'] = df['Emissions'].rolling(window=5).mean()

# Visualización de tendencias de emisiones
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Emissions', data=df, marker='o', color='b', label='CO₂ Emissions')

# Añadir el promedio movil
sns.lineplot(x='Year', y='Moving_Avg', data=df, color='orange', linestyle='--', label='5-Year Moving Average')


# Mostrar los años futuros
plt.plot(x, poly(x), color='purple', label='Regresión Lineal', linestyle='-')
plt.plot(future_years, predicted_emissions, color='pink', marker='o', linestyle='--', label='Predicción de Emisiones (2024-2033)')


#Eventos relevantes
plt.axvline(x=2016, color='g', linestyle='dotted', label='Acuerdo de París') #Acuerdo de París
plt.axvline(x=2020, color='r', linestyle='dotted', label='Inicio Pandemia') #Inicio de Pandemia




# Configuración del gráfico
plt.title('Tendencia de Emisiones de CO₂ en Guatemala (1870-2023)')
plt.xlabel('Año')
plt.ylabel('Emisiones de CO₂ (Toneladas)')
plt.legend()
plt.grid(True)





# Mostrar la gráfica
plt.show()

predictions = pd.DataFrame({
    'Year': future_years,
    'Predicted Emissions': predicted_emissions
})
print(predictions)