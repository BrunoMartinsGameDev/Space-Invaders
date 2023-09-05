import pygame,sys
from Player import Player
import Obstacle
from Alien import Alien
from random import choice
from Laser import Laser
#2 - Nesta classe irá ficar a lógica principal do jogo
class Game:
    def __init__(self) -> None:
        #3 - objeto do jogador com a sua posição na tela
        playerSprite = Player((screenWidth/2,screenHeight),screenWidth,5)
        # 3 - Imagem do player
        self.player = pygame.sprite.GroupSingle(playerSprite)

        # 4 - Variaveis dos obstaculos
        self.shape = Obstacle.shape
        self.blockSize = 6
        self.blocks = pygame.sprite.Group()
        self.obstacleAmount = 4
        self.obstacleXPositions = [num * (screenWidth/self.obstacleAmount) for num in range(self.obstacleAmount )]
        self.xStart = screenWidth/(self.obstacleAmount*self.obstacleAmount)
        self.createMultipleObstacles(*self.obstacleXPositions,xStart=self.xStart,yStart=480)

        # 5 - Variavies dos Aliens
        self.aliens = pygame.sprite.Group()
        self.alienLasers = pygame.sprite.Group()
        self.alienSetup(rows=6, cols= 8)
        self.alienDirection = 1
    
    #Cria o obstaculo individualmente
    def createObstacle(self,xStart,yStart,offsetX):
        for rowIndex, row in enumerate(self.shape):
            for colIndex, col in enumerate(row):
                if col == "x":
                    x = xStart + colIndex * self.blockSize + offsetX
                    y = yStart + rowIndex * self.blockSize
                    block = Obstacle.Block(self.blockSize,(241,79,80),x,y)
                    self.blocks.add(block)
    
    #Faz várias criaçoes de obstaculos
    def createMultipleObstacles(self,*offset,xStart,yStart):
        for offSetX in offset:
            self.createObstacle(xStart,yStart,offSetX)
    
    def alienSetup(self,rows,cols,xOffSet = 70 ,yOffSet = 100, xDistance=60, yDistance=48):
        for rowIndex, row in enumerate(range(rows)):
            for colIndex, col in enumerate(range(cols)) :
                x = colIndex * xDistance + xOffSet
                y = rowIndex * yDistance + yOffSet
                if rowIndex == 0: alienSprite = Alien('yellow',x,y)
                elif 1<= rowIndex <= 2: alienSprite = Alien('green',x,y)
                else:alienSprite = Alien('red',x,y)                
                self.aliens.add(alienSprite)

    def alienPositionChecker(self):
        allAliens = self.aliens.sprites()
        for alien in allAliens:
            if alien.rect.right >= screenWidth:
                self.alienDirection = -1
                self.alienMoveDown(2)
            elif alien.rect.left <= 0:
                self.alienDirection = 1
                self.alienMoveDown(2)
    
    def alienMoveDown(self,distance):
        for alien in self.aliens.sprites():
            alien.rect.y += distance
    
    def alienShoot(self):
        if self.aliens.sprites():
            randomAlien = choice(self.aliens.sprites())
            laserSprite = Laser(randomAlien.rect.center,6,screenHeight)
            self.alienLasers.add(laserSprite)
    #Nesta função iremos atualizar todos as sprites
    #E desenhar todas as sprites
    def run(self):
        #Lógicas
        self.player.update()
        self.aliens.update(self.alienDirection)
        self.alienPositionChecker()
        self.alienShoot()
        self.alienLasers.update()

        #Gráficos
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alienLasers.draw(screen)

#1 - verifica se estamos executando este arquivo
if __name__ == "__main__":
    pygame.init()#inicializa o pygame

    #largura e altura da tela
    screenWidth = 600
    screenHeight = 600
    #criação da tela
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    #Titulo da janela
    pygame.display.set_caption("Space Invaders")

    #Cria um relógio para definirmos o fps
    clock = pygame.time.Clock() 

    #2 - Criando objeto da classe jogo
    game = Game()

    ALIENLASER = pygame.USEREVENT +1
    pygame.time.set_timer(ALIENLASER,800)

    #loop do game
    while True:
        #verifica eventos 
        for event in pygame.event.get():

            #verifica se o evento é de sair
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alienShoot()

        #preenche a tela com uma cor rgb
        screen.fill((30,30,30))
        #2 - Executa a função run do game
        game.run()

        pygame.display.flip()
        clock.tick(60) #60 fps