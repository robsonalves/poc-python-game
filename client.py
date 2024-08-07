import pygame
import socket
import threading
import json
from settings import WIDTH, HEIGHT, WIN, FPS, WHITE, BLUE, BLACK, RED, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_LIFE, jump_sound, collect_star_sound, collect_coconut_sound, enemy_hit_sound, NUM_PLATFORMS, PLATFORM_HEIGHT
from player import Player
from game_platform import Platform
from item import Item
from enemy import Enemy
from utils import create_platforms, create_items, draw_button, create_enemies, save_score, load_highscores, display_highscores

# Configurações do cliente
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
ADDR = (SERVER_IP, SERVER_PORT)

# Inicialização do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Função para enviar dados para o servidor
def send_data(data):
    try:
        client.send(data.encode("utf-8"))
    except OSError as e:
        print(f"Erro ao enviar dados: {e}")

# Função para receber dados do servidor
def receive_data():
    while True:
        try:
            data = client.recv(1024).decode("utf-8")
            if data:
                handle_data(data)
        except OSError as e:
            print(f"Erro ao receber dados: {e}")
            client.close()
            break

# Função para lidar com dados recebidos do servidor
def handle_data(data):
    global other_players, enemies
    if data.startswith("["):
        enemies_data = json.loads(data)
        enemies.clear()
        for enemy_data in enemies_data:
            enemies.append(Enemy(enemy_data['x'], enemy_data['y'], enemy_data['speed']))
    else:
        x, y = map(int, data.split(","))
        other_players.append((x, y))

# Inicializar thread para receber dados
thread = threading.Thread(target=receive_data)
thread.start()

# Variáveis de jogo
level = 1
other_players = []
enemies = []

def reset_game(level):
    platforms = create_platforms(NUM_PLATFORMS + level)
    ground = Platform(0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT)
    platforms.add(ground)
    items = create_items(platforms, level)
    return platforms, items, 0

def setup_game(level):
    player = Player(level)
    platforms, items, score = reset_game(level)
    player.life = PLAYER_LIFE  # Reiniciar vida do jogador
    return player, platforms, items, score

def main():
    global level
    clock = pygame.time.Clock()
    run = True

    player, platforms, items, score = setup_game(level)
    player_name = input("Enter your name: ")  # Pedir o nome do jogador

    button_x, button_y, button_width, button_height = 650, 10, 140, 50

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and mouse_y:
                    level = 1
                    player, platforms, items, score = setup_game(level)

        player.update(platforms)
        platforms.update()
        items.update()
        for enemy in enemies:
            enemy.update()

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
            player, platforms, items, score = setup_game(level)

        # Verificar se todos os itens foram coletados
        if not items:
            level += 1
            player, platforms, items, score = setup_game(level)

        WIN.fill(WHITE)  # Limpar a tela antes de desenhar
        platforms.draw(WIN)
        items.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
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

    # Salvar a pontuação ao final do jogo
    save_score(player_name, score)

    # Exibir o ranking
    run = True
    while run:
        WIN.fill(WHITE)
        highscores = load_highscores()
        display_highscores(WIN, highscores)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    client.close()

if __name__ == "__main__":
    main()
