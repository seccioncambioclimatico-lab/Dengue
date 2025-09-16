# Install necessary libraries if you haven't already
# !pip install geopandas pandas matplotlib

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the shapefile for Guatemala's municipios
# Make sure to update the path to your shapefile
shapefile_path = "municipios.shp"
guatemala_municipios = gpd.read_file(shapefile_path)

# Load the dengue cases data (ensure this matches the municipio names in the shapefile)
# Example CSV format: municipio, cases
dengue_data_path = "dengue.csv"
dengue_cases = pd.read_csv(dengue_data_path)

# Merge the shapefile with the dengue data based on the municipio name
# Assuming the 'municipio' column exists in both the shapefile and the dengue dataset
guatemala_municipios = guatemala_municipios.merge(dengue_cases, how="left", left_on="NAME_1", right_on="Municipio")

# Plot the map with the dengue cases data
# Choose a color map that visually represents the dengue cases
fig, ax = plt.subplots(1, 1, figsize=(10, 15))

# Plot the municipio geometries and color them based on the number of cases
# You can choose a color map such as 'YlOrRd', 'coolwarm', etc.
guatemala_municipios.plot(column='cases', ax=ax, legend=True,
                          legend_kwds={'label': "Dengue Cases by Municipio",
                                       'orientation': "horizontal"},
                          cmap='YlOrRd', missing_kwds={'color': 'lightgrey'})

# Set plot title
plt.title("Dengue Cases by Municipio in Guatemala", fontsize=16)

# Display the plot
plt.show()

