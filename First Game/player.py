from enemy import Enemy
import pygame
import pytmx
pygame.init()

# Définition des constantes pour les couleurs
black = (0, 0, 0)
white = (255, 255, 255)
white_grey = (250, 250, 250)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = ""#pygame.image.load("knight sprite/Knight_H.png")
        self.image = self.get_image(0, 0, 16, 17)
        self.hitbox = pygame.Surface([11, 19])
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.hitbox.get_rect()
        self.position = [x, y]
        self.rect.x = self.position[0]  # coordonné x à l'origine
        self.rect.y = self.position[1]  # coordonné y à l'origine
        self.velocity_y = 0  # initialisation de la velocité
        self.speed = 3  # vitesse du joueur
        # vérifi si le joueur touche le sol (pour sauter)
        self.on_ground = True
        self.on_ground_double_jump = True  # pour que le joueur fasse un double-saut
        self.jump_count = 0
        self.first_clock = 0
        self.second_clock = 0

        self.idle = []
        for i in range(6):
            self.idle.append(self.get_image(i * 32 + (i+1) * 16, 15, 16, 17))
        self.right = []
        for i in range(6):
            self.right.append(self.get_image(i * 32 + (i+1) * 16, 109, 16, 19))
        self.attack = []
        for i in range(6):
            self.attack.append(self.get_image(
                i * 32 + (i+1) * 16, 255, 16, 19))

        self.images = {
            "right": self.right[0],
            "left": pygame.transform.flip(self.right[0], True, False),
            "idle": self.idle[0],
            "attack": self.attack[0]
        }

    def update(self, walle, platforme, enemy, projectile):
        # Gestion des mouvements du joueur
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.frame("left")
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.frame("right")
        else:
            self.frame("idle")

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.button)
                if event.button == 1:
                    self.frame("attack")
                elif event.button == 3:
                    self.frame("attack")

        # Gestion des sauts et des doubles sauts du joueur
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.on_ground = False
                self.velocity_y = -7
                # La touche de saut a été enfoncée, on peut donc faire un double saut
                self.jump_released = False
            elif self.jump_released and self.on_ground_double_jump:
                self.velocity_y = -7
                self.on_ground_double_jump = False
                # La touche de saut a été utilisée, on ne peut plus sauter de nouveau
                self.jump_released = True
        else:
            # La touche de saut a été relâchée, on peut de nouveau faire un double saut
            self.jump_released = True

        # Gestion de la gravité sur le joueur
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # empêche le joueur de sortir du cadre
        if self.rect.left < 0:
            self.rect.left = 0
        # si le joueur tombe dans le vide, il recommence du début
        if self.rect.top > 925:
            self.game_over()

        # Vérification des collisions
        self.walls = walle
        for walls in self.walls:
            self.wall = walls
            if self.rect.colliderect(walls):
                # si le joueur est en dessous de la platform, le saut s'arrête
                if self.rect.top >= self.wall.bottom - 10:
                    if self.velocity_y < 0:
                        self.rect.top = self.wall.bottom - 1
                        self.velocity_y = 1

                # stop le joueur si il touche le mur gauche
                elif self.rect.right >= self.wall.left and self.rect.bottom >= self.wall.top and self.rect.right <= self.wall.left + 5:
                    self.rect.right = self.wall.left

                # stop le joueur si il touche le mur droit
                elif self.rect.left <= self.wall.right and self.rect.bottom >= self.wall.top and self.rect.left >= self.wall.right - 5:
                    self.rect.left = self.wall.right

                # si le joueur est sur la platform2, faire comme si il était sur le sol
                elif self.rect.bottom >= self.wall.top:
                    self.rect.bottom = self.wall.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.on_ground_double_jump = True

        # vérification des collisions pour les petites platformes en bois
        self.platforme = platforme
        for plat in self.platforme:
            self.plat = plat
            if self.rect.colliderect(plat):
                # stop le joueur si il touche le mur gauche
                if self.rect.right >= self.plat.left and self.rect.bottom >= self.plat.top and self.rect.right <= self.plat.left + 5:
                    self.rect.right = self.plat.left

                # stop le joueur si il touche le mur droit
                elif self.rect.left <= self.plat.right and self.rect.bottom >= self.plat.top and self.rect.left >= self.plat.right - 5:
                    self.rect.left = self.plat.right
                # si le joueur est sur la platform2, faire comme si il était sur le sol
                elif self.rect.bottom >= self.plat.top:
                    self.rect.bottom = self.plat.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.on_ground_double_jump = True

        # regarde si un enemy touche le joueur et si oui, appele la fonction game over
        if self.rect.colliderect(enemy):
            self.game_over()
        if self.rect.colliderect(projectile):
            self.game_over()

    # variable qui fait retevenir le joueur au début du niveau si il meurt
    def game_over(self):
        tmx_data = pytmx.util_pygame.load_pygame("white_cube_tileset.tmx")
        player_position = tmx_data.get_object_by_name("player")
        self.rect.x = player_position.x
        self.rect.y = player_position.y
        self.velocity_y = 0.5
        self.on_ground = False

    # créer les sprites à partir du ficher de sprite
    def get_image(self, x, y, x_sprite, y_sprite):
        self.hitbox = pygame.Surface([11, 19])
        image = pygame.Surface([16, 19])
        image.blit(self.sprite_sheet, (0, 0), (x + 3, y, x_sprite, y_sprite))
        return image

    def frame(self, type):

        if type == "attack":
            self.attack_frame = 0
            first_clock = 0
            second_clock = 0
            # Vérifie si l'animation d'attaque est en cours et incrémente la frame
            while second_clock < len(self.attack):
                first_clock += 1
                if first_clock % 10 == 9:
                    second_clock += 1
                self.images["attack"] = self.attack[second_clock - 1]

        elif type == "right":
            self.right_frame = 0
            while self.right_frame < len(self.right):
                self.images["right"] = self.right[self.right_frame]
                self.right_frame += 1
            self.right_frame = 0

        elif type == "idle":
            self.idle_frame = 0
            while self.idle_frame < len(self.idle):
                self.images["idle"] = self.idle[self.idle_frame]
                self.idle_frame += 1
            self.idle_frame = 0

            '''
            # Animation autre que d'attaque, remet la variable attack_frame à None
            self.attack_frame = 0
            self.first_clock += 1
            if self.first_clock % 10 == 9:
                self.second_clock += 1
            frame = self.second_clock % 6

            if type == "right":
                self.images["right"] = self.right[frame]
            elif type == "left":
                self.images["left"] = pygame.transform.flip(
                    self.right[frame], True, False)
            elif type == "idle":
                self.images["idle"] = self.idle[frame]
            '''
            # met à jour les bonnes frames du sprite à afficher et supprime le background du sprite
        self.image = self.images[type]
        self.image.set_colorkey([0, 255, 255])
