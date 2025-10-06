from final_version import plot_map
import os

if __name__ == "__main__":
    cities = [
        # ("mainz-_germany", 50.002682, 8.260495),
        # ("torino-_italy", 45.070339, 7.686864),
        # ("lisbon-_portugal", 38.722252, -9.139337)
        ("bodenheim-_germany", 49.929894, 8.311285),
    ]

    for city, lat, lon in cities:
        output_dir = f"{city}"
        os.makedirs(output_dir, exist_ok=True)
        # for palette_option in range(7, 8):
        for palette_option in ["vibrant_rainbow"]:
          print(city.replace("_", " ").replace("-", ",").title())
          plot_map(
              lat=lat,
              lon=lon,
              palette=["#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f",
                        "#90be6d", "#43aa8b", "#4d908e", "#577590", "#277da1"],
              short_side_m=2000,
              output_path=f"{output_dir}/{city}_palette_{palette_option}.png",
              seed=42,
              palette_option=palette_option,
              place=city.replace("_", " ").replace("-", ",").title()
          )
