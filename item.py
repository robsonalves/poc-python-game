import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        if item_type == 'star':
            self.image = pygame.transform.scale(pygame.image.load("assets/images/star.png"), (30, 30))
        elif item_type == 'coconut':
            self.image = pygame.transform.scale(pygame.image.load("assets/images/coconut.png"), (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
