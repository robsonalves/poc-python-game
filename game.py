import pygame
from settings import WIDTH, HEIGHT, WIN, FPS, WHITE, BLUE, BLACK, jump_sound, collect_star_sound, collect_coconut_sound, NUM_PLATFORMS, PLATFORM_HEIGHT
from player import Player
from game_platform import Platform
from item import Item
from enemy import Enemy
from utils import create_platforms, create_items, draw_button, create_enemies

def reset_game(level):
    platforms = create_platforms(NUM_PLATFORMS + level)  # Aumentar o número de plataformas com o nível
    ground = Platform(0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT)
    platforms.add(ground)
    items = create_items(platforms, level)  # Passar o nível para criar itens
    enemies = create_enemies(level)  # Criar inimigos com base no nível
    return platforms, items, enemies, 0

def setup_game(level):
    player = Player(level)  # Passar o nível para ajustar a velocidade do jogador
    platforms, items, enemies, score = reset_game(level)
    return player, platforms, items, enemies, score

def main():
    clock = pygame.time.Clock()
    run = True
    level = 1

    player, platforms, items, enemies, score = setup_game(level)

    button_x, button_y, button_width, button_height = 650, 10, 140, 50  # Posição e tamanho do botão

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    # Reiniciar o jogo
                    level = 1
                    player, platforms, items, enemies, score = setup_game(level)

        player.update(platforms)
        platforms.update()
        items.update()
        enemies.update()

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
            print("Game Over")
            run = False  # Finalizar o jogo se o jogador colidir com um inimigo

        # Verificar se todos os itens foram coletados
        if not items:
            level += 1  # Aumentar o nível
            player, platforms, items, enemies, _ = setup_game(level)

        WIN.fill(WHITE)
        platforms.draw(WIN)
        items.draw(WIN)
        enemies.draw(WIN)
        player.draw(WIN)
        
        # Desenhar botão de reiniciar
        draw_button(WIN, 'Restart', button_x, button_y, button_width, button_height, BLUE)

        # Exibir pontuação e nível
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}  Level: {level}', True, BLACK)
        WIN.blit(text, (10, 10))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
