from shapely.geometry import box
import pyproj
from shapely.ops import transform
import math
import geopandas as gpd
from shapely.ops import unary_union, polygonize
import matplotlib.pyplot as plt
import json
import os


def a4_rectangle(center_lat, center_lon, short_side_m, format="A4"):
    """
    Creates a Shapely Polygon representing a rectangle (A4 or square format) centered at the specified latitude and longitude.
    The rectangle is defined in WGS84 coordinates and sized such that its short side is `short_side_m` meters long.
    For A4 format, the long side is calculated using the A4 aspect ratio (1:√2). For square format, both sides are equal.
    Parameters
    ----------
    center_lat : float
      Latitude of the rectangle's center (in degrees, WGS84).
    center_lon : float
      Longitude of the rectangle's center (in degrees, WGS84).
    short_side_m : float
      Length of the rectangle's short side in meters.
    format : str, optional
      Rectangle format: "A4" (default, aspect ratio 1:√2) or "square" (aspect ratio 1:1).
    Returns
    -------
    rect_wgs84 : shapely.geometry.Polygon
      Polygon representing the rectangle in WGS84 coordinates.
    Raises
    ------
    ValueError
      If an unsupported format is specified.
    Notes
    -----
    - Uses local UTM projection for accurate meter-based sizing.
    - Only "A4" and "square" formats are currently supported.
    """

    # A4 ratio: short:long = 1:√2
    if format.lower() == "a4":
        long_side_m = short_side_m * math.sqrt(2)
    elif format.lower() == "square":
        long_side_m = short_side_m
    else:
        raise ValueError("Only A4 and square formats are supported for now")

    # Define local UTM projection for accurate meters
    utm_zone = int((center_lon + 180) // 6) + 1
    utm_crs = pyproj.CRS(
        f"+proj=utm +zone={utm_zone} +datum=WGS84 +units=m +no_defs")
    wgs84_crs = pyproj.CRS("EPSG:4326")

    project_to_utm = pyproj.Transformer.from_crs(
        wgs84_crs, utm_crs, always_xy=True).transform
    project_to_wgs84 = pyproj.Transformer.from_crs(
        utm_crs, wgs84_crs, always_xy=True).transform

    # Convert center to UTM
    center_x, center_y = transform(project_to_utm, box(
        center_lon, center_lat, center_lon, center_lat)).centroid.xy
    cx, cy = center_x[0], center_y[0]

    # Create rectangle in UTM
    minx = cx - short_side_m/2
    maxx = cx + short_side_m/2
    miny = cy - long_side_m/2
    maxy = cy + long_side_m/2
    rect_utm = box(minx, miny, maxx, maxy)

    # Transform back to WGS84
    rect_wgs84 = transform(project_to_wgs84, rect_utm)
    return rect_wgs84


def generate_land_patches(streets_gdf, min_area_m2=50):
    """
    Generate land patches from streets.

    Parameters:
        streets_gdf (GeoDataFrame): GeoDataFrame with street geometries (LineString/MultiLineString)
        min_area_m2 (float): Minimum patch area in m² to keep

    Returns:
        GeoDataFrame: Land patches as polygons in EPSG:4326
    """
    if len(streets_gdf) == 0:
        return gpd.GeoDataFrame(columns=["geometry"], crs="EPSG:4326")

    # Merge all street geometries
    all_streets = unary_union(streets_gdf.geometry)

    # Generate polygons between streets
    land_patches = gpd.GeoDataFrame(geometry=list(polygonize(all_streets)))
    land_patches.crs = streets_gdf.crs

    # Project to meters for accurate area calculation
    land_patches = land_patches.to_crs(epsg=3857)
    land_patches = land_patches[land_patches.geometry.area >
                                min_area_m2].copy()

    # Convert back to WGS84
    land_patches = land_patches.to_crs(epsg=4326)

    return land_patches


def decimal_to_dms(lat, lon):
    """
    Convert latitude and longitude in decimal degrees to degrees, minutes, seconds (DMS) format.

    Args:
        lat (float): Latitude in decimal degrees
        lon (float): Longitude in decimal degrees

    Returns:
        str: Formatted string like 'Latitude: 49°59'34.3" N   Longitude: 8°14'50.1" E'
    """
    def convert(coord, is_lat=True):
        degrees = int(coord)
        minutes_full = abs((coord - degrees) * 60)
        minutes = int(minutes_full)
        seconds = (minutes_full - minutes) * 60
        # Determine N/S/E/W
        if is_lat:
            direction = 'N' if coord >= 0 else 'S'
        else:
            direction = 'E' if coord >= 0 else 'W'
        return f"{abs(degrees)}°{minutes}'{seconds:.1f}\" {direction}"

    lat_dms = convert(lat, is_lat=True)
    lon_dms = convert(lon, is_lat=False)
    return f"{lat_dms}   {lon_dms}"


def add_two_lines_text(
    fig,
    text1,
    text2,
    posx=0.5,
    posy=0.9,
    fontsize1=24,
    weight1='bold',
    color1='#2f2f2f',
    family1='Helvetica',
    fontsize2=20,
    weight2='normal',
    color2='#555555',
    family2='Helvetica',
    gap=0.01
):
    """
    Add two lines of text to a figure with independent styling. 
    The second line is placed just below the first line.

    Args:
        fig (matplotlib.figure.Figure): Figure to add text to.
        text1 (str): First line text.
        text2 (str): Second line text.
        posx (float): X position in figure coordinates (0-1). Default 0.5.
        posy (float): Y position in figure coordinates (0-1). Default 0.1.
        fontsize1, weight1, color1, family1: styling for first line.
        fontsize2, weight2, color2, family2: styling for second line.
        gap (float): Vertical gap between first and second line in figure coords.

    Returns:
        tuple: (text1_artist, text2_artist)
    """
    # First line
    text1_artist = fig.text(
        posx, posy,
        text1,
        ha='center', va='top',
        fontsize=fontsize1,
        weight=weight1,
        color=color1,
        family=family1
    )

    # Get renderer and bbox of first text
    fig.canvas.draw()  # ensure renderer is available
    renderer = fig.canvas.get_renderer()
    bbox1 = text1_artist.get_window_extent(renderer=renderer)
    bbox1_fig = bbox1.transformed(fig.transFigure.inverted())

    # Position second line just below the first
    y2_pos = bbox1_fig.y0 - gap

    text2_artist = fig.text(
        posx, y2_pos,
        text2,
        ha='center', va='top',
        fontsize=fontsize2,
        weight=weight2,
        color=color2,
        family=family2
    )

    return text1_artist, text2_artist


def get_palette(palette_option=1, palette=None):
    """
    Returns a color palette based on the given option or custom palette.

    Args:
      palette_option (int): Option index (1-5) for predefined palettes.
      palette (list or None): Custom palette. If provided, returned as is.

    Returns:
      list: Selected color palette.
    """
    # palettes = {
    #   "warm": ["#335c67", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e"],
    #   "sunset": ["#003049", "#d62828", "#f77f00", "#fcbf49", "#eae2b7"],
    #   "forest": ["#386641", "#6a994e", "#a7c957", "#f2e8cf", "#bc4749"],
    #   "vivid": ["#5f0f40", "#9a031e", "#fb8b24", "#e36414", "#0f4c5c"],
    #   "classic": ["#780000", "#c1121f", "#fdf0d5", "#003049", "#669bbc"],
    #   "fresh": ["#233d4d", "#fe7f2d", "#fcca46", "#a1c181", "#619b8a"],
    #   "neon": ["#390099", "#9e0059", "#ff0054", "#ff5400", "#ffbd00"],
    #   "vibrant_rainbow": ["#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f",
    #         "#90be6d", "#43aa8b", "#4d908e", "#577590", "#277da1"],
    #   "pastel_rainbow": ["#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f",
    #                     "#90be6d", "#43aa8b", "#4d908e", "#577590", "#277da1"]
    # }

    # Load palettes from palette.json
    palette_file = os.path.join(os.path.dirname(__file__), "palettes.json")
    with open(palette_file, "r") as f:
        palettes = json.load(f)

    if palette is None:
        # Accept palette_option as either int (legacy) or str (key)
        if isinstance(palette_option, int):
            # If palette_option is an integer, map to palette by index (1-based)
            keys = list(palettes.keys())
            if 1 <= palette_option <= len(keys):
                return palettes[keys[palette_option - 1]]
            else:
                # Warn and use default if out of range
                import warnings
                warnings.warn(
                    "Invalid palette_option, resorting to default palette.", UserWarning)
                return palettes["warm"]
        elif isinstance(palette_option, str):
            # If palette_option is a string, use as key
            if palette_option in palettes:
                return palettes[palette_option]
            else:
                # Warn and use default if key not found
                import warnings
                warnings.warn(
                    "Invalid palette_option key, resorting to default palette.", UserWarning)
                return palettes["warm"]
        else:
            # Warn and use default for invalid type
            import warnings
            warnings.warn(
                "Invalid palette_option type, resorting to default palette.", UserWarning)
            return palettes["warm"]
    # If custom palette is provided, return it as is
    return palette
