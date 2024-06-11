import random
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

MAP_SIZE = 150
CELL_SIZE = 32

EMPTY = 0
CROSSROAD = 'crossroad'
T_JUNCTION = 't_junction'
TURN = 'turn'
ROAD = 'road'
TREE = 'tree'
BIG_BUILDING = 'big_building'
MEDIUM_BUILDING = 'medium_building'
SMALL_BUILDING = 'small_building'
HOUSE = 'house'

CROSSROAD_LIMIT = 8
T_JUNCTION_LIMIT = 10
TURN_LIMIT = 20
MIN_DISTANCE = 5

BUILDING_SIZES = {
    BIG_BUILDING: [7, 3],
    MEDIUM_BUILDING: [5, 3],
    SMALL_BUILDING: [2, 2],
    HOUSE: [1, 1],
    TREE: [1, 1]
}

BUILDING_MINIMUMS = {
    BIG_BUILDING: 1,
    MEDIUM_BUILDING: 4,
    SMALL_BUILDING: 10,
    HOUSE: 10,
    TREE: 50
}

def is_location_valid(x, y, width=1, height=1):
    for i in range(max(0, x - MIN_DISTANCE), min(MAP_SIZE, x + width + MIN_DISTANCE)):
        for j in range(max(0, y - MIN_DISTANCE), min(MAP_SIZE, y + height + MIN_DISTANCE)):
            if map[i][j] != EMPTY:
                return False
    return True

def extend_road(x, y, direction):
    if direction == 'up':
        for i in range(x - 1, -1, -1):
            if map[i][y] != EMPTY:
                break
            map[i][y] = 'vertical_road'
    elif direction == 'down':
        for i in range(x + 1, MAP_SIZE):
            if map[i][y] != EMPTY:
                break
            map[i][y] = 'vertical_road'
    elif direction == 'left':
        for j in range(y - 1, -1, -1):
            if map[x][j] != EMPTY:
                break
            map[x][j] = 'horizontal_road'
    elif direction == 'right':
        for j in range(y + 1, MAP_SIZE):
            if map[x][j] != EMPTY:
                break
            map[x][j] = 'horizontal_road'

def place_buildings():
    for building in BUILDING_MINIMUMS:
        if building == TREE:
            continue
        count = 0
        while count < BUILDING_MINIMUMS[building]:
            x = random.randint(0, MAP_SIZE - BUILDING_SIZES[building][0])
            y = random.randint(0, MAP_SIZE - BUILDING_SIZES[building][1])
            if is_location_valid_for_building(x, y, BUILDING_SIZES[building][0], BUILDING_SIZES[building][1]):
                for i in range(x, x + BUILDING_SIZES[building][0]):
                    for j in range(y, y + BUILDING_SIZES[building][1]):
                        map[i][j] = building
                count += 1

def place_trees():
    count = 0
    while count < BUILDING_MINIMUMS[TREE]:
        x = random.randint(0, MAP_SIZE - 1)
        y = random.randint(0, MAP_SIZE - 1)
        if map[x][y] == EMPTY:
            map[x][y] = TREE
            count += 1

def is_location_valid_for_building(x, y, width, height):
    for i in range(x, x + width):
        for j in range(y, y + height):
            if i >= 0 and i < MAP_SIZE and j >= 0 and j < MAP_SIZE:
                if map[i][j] != EMPTY:
                    return False
    road_found = False
    for i in range(max(0, x - 1), min(MAP_SIZE, x + width + 1)):
        for j in range(max(0, y - 1), min(MAP_SIZE, y + height + 1)):
            if map[i][j] in ['vertical_road', 'horizontal_road', CROSSROAD, 'tjunction_up', 'tjunction_down', 'tjunction_left', 'tjunction_right', 'turn_right_up', 'turn_left_up', 'turn_right_down', 'turn_left_down']:
                road_found = True
            if i in range(x, x + width) and j in range(y, y + height):
                continue
            if map[i][j] in BUILDING_SIZES:
                return False
    return road_found

def generate_map():
    global map
    map = [[EMPTY for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    crossroad_count = 0
    t_junction_count = 0
    turn_count = 0

    while crossroad_count < CROSSROAD_LIMIT or t_junction_count < T_JUNCTION_LIMIT or turn_count < TURN_LIMIT:
        x = random.randint(1, MAP_SIZE - 2)
        y = random.randint(1, MAP_SIZE - 2)
        if map[x][y] == EMPTY and is_location_valid(x, y):
            if crossroad_count < CROSSROAD_LIMIT:
                map[x][y] = CROSSROAD
                extend_road(x, y, 'up')
                extend_road(x, y, 'down')
                extend_road(x, y, 'left')
                extend_road(x, y, 'right')
                crossroad_count += 1
            elif t_junction_count < T_JUNCTION_LIMIT:
                direction = random.choice(['up', 'down', 'left', 'right'])
                if direction == 'up':
                    map[x][y] = 'tjunction_up'
                    extend_road(x, y, 'up')
                    extend_road(x, y, 'left')
                    extend_road(x, y, 'right')
                elif direction == 'down':
                    map[x][y] = 'tjunction_down'
                    extend_road(x, y, 'down')
                    extend_road(x, y, 'left')
                    extend_road(x, y, 'right')
                elif direction == 'left':
                    map[x][y] = 'tjunction_left'
                    extend_road(x, y, 'left')
                    extend_road(x, y, 'up')
                    extend_road(x, y, 'down')
                elif direction == 'right':
                    map[x][y] = 'tjunction_right'
                    extend_road(x, y, 'right')
                    extend_road(x, y, 'up')
                    extend_road(x, y, 'down')
                t_junction_count += 1
            elif turn_count < TURN_LIMIT:
                direction = random.choice(['up-right', 'up-left', 'down-right', 'down-left'])
                if direction == 'up-right':
                    map[x][y] = 'turn_right_up'
                    extend_road(x, y, 'up')
                    extend_road(x, y, 'right')
                elif direction == 'up-left':
                    map[x][y] = 'turn_left_up'
                    extend_road(x, y, 'up')
                    extend_road(x, y, 'left')
                elif direction == 'down-right':
                    map[x][y] = 'turn_right_down'
                    extend_road(x, y, 'down')
                    extend_road(x, y, 'right')
                elif direction == 'down-left':
                    map[x][y] = 'turn_left_down'
                    extend_road(x, y, 'down')
                    extend_road(x, y, 'left')
                turn_count += 1

def draw_map():
    canvas = Image.new('RGB', (MAP_SIZE * CELL_SIZE, MAP_SIZE * CELL_SIZE), color='white')
    draw = ImageDraw.Draw(canvas)

    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            cell = map[i][j]
            if cell in asset:
                image = asset[cell]
                canvas.paste(image, (j * CELL_SIZE, i * CELL_SIZE))

    # Display image using matplotlib
    plt.figure(num="IKN CITY")
    plt.imshow(canvas)
    plt.axis('off')
    plt.show()

current_x = 0
current_y = 0
zoom_level = 1.0
zoom_step = 0.1
def on_scroll(event):
    global zoom_level
    if event.button == 'up':
        zoom_level -= zoom_step
    elif event.button == 'down':
        zoom_level += zoom_step

    ax = plt.gca()
    ax.set_xlim(current_x, current_x + MAP_SIZE * zoom_level)
    ax.set_ylim(current_y, current_y + MAP_SIZE * zoom_level)
    plt.draw()

def on_key(event):
    global current_x, current_y
    step = 10  # Jumlah pixel untuk digerakkan
    if event.key == 'up':
        current_y += step
    elif event.key == 'down':
        current_y -= step
    elif event.key == 'left':
        current_x -= step
    elif event.key == 'right':
        current_x += step

    ax = plt.gca()
    ax.set_xlim(current_x, current_x + MAP_SIZE)
    ax.set_ylim(current_y, current_y + MAP_SIZE)
    plt.draw()

def regenerate_map(event):
    redesign_map()

regen_button = plt.Button(plt.gca(), 'Regenerate Map')
regen_button.on_clicked(regenerate_map)

fig = plt.figure(num="IKN CITY")
fig.canvas.mpl_connect('scroll_event', on_scroll)
fig.canvas.mpl_connect('key_press_event', on_key)

def redesign_map():
    generate_map()
    place_buildings()
    place_trees()
    draw_map()

if __name__ == '__main__':
    asset = {
        CROSSROAD: Image.open('asset/crossroad.png').convert("RGBA"),
        'tjunction_up': Image.open('asset/tup.png').convert("RGBA"),
        'tjunction_down': Image.open('asset/tlow.png').convert("RGBA"),
        'tjunction_left': Image.open('asset/tleft.png').convert("RGBA"),
        'tjunction_right': Image.open('asset/tright.png').convert("RGBA"),
        'turn_right_up': Image.open('asset/lowleft.png').convert("RGBA"),
        'turn_left_up': Image.open('asset/lowright.png').convert("RGBA"),
        'turn_right_down': Image.open('asset/upright.png').convert("RGBA"),
        'turn_left_down': Image.open('asset/upleft.png').convert("RGBA"),
        'vertical_road': Image.open('asset/verroad.png').convert("RGBA"),
        'horizontal_road': Image.open('asset/horroad.png').convert("RGBA"),
        'tree': Image.open('asset/tree.png').convert("RGBA"),
        BIG_BUILDING: Image.open('asset/big_building.png').convert("RGBA"),
        MEDIUM_BUILDING: Image.open('asset/med_building.png').convert("RGBA"),
        SMALL_BUILDING: Image.open('asset/small_building.png').convert("RGBA"),
        HOUSE: Image.open('asset/house.png').convert("RGBA"),
        EMPTY: Image.open('asset/rumput.png').convert("RGBA")
    }
    generate_map()
    place_buildings()
    place_trees()
    draw_map()
    plt.show()
