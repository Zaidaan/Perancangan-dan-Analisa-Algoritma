import tkinter as tk
from PIL import Image, ImageTk
import random

# Load asset images
def load_assets():
    assets = {
        'big_building': Image.open('asset/big_building.png'),
        'medium_building': Image.open('asset/medium_building.png'),
        'small_building': Image.open('asset/small_building.png'),
        'road_straight': Image.open('asset/road_straight.png'),
        'road_turn': Image.open('asset/road_turn.png'),
    }
    return assets

# Generate city layout
def generate_city(assets, size=150):
    layout = [['' for _ in range(size)] for _ in range(size)]
    # Add logic to place buildings, roads, and parks
    for i in range(size):
        for j in range(size):
            # For simplicity, randomly choose between building, road, or park
            choice = random.choice(['big_building', 'medium_building', 'small_building', 'road_straight', 'road_turn'])
            layout[i][j] = choice
    return layout

# Render city layout on canvas
def render_city(canvas, layout, assets, cell_size=20):
    canvas.delete("all")
    size = len(layout)
    for i in range(size):
        for j in range(size):
            asset = assets[layout[i][j]]
            img = ImageTk.PhotoImage(asset.resize((cell_size, cell_size)))
            canvas.create_image(j*cell_size, i*cell_size, anchor=tk.NW, image=img)
            canvas.image = img

# Refresh button callback
def refresh_city():
    global layout
    layout = generate_city(assets)
    render_city(canvas, layout, assets)

# Main application
root = tk.Tk()
root.title("City Design Generator")

assets = load_assets()
layout = generate_city(assets)

canvas = tk.Canvas(root, width=3000, height=3000)
canvas.pack()

refresh_button = tk.Button(root, text="Refresh City", command=refresh_city)
refresh_button.pack()

render_city(canvas, layout, assets)

root.mainloop()
