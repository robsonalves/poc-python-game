import random
import pygame
import os
from game_platform import Platform
from item import Item
from enemy import Enemy
from settings import PLATFORM_WIDTH, PLATFORM_HEIGHT, WIDTH, HEIGHT, WHITE, BLACK

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
        # Escolher uma posição nas bordas da tela
        if random.choice([True, False]):
            x = random.choice([0, WIDTH])  # Borda esquerda ou direita
            y = random.randint(0, HEIGHT)  # Qualquer posição verticalmente
        else:
            x = random.randint(0, WIDTH)  # Qualquer posição horizontalmente
            y = random.choice([0, HEIGHT])  # Borda superior ou inferior
        enemy = Enemy(x, y)
        enemies.add(enemy)
    return enemies

def draw_button(win, text, x, y, width, height, color):
    pygame.draw.rect(win, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    win.blit(text_surf, text_rect)

def save_score(name, score):
    scores = load_highscores()
    updated = False
    for i, (n, s) in enumerate(scores):
        if n == name:
            if score > s:
                scores[i] = (name, score)
            updated = True
            break
    if not updated:
        scores.append((name, score))
    scores.sort(key=lambda x: x[1], reverse=True)
    with open("highscores.txt", "w") as file:
        for n, s in scores:
            file.write(f"{n},{s}\n")

def load_highscores():
    if not os.path.exists("highscores.txt"):
        return []
    with open("highscores.txt", "r") as file:
        scores = [line.strip().split(",") for line in file]
        scores = [(name, int(score)) for name, score in scores]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

def display_highscores(win, scores):
    font = pygame.font.Font(None, 36)
    y_offset = 100
    for idx, (name, score) in enumerate(scores[:5], start=1):  # Mostrar top 5
        text = font.render(f"{idx}. {name} - {score}", True, BLACK)
        win.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
