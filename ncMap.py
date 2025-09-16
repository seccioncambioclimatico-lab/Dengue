import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import zipfile
import os
import numpy as np

# --- Configuración de archivos ---
netcdf_path = "2023mean.nc"  # Ruta del archivo NetCDF
zip_path = "Guatemala.zip"  # Ruta del archivo ZIP con los shapefiles
extract_path = "Guatemala_shapefiles"

# --- Extraer archivos del ZIP ---
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# --- Cargar los shapefiles ---
guatemala_folder = os.path.join(extract_path, "Guatemala")
country_shp = gpd.read_file(os.path.join(guatemala_folder, "country.shp"))
deptos_shp = gpd.read_file(os.path.join(guatemala_folder, "deptos.shp"))
municipios_shp = gpd.read_file(os.path.join(guatemala_folder, "municipios.shp"))

# --- Cargar los datos NetCDF ---
ds = xr.open_dataset(netcdf_path)
t2m_exp5 = ds.t2m.sel(time=ds.time[0])  # Seleccionar expver = 5, latitude=slice(19, 13), longitude=slice(-93.5, -87))  # Recortar área

# --- Crear el gráfico ---
fig, ax = plt.subplots(figsize=(10, 10))

# Definir niveles discretos para la temperatura
temp_levels = np.linspace(float(t2m_exp5.min()), float(t2m_exp5.max()), num=10) #float(t2m_exp5.min()), float(t2m_exp5.max()), #para usar el mínimo y máximo
temp_levels = np.linspace(11, 29, num=10)
# Graficar temperatura como mapa de calor discreto

# Graficar temperatura como mapa de calor
t2m_plot = t2m_exp5.plot(ax=ax, cmap="coolwarm", alpha=0.6, levels=temp_levels)
t2m_plot.colorbar.set_label("Temperatura °C")  # Modificar nombre de la leyenda

# Dibujar los límites administrativos
municipios_shp.boundary.plot(ax=ax, color="white", linewidth=0.5) #linestyle=":", label="Municipios"
deptos_shp.boundary.plot(ax=ax, color="grey", linewidth=1) #linestyle="--"
country_shp.boundary.plot(ax=ax, color="black", linewidth=1.5)



# Configurar el mapa
ax.set_title("Temperatura media diaria para 2023")
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_xlim(-93.5, -87.5)
ax.set_ylim(13, 18.5)
ax.legend()

plt.savefig("mapa_temperatura_gt_2023.png", dpi=300, bbox_inches="tight")
# Mostrar el gráfico
plt.show()
