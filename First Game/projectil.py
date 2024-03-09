import pygame
pygame.init()

# Définition des constantes pour les couleurs
black = (0, 0, 0)
white = (255, 255, 255)
white_red = (253, 181, 181)


class Projectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25))  # géométrie de l'enemy
        self.image.fill(white_red)  # couleur de l'enemy
        self.rect = self.image.get_rect()  # rect prend les donné de image
        self.position = [x, y]
        self.rect.x = self.position[0]  # coordonné x à l'origine
        self.rect.y = self.position[1]  # coordonné y à l'origine
        self.speed = 1  # vitesse de l'enemy

    def update(self, walle):
        self.walls = walle
        for walls in self.walls:
            self.wall = walls
            if self.rect.colliderect(walls) == False:
                self.rect.x -= self.speed
            else:
                Projectil.kill(self)
