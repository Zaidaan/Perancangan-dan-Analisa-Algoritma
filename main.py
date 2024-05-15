import pygame
import random
import sys

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
big_building_img = pygame.image.load('big_building.png')
medium_building_img = pygame.image.load('medium_building.png')
small_building_img = pygame.image.load('small_building.png')
house_img = pygame.image.load('house.png')
road_straight_img = pygame.image.load('road_straight.png')
road_turn_img = pygame.image.load('road_turn.png')

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

def place_road(grid, start_x, start_y, end_x, end_y, surface):
    if start_x == end_x:
        for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
            if grid[y][start_x] == 0:
                grid[y][start_x] = 1
                rotated_img = pygame.transform.rotate(road_straight_img, 90)
                surface.blit(rotated_img, (start_x * CELL_SIZE, y * CELL_SIZE))
    elif start_y == end_y:
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            if grid[start_y][x] == 0:
                grid[start_y][x] = 1
                surface.blit(road_straight_img, (x * CELL_SIZE, start_y * CELL_SIZE))
    else:
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            if grid[start_y][x] == 0:
                grid[start_y][x] = 1
                surface.blit(road_straight_img, (x * CELL_SIZE, start_y * CELL_SIZE))
        for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
            if grid[y][end_x] == 0:
                grid[y][end_x] = 1
                rotated_img = pygame.transform.rotate(road_straight_img, 90)
                surface.blit(rotated_img, (end_x * CELL_SIZE, y * CELL_SIZE))
        
        # Determine the correct rotation for the turn
        if (start_x < end_x and start_y < end_y):
            rotated_turn = pygame.transform.rotate(road_turn_img, 0)
        elif (start_x > end_x and start_y < end_y):
            rotated_turn = pygame.transform.rotate(road_turn_img, 90)
        elif (start_x < end_x and start_y > end_y):
            rotated_turn = pygame.transform.rotate(road_turn_img, 270)
        else:  # (start_x > end_x and start_y > end_y)
            rotated_turn = pygame.transform.rotate(road_turn_img, 180)
        
        surface.blit(rotated_turn, (end_x * CELL_SIZE, end_y * CELL_SIZE))

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

    for i in range(len(placed_buildings) - 1):
        _, _, _, _, start_x, start_y = placed_buildings[i]
        _, _, _, _, end_x, end_y = placed_buildings[i + 1]
        place_road(grid, start_x, start_y, end_x, end_y, surface)

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