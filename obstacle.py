import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_type):
        super().__init__()
        self.obstacle_type = obstacle_type
        if obstacle_type == 'spike':
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))  # Vermelho para obstáculo que termina o jogo
        elif obstacle_type == 'drain':
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 0, 255))  # Azul para obstáculo que drena vida
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        pass
