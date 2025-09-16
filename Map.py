import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize #Leyenda de color continua
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import cm



# Leer el archivo CSV
df0 = pd.read_csv('dengue.csv')

# Reemplazar valores NaN con None
df0 = df0.where(pd.notna(df0), None)

# Crear el diccionario con el formato específico
data = {
    'Municipio': df0.iloc[1:, 0].tolist(),  # Primera columna sin el encabezado
    '2023': df0.iloc[1:, 1].tolist(),  # Segunda columna sin el encabezado
    '2024': df0.iloc[1:, 2].tolist()  # Segunda columna sin el encabezado
}

df = pd.DataFrame(data)

# Paso 2: Cargar el archivo shapefile con los datos geoespaciales de los municipios de Guatemala
# Asegúrate de tener un archivo shapefile de los municipios de Guatemala
shapefile = 'Municipios.shp'  # Cambia esta ruta a la de tu archivo shapefile
gdf = gpd.read_file(shapefile)
print(gdf.head())

# Paso 3: Unir los datos de casos con los datos geoespaciales
# Supongamos que en tu shapefile hay una columna 'municipio' con los nombres de los municipios
# Primero, reemplazamos los valores nulos por 0 en los datos de los casos
df['2023'] = df['2023'].fillna(0)
df['2024'] = df['2024'].fillna(0)

print(gdf.columns)

# Unir los datos de casos con la capa geoespacial por la columna de municipio
gdf = gdf.merge(df, left_on='municipio', right_on='Municipio', how='left')

# Paso 4: Crear el mapa y aplicar color según los casos de 2024
# Definimos un rango de colores
norm = Normalize(vmin=0, vmax=3772)  # Puedes ajustar los valores de vmax según tus datos
cmap = cm.get_cmap('YlOrRd')  # Mapa de colores: Amarillo a Rojo de forma continua

#Para forma discreta
bins = [0, 100, 300, 600, 1000, 1500, 2000, 3000, 4800]
colors = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#084594']
colors = ['#ffffcc',  # Amarillo claro
          '#ffeda0',  # Amarillo
          '#fed976',  # Naranja claro
          '#feb24c',  # Naranja medio
          '#fd8d3c',  # Naranja oscuro
          '#fc4e2a',  # Rojo claro
          '#e31a1c',  # Rojo medio
          '#b10026'] 
cmap = ListedColormap(colors)
norm = BoundaryNorm(bins, cmap.N)

# Paso 5: Plotear el mapa
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf.boundary.plot(ax=ax, linewidth=1, color="black")  # Dibujar los límites de los municipios


# Colorear según los casos de 2024
gdf.plot(column='2023', ax=ax, legend=True, cmap=cmap, norm=norm, 
         legend_kwds={'label': "Número de Casos de Dengue 2023",
                      'orientation': "horizontal"})

# Paso 6: Personalizar el mapa
ax.set_title('Mapa de Casos de Dengue en Municipios de Guatemala (2023)', fontsize=15)

plt.savefig('dengue_2023.png', dpi=300, bbox_inches='tight')
# Paso 7: Mostrar el mapa
plt.show()

