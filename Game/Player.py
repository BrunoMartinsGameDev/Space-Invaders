import pygame
from Laser import Laser
# 3 - Classe do jogador
class Player(pygame.sprite.Sprite):
    #Construtor da classe player com o parametro de posição
    def __init__(self,pos,constraint,speed) -> None:
        super().__init__()
        self.image = pygame.image.load("Game\sprites\player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.limiteXMaximo = constraint
        
        #Variaveis para o laser
        self.podeAtirar = True
        self.laserTimer = 0
        self.laserTempoDeRecarga = 600

        self.lasers = pygame.sprite.Group()
    
    #Função para pegar comando do jogador
    def getInput(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.podeAtirar:
            self.shootLaser()
            self.podeAtirar = False
            self.laserTimer = pygame.time.get_ticks()
    
    #Função para limitar o jogador na tela
    def constraint(self):
        if self.rect.left <=0:
            self.rect.left = 0
        if self.rect.right >= self.limiteXMaximo:
            self.rect.right = self.limiteXMaximo

    #Função para atirar o laser
    def shootLaser(self):
        self.lasers.add(Laser(self.rect.center,self.rect.bottom,-8))

    #Função que recarrega o laser
    def reload(self):
        if not self.podeAtirar:
            tempoAtual = pygame.time.get_ticks()
            if tempoAtual - self.laserTimer >= self.laserTempoDeRecarga:
                self.podeAtirar = True

    #Função que rodará a todo momento no loop principal
    def update(self):
        self.getInput()
        self.constraint()
        self.reload()
        self.lasers.update()