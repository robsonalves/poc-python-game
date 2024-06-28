import pygame

# Inicialização do Pygame e do mixer
pygame.init()
pygame.mixer.init()

# Configurações de tela
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Platformer Adventure")

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
PLAYER_LIFE = 3  # Vida do jogador

# Configurações das Plataformas
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 20
NUM_PLATFORMS = 10  # Número de plataformas aumentadas

# Carregar sprites
platform_sprite = pygame.image.load("assets/images/platform.png")

# Carregar sons
jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
collect_star_sound = pygame.mixer.Sound("assets/sounds/coin.wav")
collect_coconut_sound = pygame.mixer.Sound("assets/sounds/pickup.wav")
enemy_hit_sound = pygame.mixer.Sound("assets/sounds/enemy_hit.wav")
obstacle_hit_sound = pygame.mixer.Sound("assets/sounds/obstacle_hit.wav")  # Novo som para colisão com obstáculos
