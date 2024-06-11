import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Constants
CELL_SIZE = 20
GRID_SIZE = 150
VIEWPORT_SIZE = 600
MAP_SIZE = GRID_SIZE * CELL_SIZE
SCREEN = pygame.display.set_mode((VIEWPORT_SIZE, VIEWPORT_SIZE))
BUTTON_SIZE = 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRID_COLOR = (200, 200, 200)
VIEWPORT_SCROLL_SPEED = 20

# Building counts
big_building_count = 5
medium_building_count = 10
small_building_count = 20
house_count = 30

# Define a Building class
class Building:
    def __init__(self, x, y, width, height, middle_x, front_y, right_x, middle_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.middle_x = middle_x
        self.front_y = front_y
        self.right_x = right_x
        self.middle_y = middle_y

def update_building_counts(event):
    global big_building_count, medium_building_count, small_building_count, house_count
    if event.key == pygame.K_1:
        big_building_count += 1
    elif event.key == pygame.K_2:
        big_building_count = max(0, big_building_count - 1)
    elif event.key == pygame.K_3:
        medium_building_count += 1
    elif event.key == pygame.K_4:
        medium_building_count = max(0, medium_building_count - 1)
    elif event.key == pygame.K_5:
        small_building_count += 1
    elif event.key == pygame.K_6:
        small_building_count = max(0, small_building_count - 1)
    elif event.key == pygame.K_7:
        house_count += 1
    elif event.key == pygame.K_8:
        house_count = max(0, house_count - 1)
    elif event.key == pygame.K_SPACE:
        return True  # Generate new city layout
    return False

# Load images
big_building_img = pygame.image.load('asset/big_building.png')
medium_building_img = pygame.image.load('asset/medium_building.png')
small_building_img = pygame.image.load('asset/small_building.png')
house_img = pygame.image.load('asset/house.png')
road_straight_img = pygame.image.load('asset/road_straight.png')
road_turn_img = pygame.image.load('asset/road_turn.png')

# Resize images to match the cell sizes
big_building_img = pygame.transform.scale(big_building_img, (10 * CELL_SIZE, 5 * CELL_SIZE))
medium_building_img = pygame.transform.scale(medium_building_img, (5 * CELL_SIZE, 3 * CELL_SIZE))
small_building_img = pygame.transform.scale(small_building_img, (2 * CELL_SIZE, 2 * CELL_SIZE))
house_img = pygame.transform.scale(house_img, (1 * CELL_SIZE, 2 * CELL_SIZE))
road_straight_img = pygame.transform.scale(road_straight_img, (CELL_SIZE, CELL_SIZE))
road_turn_img = pygame.transform.scale(road_turn_img, (CELL_SIZE, CELL_SIZE))

def draw_grid(surface):
    for x in range(0, MAP_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, MAP_SIZE))
    for y in range(0, MAP_SIZE, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (MAP_SIZE, y))

def place_building(grid, width, height, image, surface, buffer=10):
    while True:
        x = random.randint(0, GRID_SIZE - width - 2 * buffer)
        y = random.randint(0, GRID_SIZE - height - 2 * buffer)
        if all(grid[y+i+buffer][x+j+buffer] == 0 for i in range(height) for j in range(width)):
            for i in range(height + 2 * buffer):
                for j in range(width + 2 * buffer):
                    grid[y+i][x+j] = 1
            surface.blit(image, ((x + buffer) * CELL_SIZE, (y + buffer) * CELL_SIZE))
            middle_x = x + width // 2 + buffer
            front_y = y + height + buffer
            right_x = x + width + buffer
            middle_y = y + height // 2 + buffer

            return Building(x + buffer, y + buffer, width, height, middle_x, front_y, right_x, middle_y)

def place_road(surface, path):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        if x1 == x2:  # Vertical road
            for y in range(min(y1, y2), max(y1, y2) + 1):
                surface.blit(pygame.transform.rotate(road_straight_img, 90), (x1 * CELL_SIZE, y * CELL_SIZE))
        elif y1 == y2:  # Horizontal road
            for x in range(min(x1, x2), max(x1, x2) + 1):
                surface.blit(road_straight_img, (x * CELL_SIZE, y1 * CELL_SIZE))
        else:  # Diagonal road
            for x in range(min(x1, x2), max(x1, x2) + 1):
                surface.blit(road_straight_img, (x * CELL_SIZE, y1 * CELL_SIZE))
            for y in range(min(y1, y2), max(y1, y2) + 1):
                surface.blit(road_straight_img, (x2 * CELL_SIZE, y * CELL_SIZE))

            # Determine the correct rotation for the turn
            if x1 < x2 and y1 < y2:
                rotated_turn = pygame.transform.rotate(road_turn_img, 0)
            elif x1 > x2 and y1 < y2:
                rotated_turn = pygame.transform.rotate(road_turn_img, 90)
            elif x1 < x2 and y1 > y2:
                rotated_turn = pygame.transform.rotate(road_turn_img, 270)
            else:  # (x1 > x2 and y1 > y2)
                rotated_turn = pygame.transform.rotate(road_turn_img, 180)

            surface.blit(rotated_turn, (x2 * CELL_SIZE, y2 * CELL_SIZE))

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def generate_map():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    surface = pygame.Surface((MAP_SIZE, MAP_SIZE))
    surface.fill(WHITE)

    placed_buildings = []
    building_types = [
        (10, 5, big_building_img, big_building_count),
        (5, 3, medium_building_img, medium_building_count),
        (2, 2, small_building_img, small_building_count),
        (1, 2, house_img, house_count)
    ]

    for width, height, image, count in building_types:
        for _ in range(count):
            building = place_building(grid, width, height, image, surface)
            placed_buildings.append(building)

    # Build the graph
    graph = {i: [] for i in range(len(placed_buildings))}
    for i, building1 in enumerate(placed_buildings):
        x1, y1 = building1.x, building1.y
        for j, building2 in enumerate(placed_buildings):
            if i != j:
                x2, y2 = building2.x, building2.y
                distance = euclidean_distance(x1, y1, x2, y2)
                graph[i].append((j, distance))

    # Find all possible connections and their distances
    all_edges = []
    for node, connections in graph.items():
        for neighbor, distance in connections:
            all_edges.append((node, neighbor, distance))

    # Sort all edges by their distance (shortest first)
    all_edges.sort(key=lambda x: x[2])

    # Initialize union-find data structure to keep track of connected components
    parent = {i: i for i in range(len(placed_buildings))}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rootX = find(x)
        rootY = find(y)
        if rootX != rootY:
            parent[rootY] = rootX

    # Kruskal's algorithm to create the minimum spanning tree
    mst_edges = []
    for node1, node2, distance in all_edges:
        if find(node1) != find(node2):
            union(node1, node2)
            mst_edges.append((node1, node2))

    # Generate the paths based on MST edges
    for node1, node2 in mst_edges:
        building1 = placed_buildings[node1]
        building2 = placed_buildings[node2]
        path = [(building1.middle_x, building1.front_y), (building2.middle_x, building2.front_y)]
        place_road(surface, path)

    return surface

# Main loop
def main():
    clock = pygame.time.Clock()
    viewport_x, viewport_y = 0, 0

    # Generate the map once
    generated_map = generate_map()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if update_building_counts(event):
                    # Regenerate map when building counts are updated
                    generated_map = generate_map()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            viewport_x = max(viewport_x - VIEWPORT_SCROLL_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            viewport_x = min(viewport_x + VIEWPORT_SCROLL_SPEED, MAP_SIZE - VIEWPORT_SIZE)
        if keys[pygame.K_UP]:
            viewport_y = max(viewport_y - VIEWPORT_SCROLL_SPEED, 0)
        if keys[pygame.K_DOWN]:
            viewport_y = min(viewport_y + VIEWPORT_SCROLL_SPEED, MAP_SIZE - VIEWPORT_SIZE)

        SCREEN.fill(WHITE)
        SCREEN.blit(generated_map, (-viewport_x, -viewport_y))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
