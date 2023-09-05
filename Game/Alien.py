import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,type,x,y) -> None:
        super().__init__()
        filePath = "Game/sprites/" + type + ".png"
        self.image = pygame.image.load(filePath).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update(self,direction):
        self.rect.x += direction