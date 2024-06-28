import random
import pygame
from settings import PLATFORM_WIDTH, PLATFORM_HEIGHT, WIDTH, HEIGHT, WHITE
from game_platform import Platform
from item import Item
from enemy import Enemy
from obstacle import Obstacle

def create_platforms(num_platforms):
    platforms = pygame.sprite.Group()
    for _ in range(num_platforms):
        platform = Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), random.randint(HEIGHT // 2, HEIGHT - PLATFORM_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.add(platform)
    return platforms

def create_items(platforms, level):
    items = pygame.sprite.Group()
    item_positions = set()
    item_types = ['star'] * (3 + level) + ['coconut'] * (2 + level)
    for item_type in item_types:
        item = create_item_near_platform(platforms, item_type, item_positions)
        items.add(item)
    return items

def create_item_near_platform(platforms, item_type, item_positions):
    while True:
        platform = random.choice(platforms.sprites())
        x = random.randint(platform.rect.left, platform.rect.right)
        y = platform.rect.top - 30
        if (x, y) not in item_positions:
            item_positions.add((x, y))
            item = Item(x, y, item_type)
            print(f"Created item: {item_type} at ({x}, {y})")
            return item

def create_enemies(level):
    enemies = pygame.sprite.Group()
    for _ in range(level):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 2)
        enemy = Enemy(x, y)
        enemies.add(enemy)
    return enemies

def create_obstacles(platforms, items):
    obstacles = pygame.sprite.Group()
    for item in items:
        if random.random() < 0.5:  # 50% chance de criar um obstáculo perto de um item
            x = item.rect.x + random.choice([-50, 50])
            y = item.rect.y
            obstacle = Obstacle(x, y, 'drain')
            obstacles.add(obstacle)
    return obstacles

def draw_button(win, text, x, y, width, height, color):
    pygame.draw.rect(win, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    win.blit(text_surf, text_rect)
