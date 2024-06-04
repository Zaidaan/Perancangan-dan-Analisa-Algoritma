<<<<<<< Updated upstream
from PIL import Image, ImageDraw
import random

# Ukuran gambar dan jumlah langkah
scale = 10
width = 150 * scale
height = 150 * scale
max_count = 10

curve = Image.open("image/curve.png")
road = Image.open("image/road.png")
building = Image.open("image/big_building.png")
house = Image.open("image/house.png")
buildings = [building,house]
tree = Image.open("image/tree.png")
image = Image.new("RGBA", (width, height), color="green")
images = Image.new("RGBA", (width, height), color="green")
draw = ImageDraw.Draw(image)
draws = ImageDraw.Draw(images)
trees = [tree]
titikSudut = [(0,0),(width-(2*scale),height-(2*scale)),(0,height-(2*scale)),(width-(2*scale),0)]

direction = ["atas","bawah","kanan","kiri"]
startPoint = { "atas" : "bawah", "bawah" : "atas", "kanan" : "kiri","kiri" : "kanan"}
move = { "atas" : [0,2*scale], "bawah" :[0,-2*scale], "kanan" : [2*scale,0],"kiri" : [-2*scale,0]}


def makeRoads(x,y,arah,count,length):
    global width, height
    w, h = (2*scale, 2*scale) 
    draw.rectangle( xy = (x,y, x + w , y + h), fill = (0,0,0))
    if not count :
        count = max_count
        if not random.randint(0,3):
            titikSudut.append((x,y))
            arah = random.choice(direction[2:] if arah == "atas" or arah == "bawah" else direction[:2])
    if ( length > 450 and (x<0 or y<0 or x >= width or y >= height) ) or length >= 700:
        return
    if (x >= 0 and x < width-2) and (y >= 0 and y < height-2):
        makeRoads(x+move[arah][0], y+move[arah][1],arah,count-1,length+1)
    else :
        titikSudut.append((x%width, y%height))
        titikSudut.append(((width+x+move[arah][0])%width, (height+y+move[arah][1])%height))
        makeRoads((width+x+move[arah][0])%width, (height+y+move[arah][1])%height,arah,max_count,length+1)
    

def render():
    directions = random.choice(direction)
    if directions == "atas":
        x = max_count * random.randint(1,width/max_count)
        y = 0
    elif directions == "bawah":
        x = max_count * random.randint(1,width/max_count)
        y = height-1
    elif direction == "kanan":
        x = 0
        y = max_count * random.randint(1,height/max_count)
    else:
        x = width-1
        y = max_count * random.randint(1,height/max_count)
    makeRoads(x,y,directions,max_count,1)
    


def drawArea(x,y,x1,y1,side):
    padding  = 2*scale
    x += padding ; y+= padding
    if x >= x1-scale or y >= y1-scale:
        return
    curX,curY = x ,y
    #draw.rectangle( xy = (x,y, x1-scale ,y1-scale), fill = (255,0,255))
    
    gedung = random.choice(buildings)
    if  gedung.size[0] < (x1-x-scale) and  gedung.size[1] < (y1-y-scale):
        image.paste(gedung,(x,y))
    elif (x1-x) > tree.size[0] and (y1-y) > tree.size[1] :
        gedung = random.choice(trees)
        image.paste(gedung,(x,y))
    while (curX + gedung.size[0] + padding) < x1 and side:
        size = gedung.size[0] + scale
        if y+building.size[0]-padding < y1:
            drawArea(curX+size,y-padding,x1,y+building.size[0]-padding,False)
        curX += size + scale
    while (curY + gedung.size[1] + padding) < y1 and side:
        size = gedung.size[1] + scale
        if x+building.size[1]-padding < x1:
            drawArea(x-padding,curY+size,x+building.size[1]-padding,y1,False)
        curY += size + scale
    
    if (x+gedung.size[0]-padding+scale)<x1 and (y+gedung.size[1]-padding+scale) < y1 and not side:
        drawArea(x+gedung.size[0],y+gedung.size[1],x1,y1,True)

def search():
    for idx, ver in enumerate(titikSudut):
        minX  = 0
        nearX = width
        nearY = height
        minY = 0
        maxX = 0
        maxY = 0
        for i in range(0,len(titikSudut)):
            if i == idx :
               continue
            if titikSudut[i][0] > ver[0] and titikSudut[i][0]  < nearX:
                nearX = titikSudut[i][0]
            if titikSudut[i][1] > ver[1] and titikSudut[i][1]  < nearY:
                nearY = titikSudut[i][1]
            if titikSudut[i][0] >= minX and titikSudut[i][0] < ver[0]:
               minX = titikSudut[i][0]
               maxY = titikSudut[i][1]
            if titikSudut[i][1] >= minY and titikSudut[i][1] < ver[1]:
               minY = titikSudut[i][1]
               maxX = titikSudut[i][0]
        if minX > 0 and minY > 0:
            print("jumpa")
            if (minX,minY) not in titikSudut:
                titikSudut.append((minX,minY)) 
            if (maxX,maxY) not in titikSudut:
                titikSudut.append((maxX,maxY))
            print(ver, minX,minY)
            drawArea(minX+scale,minY+scale,ver[0],ver[1],True)
        if (nearX,nearY) not in titikSudut:
            titikSudut.append((nearX,nearY))
        if minX == 0 or minY == 0:
            drawArea(minX,minY,ver[0],ver[1],True)

render()
tmp = titikSudut

search()
print(titikSudut)
print(len(titikSudut))
for ver in titikSudut:
    draws.rectangle(xy = (ver[0],ver[1],ver[0]+(2*scale),ver[1]+(2*scale)),fill=(0,0,0))
# Menyimpan gambar sebagai file
image.show()
image.save("main.png")
=======
import random
from PIL import Image, ImageDraw

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
    BIG_BUILDING: 50,
    MEDIUM_BUILDING: 100,
    SMALL_BUILDING: 250,
    HOUSE: 500,
    TREE: 500
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

    canvas.save('citymap.png', format='PNG')
    canvas.show()
    
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
        BIG_BUILDING: Image.open('asset/big_building.png').convert("RGBA"),
        MEDIUM_BUILDING: Image.open('asset/medium_building.png').convert("RGBA"),
        SMALL_BUILDING: Image.open('asset/small_building.png').convert("RGBA"),
        HOUSE: Image.open('asset/house.png').convert("RGBA"),
        EMPTY: Image.open('asset/rumput.png').convert("RGBA")
    }
    generate_map()
    place_buildings()
    place_trees()
    draw_map()
>>>>>>> Stashed changes
