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

# Classe do Jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
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
        if collisions and self.vel_y > 0:
            self.rect.bottom = collisions[0].rect.top
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

# Classe da Plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Classe dos Itens Colecionáveis
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = pygame.Surface((30, 30))
        if item_type == 'star':
            self.image.fill(YELLOW)
        elif item_type == 'coconut':
            self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

def main():
    clock = pygame.time.Clock()
    run = True

    player = Player()
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    items = pygame.sprite.Group()

    all_sprites.add(player)

    # Criação de plataformas básicas
    for _ in range(NUM_PLATFORMS):
        platform = Platform(random.randint(0, WIDTH - PLATFORM_WIDTH), random.randint(HEIGHT // 2, HEIGHT - PLATFORM_HEIGHT), PLATFORM_WIDTH, PLATFORM_HEIGHT)
        all_sprites.add(platform)
        platforms.add(platform)

    # Criação da plataforma no chão
    ground = Platform(0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT)
    all_sprites.add(ground)
    platforms.add(ground)

    # Criação de itens colecionáveis
    for _ in range(5):
        item = Item(random.randint(0, WIDTH), random.randint(0, HEIGHT - 150), random.choice(['star', 'coconut']))
        all_sprites.add(item)
        items.add(item)

    score = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        all_sprites.update(platforms)

        # Checar colisão com itens
        collected_items = pygame.sprite.spritecollide(player, items, True)
        for item in collected_items:
            if item.item_type == 'star':
                score += 10
            elif item.item_type == 'coconut':
                score += 5

        # Verificar se todos os itens foram coletados
        if not items:
            # Reiniciar fase ou passar para a próxima
            for _ in range(5):
                item = Item(random.randint(0, WIDTH), random.randint(0, HEIGHT - 150), random.choice(['star', 'coconut']))
                all_sprites.add(item)
                items.add(item)

        WIN.fill(WHITE)
        all_sprites.draw(WIN)
        
        # Exibir pontuação
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {score}', True, BLACK)
        WIN.blit(text, (10, 10))
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
