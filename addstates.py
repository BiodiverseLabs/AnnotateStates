import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Load your dataset
file_path = r'your_file.xlsx'
df = pd.read_excel(file_path)

# Create GeoDataFrame for your points
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry)

# Assign CRS to geo_df (assuming WGS84)
geo_df.set_crs(epsg=4326, inplace=True)

# Load U.S. states shapefile
states = gpd.read_file(r'tl_2024_us_state.shp')

# Reproject geo_df to match states CRS
geo_df = geo_df.to_crs(states.crs)

# Perform spatial join
geo_df = gpd.sjoin(geo_df, states, how="left", predicate="intersects")

# Save the updated dataset
geo_df.drop(columns='geometry').to_excel(r'updated_file_with_states.xlsx', index=False)

