import unittest
import pygame
from game import setup_game, Player, Platform, Item, WIDTH, HEIGHT, PLAYER_VEL

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player, self.all_sprites, self.platforms, self.items, self.score = setup_game()

    def tearDown(self):
        pygame.quit()

    def test_player_initial_position(self):
        self.assertEqual(self.player.rect.center, (WIDTH // 2, HEIGHT // 2))

    def test_platforms_creation(self):
        self.assertEqual(len(self.platforms), 11)  # 10 plataformas + 1 chão

    def test_items_creation(self):
        self.assertEqual(len(self.items), 5)

    def test_player_movement(self):
        initial_x = self.player.rect.x
        self.player.rect.x += PLAYER_VEL
        self.player.update(self.platforms)
        self.assertEqual(self.player.rect.x, initial_x + PLAYER_VEL)

    def test_collect_items(self):
        initial_score = self.score
        collected_items_count = 0
        for item in list(self.items):  # Usar uma lista para evitar modificação durante a iteração
            self.player.rect.topleft = item.rect.topleft  # Simular coleta do item
            self.all_sprites.update(self.platforms)  # Atualizar todas as sprites
            collected_items = pygame.sprite.spritecollide(self.player, self.items, True)
            for collected_item in collected_items:
                collected_items_count += 1
                if collected_item.item_type == 'star':
                    self.score += 10
                    print("Collected a star, +10 points")
                elif collected_item.item_type == 'coconut':
                    self.score += 5
                    print("Collected a coconut, +5 points")
        print(f"Collected {collected_items_count} items, final score: {self.score}")
        self.assertEqual(collected_items_count, 5)  # Verificar se todos os 5 itens foram coletados
        self.assertEqual(self.score, initial_score + 40)

    def test_collect_all_items_by_moving_player(self):
        initial_score = self.score
        collected_items_count = 0
        for item in self.items:
            self.player.rect.topleft = item.rect.topleft  # Mover o jogador para o item
            self.all_sprites.update(self.platforms)  # Atualizar todas as sprites
            collected_items = pygame.sprite.spritecollide(self.player, self.items, True)
            for collected_item in collected_items:
                collected_items_count += 1
                if collected_item.item_type == 'star':
                    self.score += 10
                    print(f"Collected a star at ({collected_item.rect.x}, {collected_item.rect.y}), +10 points")
                elif collected_item.item_type == 'coconut':
                    self.score += 5
                    print(f"Collected a coconut at ({collected_item.rect.x}, {collected_item.rect.y}), +5 points")
        print(f"Collected {collected_items_count} items, final score: {self.score}")
        self.assertEqual(collected_items_count, 5)  # Verificar se todos os 5 itens foram coletados
        self.assertEqual(self.score, initial_score + 40)

    def test_reset_game(self):
        self.player, self.all_sprites, self.platforms, self.items, self.score = setup_game()
        self.assertEqual(self.score, 0)
        self.assertEqual(len(self.platforms), 11)  # 10 plataformas + 1 chão
        self.assertEqual(len(self.items), 5)

if __name__ == "__main__":
    unittest.main()
