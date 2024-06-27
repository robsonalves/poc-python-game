import random
import pygame
from settings import PLATFORM_WIDTH, PLATFORM_HEIGHT, WIDTH, HEIGHT, WHITE
from game_platform import Platform
from item import Item

def create_platforms(num_platforms):
    platforms = pygame.sprite.Group()
    for _ in range(num_platforms):
        platform = Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), random.randint(HEIGHT // 2, HEIGHT - PLATFORM_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.add(platform)
    return platforms

def create_items(platforms, level):
    items = pygame.sprite.Group()
    item_positions = set()  # Manter as posições ocupadas para evitar sobreposição
    item_types = ['star'] * (3 + level) + ['coconut'] * (2 + level)  # Aumentar o número de itens com o nível
    for item_type in item_types:
        item = create_item_near_platform(platforms, item_type, item_positions)
        items.add(item)
    return items

def create_item_near_platform(platforms, item_type, item_positions):
    while True:
        platform = random.choice(platforms.sprites())
        x = random.randint(platform.rect.left, platform.rect.right)
        y = platform.rect.top - 30  # Posicionar o item logo acima da plataforma
        if (x, y) not in item_positions:
            item_positions.add((x, y))
            item = Item(x, y, item_type)
            print(f"Created item: {item_type} at ({x}, {y})")
            return item

def draw_button(win, text, x, y, width, height, color):
    pygame.draw.rect(win, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    win.blit(text_surf, text_rect)
