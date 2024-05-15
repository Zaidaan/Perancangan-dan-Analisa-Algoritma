import pygame
import random
from PIL import Image, ImageDraw

# Inisialisasi Pygame
pygame.init()

# Definisi ukuran layar
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("City Map Generator")

# Ukuran peta dan sel
map_width, map_height = 150, 150
cell_size = 50  # Ukuran sel lebih kecil untuk skala realistis

# Warna latar belakang
background_color = (0, 255, 0)  # Hijau

# Fungsi untuk menggambar grid menggunakan PIL
def draw_grid(image):
    draw = ImageDraw.Draw(image)
    for x in range(0, map_width * cell_size, cell_size):
        draw.line((x, 0, x, map_height * cell_size), fill="black")
    for y in range(0, map_height * cell_size, cell_size):
        draw.line((0, y, map_width * cell_size, y), fill="black")
    return image

# Fungsi untuk menempatkan aset secara acak
def place_assets(num_assets, size):
    assets = []
    for _ in range(num_assets):
        while True:
            row = random.randint(0, map_height - size[1] // cell_size)
            col = random.randint(0, map_width - size[0] // cell_size)
            if all((row + dy, col + dx) not in assets for dy in range(size[1] // cell_size) for dx in range(size[0] // cell_size)):
                for dy in range(size[1] // cell_size):
                    for dx in range(size[0] // cell_size):
                        assets.append((row + dy, col + dx))
                break
    return [(row, col) for row, col in assets if col % (size[0] // cell_size) == 0 and row % (size[1] // cell_size) == 0]

# Fungsi untuk menggambar aset pada peta menggunakan PIL
def draw_assets(image, buildings, roads):
    for road in roads:
        for (row, col) in road:
            image.paste(road_image, (col * cell_size, row * cell_size, col * cell_size + road_size[0], row * cell_size + road_size[1]))
    for (row, col, building_type) in buildings:
        if building_type == 'small':
            image.paste(small_building_image, (col * cell_size, row * cell_size, col * cell_size + small_building_size[0], row * cell_size + small_building_size[1]))
        elif building_type == 'medium':
            image.paste(med_building_image, (col * cell_size, row * cell_size, col * cell_size + med_building_size[0], row * cell_size + med_building_size[1]))
        elif building_type == 'large':
            image.paste(big_building_image, (col * cell_size, row * cell_size, col * cell_size + big_building_size[0], row * cell_size + big_building_size[1]))
        elif building_type == 'house':
            image.paste(house_image, (col * cell_size, row * cell_size, col * cell_size + house_size[0], row * cell_size + house_size[1]))
    return image

# Fungsi untuk menempatkan bangunan dengan jenis yang berbeda secara acak
def place_buildings():
    buildings = []
    buildings += [(row, col, 'large') for (row, col) in place_assets(1, big_building_size)]
    buildings += [(row, col, 'medium') for (row, col) in place_assets(4, med_building_size)]
    buildings += [(row, col, 'small') for (row, col) in place_assets(10, small_building_size)]
    buildings += [(row, col, 'house') for (row, col) in place_assets(10, house_size)]
    return buildings

# Fungsi untuk menempatkan jalan secara bersebelahan agar membentuk jalan yang panjang
def place_roads(num_roads, road_length):
    roads = []
    for _ in range(num_roads):
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            start_row = random.randint(0, map_height - 1)
            start_col = random.randint(0, map_width - road_length)
            road = [(start_row, start_col + i) for i in range(road_length)]
        else:
            start_row = random.randint(0, map_height - road_length)
            start_col = random.randint(0, map_width - 1)
            road = [(start_row + i, start_col) for i in range(road_length)]
        roads.append(road)
    return roads

# Fungsi utama
def main():
    running = True
    clock = pygame.time.Clock()

    # Ukuran bangunan
    global small_building_size, med_building_size, big_building_size, house_size, road_size
    small_building_size = (2 * cell_size, 2 * cell_size)
    med_building_size = (5 * cell_size, 3 * cell_size)
    big_building_size = (10 * cell_size, 5 * cell_size)
    house_size = (cell_size, 2 * cell_size)
    road_size = (4 * cell_size, cell_size)

    # Load aset
    global small_building_image, med_building_image, big_building_image, house_image, road_image
    small_building_image = Image.open("small_building.png").resize(small_building_size)
    med_building_image = Image.open("med_building.png").resize(med_building_size)
    big_building_image = Image.open("big_building.png").resize(big_building_size)
    house_image = Image.open("house.png").resize(house_size)
    road_image = Image.open("road.png").resize(road_size)

    # Buat gambar peta menggunakan PIL
    city_map = Image.new('RGB', (map_width * cell_size, map_height * cell_size), background_color)
    city_map = draw_grid(city_map)
    
    # Tempatkan bangunan dan jalan secara acak
    buildings = place_buildings()
    roads = place_roads(20, 4)  # 20 jalan dengan panjang 4

    city_map = draw_assets(city_map, buildings, roads)

    # Simpan peta sebagai gambar
    city_map.save("generated_city_map.png")

    # Konversi gambar PIL ke format Pygame
    mode = city_map.mode
    size = city_map.size
    data = city_map.tobytes()
    pygame_image = pygame.image.fromstring(data, size, mode)

    # Koordinat untuk menggulir peta
    scroll_x, scroll_y = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    scroll_x = min(scroll_x + 10, 0)
                if event.key == pygame.K_RIGHT:
                    scroll_x = max(scroll_x - 10, screen_width - map_width * cell_size)
                if event.key == pygame.K_UP:
                    scroll_y = min(scroll_y + 10, 0)
                if event.key == pygame.K_DOWN:
                    scroll_y = max(scroll_y - 10, screen_height - map_height * cell_size)

        screen.fill((255, 255, 255))
        screen.blit(pygame_image, (scroll_x, scroll_y))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()