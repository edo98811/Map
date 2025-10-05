# Map

Create artistic maps.

## Features

- Select a location
- Generate a stylized map image
- Save or share your map

## Running Instructions

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/Map.git
  cd Map
  ```
2. Create a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Customize parameters in `main.py`:
  
  **Palette options:**  
  Choose from several curated color palettes, each represented as an array of hexadecimal color codes:

  - `["#335c67", "#fff3b0", "#e09f3e", "#9e2a2b", "#540b0e"]`  
    *Earthy greens and warm browns.*

  - `["#003049", "#d62828", "#f77f00", "#fcbf49", "#eae2b7"]`  
    *Deep blues, vibrant reds, and warm yellows.*

  - `["#386641", "#6a994e", "#a7c957", "#f2e8cf", "#bc4749"]`  
    *Forest greens with soft neutrals and a bold accent.*

  - `["#5f0f40", "#9a031e", "#fb8b24", "#e36414", "#0f4c5c"]`  
    *Rich purples, reds, and oranges with a deep blue.*

  - `["#780000", "#c1121f", "#fdf0d5", "#003049", "#669bbc"]`  
    *Strong reds, soft cream, and cool blues.*

  These palettes can be used for theming, data visualization, or UI design to provide visually appealing color combinations.

    - **Location**: Decide on a meaningful place (e.g., your hometown, a favorite city).
    - **Map size**: Adjust `short_side_m` to fit your desired print size or level of detail.
    - **Style**: Select a color palette (`palette_option`) that matches your decor or personal taste.
    - **Reproducibility**: Set a `seed` value to ensure consistent results if you want to recreate the same map later.
    - **Output**: Choose an `output_path` that helps you organize your generated images.

    Example usage:

    ```python
    from map import plot_map

    # I want a map of Paris, sized for a small frame, with the blue-themed palette.
    plot_map(
      lat=48.8566,
      lon=2.3522,
      short_side_m=3000,
      output_path="paris_blue.png",
      palette_option=2,  
      seed=123
    )
    ```



## About

I created this project to design and display artistic maps of the places I've lived, so I could hang them as unique decorations in my home.