import pygame
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL, PLAYER_JUMP, GRAVITY, WIDTH, HEIGHT
from settings import jump_sound

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/images/player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
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
