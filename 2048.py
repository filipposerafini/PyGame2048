import random
import math
import pygame
from pygame.locals import *

# Colors
BACKGROUND = (187, 173, 160)

TILE_COLOR = {
        '0' : (204, 192, 179),
        '2' : (238, 228, 218),
        '4' : (237, 224, 200),
        '8' : (242, 177, 121),
        '16' : (245, 149, 99),
        '32' : (246, 124, 95),
        '64' : (246, 94, 59),
        '128' : (237, 207, 114),
        '256' : (237, 204, 97),
        '512' : (237, 200, 80),
        '1024' : (237, 197, 63),
        '2048' : (237, 194, 46),
        '4096' : (62, 57, 51),
        '8192' : (70, 87, 240),
        }

TEXT_COLOR = {
        '2' : (119, 110, 101),
        '4' : (119, 110, 101),
        '8' : (249, 246, 242),
        '16' : (249, 246, 242),
        '32' : (249, 246, 242),
        '64' : (249, 246, 242),
        '128' : (249, 246, 242),
        '256' : (249, 246, 242),
        '512' : (249, 246, 242),
        '1024' : (249, 246, 242),
        '2048' : (249, 246, 242),
        '4096' : (249, 246, 242),
        '8192' : (249, 246, 242),
        }

# Defines
SIDES = 4
PADDING = 20
SCALING = 16
FONT_OFFSET = 15
FPS = 60
SPEED = 0.2
DISTANCE_THRESHOLD = 0.5
SCALE_SPEED = 0.1
SIZE_OFFSET = 1.5

# Tile Class
class Tile:

    def __init__(self, x, y, value):
        self.pos = pygame.Vector2(x, y)
        self.value = value
        self.dest = self.pos
        self.old_value = value
        self.distance = 0
        self.size = 0
        self.update = False

    def move(self, dx, dy, double):
        self.dest.x = dx
        self.dest.y = dy
        self.distance = self.pos.distance_to(self.dest)
        if double:
            self.old_value = self.value
            self.value *= 2
            self.size = cell_size * SIZE_OFFSET
            return self, self.value
        else:
            return self, 0

    def draw(self, surface, cell_size):
        if self.value != 0:

            # Tile Size
            if self.size != cell_size:
                self.size += (cell_size - self.size) * SCALE_SPEED

            # Tile Surface
            tile = pygame.Surface((self.size, self.size))
            tile.fill(BACKGROUND)
            tile_rect = tile.get_rect()

            # Tile Text
            text = str(self.old_value)
            pygame.draw.rect(tile, TILE_COLOR[text], tile_rect, border_radius=10)
            font = pygame.font.SysFont('Google Sans', int(self.size * 0.8 - FONT_OFFSET * (len(text) - 1)), bold=True)
            text_surf = font.render(text, True, TEXT_COLOR[text])
            text_rect = text_surf.get_rect()
            text_rect.center = tile_rect.center
            tile.blit(text_surf, text_rect)

            # Tile Position
            self.pos = self.pos.lerp(self.dest, SPEED)
            # self.pos = self.dest

            # Tile Value
            if self.pos.distance_to(self.dest) < DISTANCE_THRESHOLD:
                self.old_value = self.value

            rect = pygame.Rect(PADDING + cell_size / 2 - self.size / 2 + self.pos.x * (cell_size + PADDING), 
                               PADDING + cell_size / 2 - self.size / 2 + self.pos.y * (cell_size + PADDING), 
                               self.size, 
                               self.size)

            # Draw
            surface.blit(tile, rect)

# New Game
def new_game():
    tiles = [[Tile(x, y, 0) for x in range(SIDES)] for y in range(SIDES)]

    tiles = new_tile(tiles)
    tiles = new_tile(tiles)

    return tiles, 0

# New Tile
def new_tile(tiles):
    while True:
        x = random.randint(0, SIDES - 1)
        y = random.randint(0, SIDES - 1)

        if tiles[x][y].value == 0:
            value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
            tiles[x][y] = Tile(x, y, value)
            break
    return tiles

# Scroll Tiles
def vertical(tiles, min_y, max_y, direction):
    stuck = True 
    score = 0
    dump = []
    for y in range(min_y, max_y, -direction):
        for x in range(SIDES):
            if tiles[x][y].value != 0:
                moved = False
                double = False
                for ay in range(y + direction, min_y + direction * 2, direction):
                    if tiles[x][ay].value == 0:
                        moved = True
                        dy = ay
                        continue
                    elif tiles[x][ay].old_value == tiles[x][ay].value and tiles[x][ay].old_value == tiles[x][y].value:
                        moved = True
                        dy = ay
                        double = True
                        break
                    else:
                        break

                if moved:
                    dump.append(tiles[x][dy])
                    tiles[x][dy], points = tiles[x][y].move(x, dy, double)
                    tiles[x][y] = Tile(x, y, 0)
                    stuck = False
                    score += points
    return stuck, tiles, dump, score

def horizontal(tiles, min_x, max_x, direction):
    stuck = True
    score = 0
    dump = []
    for x in range (min_x, max_x, -direction):
        for y in range (SIDES):
            if tiles[x][y].value != 0:
                moved = False
                double = False
                for ax in range(x + direction, min_x + direction * 2, direction):
                    if tiles[ax][y].value == 0:
                        moved = True
                        dx = ax
                        continue
                    elif tiles[ax][y].old_value == tiles[ax][y].value and tiles[ax][y].old_value == tiles[x][y].value:
                        moved = True
                        dx = ax
                        double = True
                        break
                    else:
                        break
                if moved:
                    dump.append(tiles[dx][y])
                    tiles[dx][y], points = tiles[x][y].move(dx, y, double)
                    tiles[x][y] = Tile(x, y, 0)
                    stuck = False
                    score += points
    return stuck, tiles, dump, score

# Print Tiles
def print_tiles(tiles):
    for x in range(SIDES):
        for y in range(SIDES):
            print(tiles[y][x].value, end='\t')
        print('\n')
    print('\n')

# Init
pygame.init()
pygame.display.set_caption('2048')

# Screen
cell_size = int(pygame.display.Info().current_w / SCALING)
screen_size = SIDES * cell_size + (SIDES + 1) * PADDING
screen = pygame.display.set_mode((screen_size, screen_size))

# Clock
clock = pygame.time.Clock()

# New game
tiles, score = new_game()
dump = []

# Game Loop
running = True

while running:

    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            stuck = True
            dump.clear()

            if event.key == pygame.K_RETURN:
                tiles, score = new_game()

            elif event.key == pygame.K_SPACE:
                pass

            elif event.key == pygame.K_UP:
                min_y = 1
                max_y = SIDES
                direction = -1
                stuck, tiles, dump, points = vertical(tiles, min_y, max_y, direction)

            elif event.key == pygame.K_DOWN:
                min_y = SIDES - 2
                max_y = -1
                direction = 1
                stuck, tiles, dump, points = vertical(tiles, min_y, max_y, direction)

            elif event.key == pygame.K_LEFT:
                min_x = 1
                max_x = SIDES
                direction = -1
                stuck, tiles, dump, points = horizontal(tiles, min_x, max_x, direction)
    
            elif event.key == pygame.K_RIGHT:
                min_x = SIDES - 2
                max_x = -1
                direction = 1
                stuck, tiles, dump, points = horizontal(tiles, min_x, max_x, direction)
            else:
                continue

            if not stuck:
                tiles = new_tile(tiles)
                score += points

        else:
            continue

    # Draw Background
    screen.fill(BACKGROUND)
    for x in range(SIDES):
        for y in range(SIDES):
            rect = pygame.Rect(PADDING + x * (cell_size + PADDING), PADDING + y * (cell_size + PADDING), cell_size, cell_size)
            pygame.draw.rect(screen, TILE_COLOR['0'], rect, border_radius=10)

    # Draw Tiles
    for tile in dump:
        tile.draw(screen, cell_size)

    for x in range(SIDES):
        for y in range(SIDES):
            tiles[x][y].draw(screen, cell_size)

    pygame.display.flip()

# Quit
pygame.quit()
