import pygame
from settings import WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Defina o tamanho do inimigo
        self.image.fill((255, 0, 0))  # Cor vermelha para o inimigo
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed  # Velocidade do inimigo

    def update(self):
        # Lógica de movimento do inimigo
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed = -self.speed

    def draw(self, win):
        win.blit(self.image, self.rect)
