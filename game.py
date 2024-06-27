import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Plataforma")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)

# FPS
FPS = 60

# Configurações do Jogador
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_VEL = 5
PLAYER_JUMP = 15  # Aumentar a força do pulo
GRAVITY = 1  # Gravidade ajustada

# Configurações das Plataformas
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 20
NUM_PLATFORMS = 10  # Número de plataformas aumentadas

# Carregar sons
jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
collect_star_sound = pygame.mixer.Sound("assets/sounds/coin.wav")
collect_coconut_sound = pygame.mixer.Sound("assets/sounds/pickup.wav")

# Carregar sprites (exemplo, você precisa substituir pelos seus próprios sprites)
player_sprite = pygame.image.load("assets/images/player.png")
star_sprite = pygame.image.load("assets/images/star.png")
coconut_sprite = pygame.image.load("assets/images/coconut.png")
platform_sprite = pygame.image.load("assets/images/platform.png")

# Classe do Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.vel_y = 0
        self.jumping = False
        self.jump_count = 0  # Contador de pulos

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_VEL
        if keys[pygame.K_SPACE]:
            self.jump()

        self.vel_y += GRAVITY  # Gravidade
        self.rect.y += self.vel_y

        # Checar colisão com plataformas
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        if collisions:
            for platform in collisions:
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.bottom:  # Apenas corrigir a posição se o jogador estiver caindo e a colisão estiver em cima
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.jump_count = 0  # Resetar contador de pulos ao tocar no chão

        # Prevenir que o jogador saia da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def jump(self):
        if self.jump_count < 2:  # Permitir até dois pulos
            self.vel_y = -PLAYER_JUMP
            self.jump_count += 1
            jump_sound.play()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe da Plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(platform_sprite, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def create_platforms(num_platforms):
    platforms = pygame.sprite.Group()
    for _ in range(num_platforms):
        platform = Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), random.randint(HEIGHT // 2, HEIGHT - PLATFORM_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT)
        platforms.add(platform)
    return platforms

# Classe dos Itens Colecionáveis
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        if item_type == 'star':
            self.image = pygame.transform.scale(star_sprite, (30, 30))
        elif item_type == 'coconut':
            self.image = pygame.transform.scale(coconut_sprite, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def create_items(platforms):
    items = pygame.sprite.Group()
    item_positions = set()  # Manter as posições ocupadas para evitar sobreposição
    item_types = ['star', 'star', 'star', 'coconut', 'coconut']
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
