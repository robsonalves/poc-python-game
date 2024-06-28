import pygame
import socket
import threading
from settings import WIDTH, HEIGHT, WIN, FPS, WHITE, BLUE, BLACK, RED, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_LIFE, jump_sound, collect_star_sound, collect_coconut_sound, enemy_hit_sound, obstacle_hit_sound, NUM_PLATFORMS, PLATFORM_HEIGHT
from player import Player
from game_platform import Platform
from item import Item
from enemy import Enemy
from obstacle import Obstacle
from utils import create_platforms, create_items, draw_button, create_enemies, create_obstacles

# Configurações do cliente
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
ADDR = (SERVER_IP, SERVER_PORT)

# Inicialização do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Função para enviar dados para o servidor
def send_data(data):
    client.send(data.encode("utf-8"))

# Função para receber dados do servidor
def receive_data():
    while True:
        try:
            data = client.recv(1024).decode("utf-8")
            if data:
                handle_data(data)
        except:
            client.close()
            break

# Função para lidar com dados recebidos do servidor
def handle_data(data):
    global other_players
    x, y = map(int, data.split(","))
    other_players.append((x, y))

# Inicializar thread para receber dados
thread = threading.Thread(target=receive_data)
thread.start()

# Variáveis de jogo
level = 1
other_players = []

def reset_game(level):
    platforms = create_platforms(NUM_PLATFORMS + level)
    ground = Platform(0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT)
    platforms.add(ground)
    items = create_items(platforms, level)
    enemies = create_enemies(level)
    obstacles = create_obstacles(platforms, items)  # Criar obstáculos próximos aos itens coletáveis
    return platforms, items, enemies, obstacles, 0

def setup_game(level):
    player = Player(level)
    platforms, items, enemies, obstacles, score = reset_game(level)
    player.life = PLAYER_LIFE  # Reiniciar vida do jogador
    return player, platforms, items, enemies, obstacles, score

def main():
    global level
    clock = pygame.time.Clock()
    run = True

    player, platforms, items, enemies, obstacles, score = setup_game(level)

    button_x, button_y, button_width, button_height = 650, 10, 140, 50

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    level = 1
                    player, platforms, items, enemies, obstacles, score = setup_game(level)

        player.update(platforms)
        platforms.update()
        items.update()
        enemies.update()
        obstacles.update()

        # Enviar posição do jogador para o servidor
        send_data(f"{player.rect.x},{player.rect.y}")

        # Checar colisão com itens
        collected_items = pygame.sprite.spritecollide(player, items, True)
        for item in collected_items:
            if item.item_type == 'star':
                score += 10
                collect_star_sound.play()
            elif item.item_type == 'coconut':
                score += 5
                collect_coconut_sound.play()

        # Checar colisão com inimigos
        if pygame.sprite.spritecollideany(player, enemies):
            enemy_hit_sound.play()
            font = pygame.font.Font(None, 72)
            text = font.render("Ouchhh, you have been bitten", True, BLACK)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            player, platforms, items, enemies, obstacles, score = setup_game(level)

        # Checar colisão com obstáculos
        collided_obstacle = pygame.sprite.spritecollideany(player, obstacles)
        if collided_obstacle:
            obstacle_hit_sound.play()
            if collided_obstacle.obstacle_type == 'spike':
                font = pygame.font.Font(None, 72)
                text = font.render("Game Over!", True, RED)
                WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                level = 1
                player, platforms, items, enemies, obstacles, score = setup_game(level)
            elif collided_obstacle.obstacle_type == 'drain':
                player.life -= 1

        # Verificar se todos os itens foram coletados
        if not items:
            level += 1
            player, platforms, items, enemies, obstacles, _ = setup_game(level)

        WIN.fill(WHITE)
        platforms.draw(WIN)
        items.draw(WIN)
        enemies.draw(WIN)
        obstacles.draw(WIN)
        player.draw(WIN)

        # Desenhar outros jogadores
        for pos in other_players:
            pygame.draw.rect(WIN, BLUE, (pos[0], pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))

        # Desenhar botão de reiniciar
        draw_button(WIN, 'Restart', button_x, button_y, button_width, button_height, BLUE)

        # Exibir pontuação, nível e vida do jogador
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}  Level: {level}  Life: {player.life}', True, BLACK)
        WIN.blit(text, (10, 10))

        pygame.display.update()

    pygame.quit()
    client.close()

if __name__ == "__main__":
    main()
