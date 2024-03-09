from player import Player
from enemy import Enemy
from projectil import Projectil

import pytmx
import pyscroll
import pygame
pygame.init()

# Définition des constantes pour les couleurs
black = (0, 0, 0)
white = (255, 255, 255)
white_grey = (250, 250, 250)


class Game:

    def __init__(self):
        # Définition de la taille de la fenêtre du jeu
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Lost in the Darkness")
        # importer la carte tmx
        self.tmx_data = pytmx.util_pygame.load_pygame("white_cube_tileset.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, self.screen.get_size())
        self.map_layer.zoom = 1.5

        # importer le background
        self.background_image = pygame.image.load("CUTE/camp.png")

        # générer le joueur
        player_position = self.tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)
        # générer l'enemy
        enemy_position = self.tmx_data.get_object_by_name("enemy")
        self.enemy = Enemy(enemy_position.x, enemy_position.y)

        # générer les projectils
        projectil_position = self.tmx_data.get_object_by_name("projectil")
        self.projectile = Projectil(projectil_position.x, projectil_position.y)

        # Les collisions
        self.walls = []

        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height))
        # Les collisions avec les platforme à 1 direction
        self.platforme = []

        for obj in self.tmx_data.objects:
            if obj.type == "onedirection_collision":
                self.platforme.append(pygame.Rect(
                    obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        self.player_group = pyscroll.PyscrollGroup(
            map_layer=self.map_layer, default_layer=5)
        self.enemy_group = pyscroll.PyscrollGroup(
            map_layer=self.map_layer, default_layer=5)
        self.player_group.add(self.player)
        self.enemy_group.add(self.enemy)
        self.enemy_group.add(self.projectile)

        self.count = 0

    def projectil(self):
        self.count += 1
        if self.count == 120:
            # générer les projectils
            projectil_position = self.tmx_data.get_object_by_name("projectil")
            self.projectile = Projectil(
                projectil_position.x, projectil_position.y)
            self.enemy_group.add(self.projectile)
            self.count = 0

    def update(self):
        self.player_group.update(
            self.walls, self.platforme, self.enemy, self.projectile)
        self.enemy_group.update(self.walls)
        self.projectil()

    def run(self):
        # Boucle principale du jeu
        running = True
        clock = pygame.time.Clock()
        while running:

            self.update()
            self.player_group.center(self.player.rect.center)
            self.all_groupe = pyscroll.PyscrollGroup(
                map_layer=self.map_layer, default_layer=5)

            self.screen.blit(self.background_image, (0, 0))
            self.all_groupe.add(self.enemy_group)
            self.all_groupe.add(self.player_group)
            self.all_groupe.draw(self.screen)
            pygame.display.flip()
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            # Limite le nombre de FPS
            clock.tick(60)
        # Fermeture de Pygame
        pygame.quit()
