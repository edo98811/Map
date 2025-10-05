import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from shapely.ops import unary_union, polygonize
from shapely.geometry import box
from helper_functions import a4_rectangle, generate_land_patches, decimal_to_dms, add_two_lines_text, get_palette
from matplotlib import patheffects
from matplotlib.text import Text


def plot_map(
    lat,
    lon,
    short_side_m=5000,
    output_path="mainz_final.png",
    seed=42,
    palette_option=1
):
    """
    Plots a stylized map of a specified location and saves it as an image.
    Parameters
    ----------
    lat : float
      Latitude of the map center.
    lon : float
      Longitude of the map center.
    short_side_m : int, optional
      Length of the short side of the map rectangle in meters (default is 5000).
    output_path : str, optional
      Path to save the output image file (default is "mainz_final.png").
    palette : list or None, optional
      List of colors to use for buildings and land patches. If None, a palette is selected based on `palette_option`.
    seed : int, optional
      Random seed for color assignment (default is 42).
    palette_option : int, optional
      Option to select a predefined color palette (default is 1).
    Returns
    -------
    None
      The function saves the generated map as an image file at `output_path`.
    Notes
    -----
    - The map includes buildings, streets, railways, and water features within an A4-sized rectangle centered at the specified coordinates.
    - Uses OpenStreetMap data via OSMnx and GeoPandas for spatial operations.
    - The appearance of buildings and land patches is randomized using the provided palette and seed.
    - The function customizes the map's style and adds a location label.
    """

    palette = get_palette(palette_option)

    rectangle = a4_rectangle(lat, lon, short_side_m=short_side_m, format="A4")

    polygons = gpd.GeoDataFrame(geometry=[rectangle], crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(8.27, 11.69), facecolor="#f6f5f3")
    ax.set_facecolor("#f6f5f3")

    tags = {
        "building": True,
        "highway": True,
        "railway": True,
        "natural": True
    }
    gdf = ox.features.features_from_polygon(
        polygons.geometry.iloc[0], tags=tags)

    buildings = gdf[gdf["building"].notna()].copy()
    streets = gdf[gdf["highway"].notna()].copy()
    rail = gdf[gdf["railway"].notna()].copy()
    water = gdf[gdf["natural"].isin(["water", "river", "lake"])].copy()

    buildings = gpd.clip(buildings, polygons)
    streets = gpd.clip(streets, polygons)
    rail = gpd.clip(rail, polygons)
    water = gpd.clip(water, polygons)

    land_patches = generate_land_patches(streets)

    np.random.seed(seed)
    if len(buildings):
        buildings["color"] = np.random.choice(palette, len(buildings))
    if len(land_patches):
        land_patches["color"] = [mcolors.to_rgba(
            c, alpha=0.4) for c in np.random.choice(palette, len(land_patches))]

    if len(land_patches):
        land_patches.plot(ax=ax, color=land_patches["color"], linewidth=0)

    if len(rail):
        rail = rail[rail.geometry.notna() & ~rail.geometry.is_empty].copy()
        rail = rail[rail.geometry.geom_type.isin(
            ["LineString", "MultiLineString"])]
        if not rail.empty:
            rail.plot(ax=ax, color="#9b7b5b", linewidth=1, alpha=0.8)

    if len(streets):
        streets = streets[streets.geometry.geom_type.isin(
            ["LineString", "MultiLineString"])]
        main_roads = streets[streets["highway"].isin(
            ["primary", "trunk", "motorway"])]
        secondary_roads = streets[~streets["highway"].isin(
            ["primary", "trunk", "motorway"])]
        if len(secondary_roads):
            secondary_roads.plot(ax=ax, color="#3a3a3a",
                                 linewidth=0.5, alpha=1)
        if len(main_roads):
            main_roads.plot(ax=ax, color="#3a3a3a", linewidth=1.1, alpha=0.9)

    if len(buildings):
        buildings.plot(
            ax=ax, color=buildings["color"], edgecolor="none", linewidth=0, alpha=0.8)

    if len(water):
        water.plot(ax=ax, color="#a3c4f3", alpha=0.95, linewidth=0)

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    add_two_lines_text(fig, "Mainz, Germany", decimal_to_dms(
        lat, lon), posx=0.5, posy=0.13)

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches='tight',
        pad_inches=0,
        facecolor=fig.get_facecolor(),
        format="png",
        transparent=False
    )
