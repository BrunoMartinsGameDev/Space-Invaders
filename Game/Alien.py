import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,type,x,y) -> None:
        super().__init__()
        filePath = "Game/sprites/" + type + ".png"
        self.image = pygame.image.load(filePath).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if type == 'red':
            self.score = 100
        elif type == 'green':
            self.score = 200
        elif type == 'yellow':
            self.score = 300
                
    
    def update(self,direction):
        self.rect.x += direction
class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screenWidth) -> None:
        super().__init__()
        self.image = pygame.image.load("Game/sprites/extra.png").convert_alpha()
        if side == "right":
            x = screenWidth + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        self.rect = self.image.get_rect(topleft = (x,80))
    def update(self):
        self.rect.x += self.speed