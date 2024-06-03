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

def place_building(grid, width, height, image, surface):
    while True:
        x = random.randint(0, GRID_SIZE - width)
        y = random.randint(0, GRID_SIZE - height)
        if all(grid[y+i][x+j] == 0 for i in range(height) for j in range(width)):
            for i in range(height):
                for j in range(width):
                    grid[y+i][x+j] = 1
            surface.blit(image, (x * CELL_SIZE, y * CELL_SIZE))
            front_x = x + width // 2
            front_y = y + height
            return (x, y, width, height, front_x, front_y)

def place_road(surface, path):
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        if x1 == x2:  # Vertical road
            for y in range(min(y1, y2), max(y1, y2) + 1):
                surface.blit(road_straight_img, (x1 * CELL_SIZE, y * CELL_SIZE))
        elif y1 == y2:  # Horizontal road
            for x in range(min(x1, x2), max(x1, x2) + 1):
                surface.blit(road_straight_img, (x * CELL_SIZE, y1 * CELL_SIZE))
        else:  # Diagonal road
            for x in range(min(x1, x2), max(x1, x2) + 1):
                surface.blit(road_straight_img, (x * CELL_SIZE, y1 * CELL_SIZE))
            for y in range(min(y1, y2), max(y1, y2) + 1):
                surface.blit(road_straight_img, (x2 * CELL_SIZE, y * CELL_SIZE))

            # Determine the correct rotation for the turn
            if x1 < x2:
                rotated_turn = pygame.transform.rotate(road_turn_img, 270)
            elif x1 > x2:
                rotated_turn = pygame.transform.rotate(road_turn_img, 90)
            elif x1 < x2:
                rotated_turn = pygame.transform.rotate(road_turn_img, 270)
            else:  # (x1 > x2 and y1 > y2)
                rotated_turn = pygame.transform.rotate(road_turn_img, 90)

            surface.blit(rotated_turn, (x2 * CELL_SIZE, y2 * CELL_SIZE))




def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_map():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    surface = pygame.Surface((MAP_SIZE, MAP_SIZE))
    surface.fill(BLACK)

    buildings = [
        (10, 5, big_building_img, 1),
        (5, 3, medium_building_img, 4),
        (2, 2, small_building_img, 10),
        (1, 2, house_img, 10)
    ]

    placed_buildings = []
    for width, height, image, count in buildings:
        for _ in range(count):
            building_info = place_building(grid, width, height, image, surface)
            placed_buildings.append(building_info)

    # Build the graph
    graph = {i: [] for i in range(len(placed_buildings))}
    for i in range(len(placed_buildings)):
        x1, y1, w1, h1, front_x1, front_y1= placed_buildings[i]
        for j in range(i + 1, len(placed_buildings)):
            x2, y2, w2, h2, front_x2, front_y2 = placed_buildings[j]
            distance = euclidean_distance(x1, y1, x2, y2)
            graph[i].append((j, distance))
            graph[j].append((i, distance))

    # Minimum Spanning Tree Algorithm (Prim's Algorithm)
    mst = set()
    visited = set()
    start_node = random.randint(0, len(placed_buildings) - 1)
    visited.add(start_node)
    while len(visited) < len(placed_buildings):
        min_edge = None
        min_distance = float('inf')
        for node in visited:
            for neighbor, distance in graph[node]:
                if neighbor not in visited and distance < min_distance:
                    min_edge = (node, neighbor)
                    min_distance = distance
        mst.add((min_edge[0], min_edge[1]))
        visited.add(min_edge[1])

    # Place roads based on MST edges
    for edge in mst:
        x1, y1, w1, h1, front_x1, front_y1 = placed_buildings[edge[0]]
        x2, y2, w2, h2, front_x2, front_y2 = placed_buildings[edge[1]]
        path = [(front_x1, front_y1), (front_x2, front_y2)]
        place_road(surface, path)

    draw_grid(surface)
    return surface


# Main loop
def main():
    viewport_x, viewport_y = 0, 0
    clock = pygame.time.Clock()
    button_rect = pygame.Rect(VIEWPORT_SIZE - BUTTON_SIZE - 10, VIEWPORT_SIZE - BUTTON_SIZE - 10, BUTTON_SIZE, BUTTON_SIZE)

    map_surface = generate_map()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    map_surface = generate_map()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            viewport_x = max(0, viewport_x - VIEWPORT_SCROLL_SPEED)
        if keys[pygame.K_RIGHT]:
            viewport_x = min(MAP_SIZE - VIEWPORT_SIZE, viewport_x + VIEWPORT_SCROLL_SPEED)
        if keys[pygame.K_UP]:
            viewport_y = max(0, viewport_y - VIEWPORT_SCROLL_SPEED)
        if keys[pygame.K_DOWN]:
            viewport_y = min(MAP_SIZE - VIEWPORT_SIZE, viewport_y + VIEWPORT_SCROLL_SPEED)

        SCREEN.fill(BLACK)
        SCREEN.blit(map_surface, (-viewport_x, -viewport_y))
        pygame.draw.rect(SCREEN, RED, button_rect)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
