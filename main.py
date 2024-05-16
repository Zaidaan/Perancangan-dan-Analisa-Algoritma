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