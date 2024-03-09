import pygame
pygame.init()

# Définition des constantes pour les couleurs
black = (0, 0, 0)
white = (255, 255, 255)
white_red = (253, 181, 181)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # géométrie de l'enemy
        self.image.fill(white_red)  # couleur de l'enemy
        self.rect = self.image.get_rect()  # rect prend les donné de image
        self.position = [x, y]
        self.rect.x = self.position[0]  # coordonné x à l'origine
        self.rect.y = self.position[1]  # coordonné y à l'origine
        self.velocity_y = 0  # initialisation de la velocité
        self.speed = 3  # vitesse de l'enemy
        self.direction = 1  # 1 = droite -1 = gauche
        # vérifi si l'enemy touche le sol (pour sauter)
        self.on_ground = True

    def update(self, walle):

        # Gestion de la gravité sur l'enemy
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Gestion des mouvements sur l'enemy
        self.rect.x += self.speed * self.direction

        # Vérification des collisions
        self.walls = walle
        for walls in self.walls:
            self.wall = walls
            if self.rect.colliderect(walls):
                # si le joueur est en dessous de la platform, le saut s'arrête
                if self.rect.top >= self.wall.bottom - 10:
                    self.velocity_y = 0.5

                # stop le joueur si il touche le mur gauche
                elif self.rect.right >= self.wall.left and self.rect.bottom >= self.wall.top and self.rect.right <= self.wall.left + 5:
                    self.rect.right = self.wall.left
                    self.direction *= -1

                # stop le joueur si il touche le mur droit
                elif self.rect.left <= self.wall.right and self.rect.bottom >= self.wall.top and self.rect.left >= self.wall.right - 5:
                    self.rect.left = self.wall.right
                    self.direction *= -1

                # si le joueur est sur la platform2, faire comme si il était sur le sol
                elif self.rect.bottom >= self.wall.top:
                    self.rect.bottom = self.wall.top
                    self.velocity_y = 0
                    self.on_ground = True
