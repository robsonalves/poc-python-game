import pygame
from settings import platform_sprite

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(platform_sprite, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
