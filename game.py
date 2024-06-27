import pygame
from settings import WIDTH, HEIGHT, WIN, FPS, WHITE, BLUE, jump_sound, collect_star_sound, collect_coconut_sound, NUM_PLATFORMS, PLATFORM_HEIGHT, BLACK
from player import Player
from game_platform import Platform
from item import Item
from utils import create_platforms, create_items, draw_button

def reset_game():
    platforms = create_platforms(NUM_PLATFORMS)
    ground = Platform(0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT)
    platforms.add(ground)
    items = create_items(platforms)
    return platforms, items, 0

def setup_game():
    player = Player()
    platforms, items, score = reset_game()

    return player, platforms, items, score

def main():
    clock = pygame.time.Clock()
    run = True

    player, platforms, items, score = setup_game()

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
                    player, platforms, items, score = setup_game()

        player.update(platforms)
        platforms.update()
        items.update()

        # Checar colisão com itens
        collected_items = pygame.sprite.spritecollide(player, items, True)
        for item in collected_items:
            if item.item_type == 'star':
                score += 10
                collect_star_sound.play()
            elif item.item_type == 'coconut':
                score += 5
                collect_coconut_sound.play()

        # Verificar se todos os itens foram coletados
        if not items:
            platforms, items, _ = reset_game()

        WIN.fill(WHITE)
        platforms.draw(WIN)
        items.draw(WIN)
        player.draw(WIN)
        
        # Desenhar botão de reiniciar
        draw_button(WIN, 'Restart', button_x, button_y, button_width, button_height, BLUE)

        # Exibir pontuação
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, BLACK)
        WIN.blit(text, (10, 10))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
