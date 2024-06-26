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
            jump_sound.play()

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
    for _ in range(5):
        item = create_item_near_platform(platforms)
        items.add(item)
    return items

def create_item_near_platform(platforms):
    platform = random.choice(platforms.sprites())
    x = random.randint(platform.rect.left, platform.rect.right)
    y = platform.rect.top - 30  # Posicionar o item logo acima da plataforma
    item_type = random.choice(['star', 'coconut'])
    return Item(x, y, item_type)

def main():
    clock = pygame.time.Clock()
    run = True

    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    platforms = create_platforms(NUM_PLATFORMS)
    all_sprites.add(platforms)

    ground = Platform(0, HEIGHT - PLATFORM_HEIGHT, WIDTH, PLATFORM_HEIGHT)
    platforms.add(ground)
    all_sprites.add(ground)

    items = create_items(platforms)
    all_sprites.add(items)

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
                collect_star_sound.play()
            elif item.item_type == 'coconut':
                score += 5
                collect_coconut_sound.play()

        # Verificar se todos os itens foram coletados
        if not items:
            # Reiniciar plataformas e itens
            for platform in platforms:
                if platform != ground:
                    platform.kill()
            platforms = create_platforms(NUM_PLATFORMS)
            all_sprites.add(platforms)

            items = create_items(platforms)
            all_sprites.add(items)

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
