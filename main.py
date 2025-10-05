from final_version import plot_map
import os

if __name__ == "__main__":
    cities = [
      ("mainz", 50.002682, 8.260495),
      ("torino", 45.070339, 7.686864),
      ("lisbon", 38.722252, -9.139337)
    ]

    for city, lat, lon in cities:
      output_dir = f"{city}"
      os.makedirs(output_dir, exist_ok=True)
      for palette_option in range(1, 6):
        plot_map(
          lat=lat,
          lon=lon,
          short_side_m=5000,
          output_path=f"{output_dir}/{city}_palette{palette_option}.png",
          palette=palette_option,
          seed=42,
          palette_option=palette_option
        )
