from typing import Any
import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,screenHeight,speed = -8) -> None:
        super().__init__()
        self.image = pygame.Surface((4,20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.heightLimite = screenHeight


    def destroy(self):
        if self.rect.y < -50 or self.rect.y >=self.heightLimite+50:
            self.kill()
    def update(self) -> None:
        self.rect.y += self.speed
        self.destroy()