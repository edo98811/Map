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
  Choose these color palettes:

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

You can customise these parameters:

  - **Location**: Decide on a meaningful place (e.g., your hometown, a favorite city).
  - **Map size**: Adjust `short_side_m` to fit your desired print size or level of detail.
  - **Style**: Select a color palette (`palette_option`) that matches your decor or personal taste.
  - **Reproducibility**: Set a `seed` value to ensure consistent results if you want to recreate the same map later.
  - **Output**: Choose an `output_path` that helps you organize your generated images.

    Example usage:

    ```python
    from map import plot_map

    # I want a map of Turin with a nice pastel palette.
    plot_map(
        lat= 45.070339,
        lon= 7.686864,
        palette=["#f94144", "#f3722c", "#f8961e", "#f9844a", "#f9c74f",
                  "#90be6d", "#43aa8b", "#4d908e", "#577590", "#277da1"],
        short_side_m=5000,
        output_path=f"torino.png",
        seed=42,
        place="Turin, Italy"
    )

    ```

![example_output](docs/example.png)

## About

I created this project to design artistic maps of the places I've lived in, so I could hang them as decorations in my home.
