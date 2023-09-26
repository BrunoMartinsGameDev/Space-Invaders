import pygame,sys
from Player import Player
import Obstacle
from Alien import Alien, Extra
from random import choice,randint
from Laser import Laser
# Nesta classe irá ficar a lógica principal do jogo
class Game:
    def __init__(self) -> None:
        # objeto do jogador com a sua posição na tela
        playerSprite = Player((screenWidth/2,screenHeight),screenWidth,5)
        # Imagem do player
        self.player = pygame.sprite.GroupSingle(playerSprite)

        # Variaveis de vida e ponto
        self.lives = 3
        self.liveSurf = pygame.image.load("Game/sprites/player.png").convert_alpha()
        self.livesXStartPosition = screenWidth - (self.liveSurf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("Game/sprites/Pixeled.ttf",20)

        # Variaveis dos obstaculos
        self.shape = Obstacle.shape
        self.blockSize = 6
        self.blocks = pygame.sprite.Group()
        self.obstacleAmount = 4
        self.obstacleXPositions = [num * (screenWidth/self.obstacleAmount) for num in range(self.obstacleAmount )]
        self.xStart = screenWidth/(self.obstacleAmount*self.obstacleAmount)
        self.createMultipleObstacles(*self.obstacleXPositions,xStart=self.xStart,yStart=480)

        # Variavies dos Aliens
        self.aliens = pygame.sprite.Group()
        self.alienLasers = pygame.sprite.Group()
        self.alienSetup(rows=6, cols= 8)
        self.alienDirection = 1

        # ExtraAlien
        self.extra = pygame.sprite.GroupSingle()
        self.extraSpawnTime = randint(400,800)

        # Audios
        # musica
        # music = pygame.mixer.Sound("Game/sound/music.wav")
        # music.set_volume(0.2)
        # music.play(loops=-1)

        # Sound Effects
        # self.laserSound = pygame.mixer.Sound("Game/sound/laser.wav")
        # self.laserSound.set_volume(0.5)
        # linha 99
        # self.explosionSound = pygame.mixer.Sound("Game/sound/explosion.wav")
        # self.explosionSound.set_volume(0.3)
        # linha 121

    # Cria o obstaculo individualmente
    def createObstacle(self,xStart,yStart,offsetX):
        for rowIndex, row in enumerate(self.shape):
            for colIndex, col in enumerate(row):
                if col == "x":
                    x = xStart + colIndex * self.blockSize + offsetX
                    y = yStart + rowIndex * self.blockSize
                    block = Obstacle.Block(self.blockSize,(241,79,80),x,y)
                    self.blocks.add(block)
    
    # Faz várias criaçoes de obstaculos
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
            laserSprite = Laser(randomAlien.rect.center,screenHeight,6)
            self.alienLasers.add(laserSprite)
            # self.laserSound.play()
    
    def extraAlienTime(self):
        self.extraSpawnTime -= 1
        if self.extraSpawnTime <=0:
            self.extra.add(Extra(choice(['right','left']),screenWidth))
            self.extraSpawnTime = randint(400,800)
    
    def collisionCheck(self):
        #Laser do Player
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #Colisão com obstaculos
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                
                #Colisão com aliens
                aliensHit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliensHit:
                    for alien in aliensHit:
                        self.score += alien.score
                    laser.kill()
                    # self.explosionSound.play()
                    
                #Colisão com extra
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 500
                    laser.kill()

        #laser dos aliens
        if self.alienLasers:
            for laser in self.alienLasers:
                #colisão com obstaculos
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                #colisão com player
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        pygame.quit()
                        sys.exit()
        #aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)
            
                if pygame.sprite.spritecollide(alien, self.player,False):
                    pygame.quit()
                    sys.exit()
    
    def displayLives(self):
        for live in range(self.lives - 1):
            x = self.livesXStartPosition + (live * (self.liveSurf.get_size()[0] + 10))
            screen.blit(self.liveSurf,(x,8))
    
    def displayScore(self):
        scoreSurf = self.font.render(f"Score: {self.score}",False,'white')
        scoreRect = scoreSurf.get_rect(topleft = (10,-10))
        screen.blit(scoreSurf,scoreRect)
    
    def victoryMessage(self):
        if not self.aliens.sprites():
            victorySurf = self.font.render("You Won",False,"white")
            victoryRect = victorySurf.get_rect(center = (screenWidth/2,screenHeight/2))
            screen.blit(victorySurf,victoryRect)
    #Nesta função iremos atualizar todos as sprites
    #E desenhar todas as sprites
    def run(self):
        #Player
        # self.player.update()
        # self.player.sprite.lasers.draw(screen)
        # self.player.draw(screen)

        #Aliens
        # self.aliens.update(self.alienDirection)
        # self.aliens.draw(screen)
        # self.alienPositionChecker()

        #alien lasers
        # self.alienLasers.update()
        # self.alienLasers.draw(screen)

        #alienExtra
        # self.extraAlienTime()
        # self.extra.update()
        # self.extra.draw(screen)

        #Checa colisões
        # self.collisionCheck()

        #Gráficos
        # self.blocks.draw(screen)
        # self.displayLives()
        # self.displayScore()
        # self.victoryMessage()
        ...

class CRT:
    def __init__(self) -> None:
        self.tv = pygame.image.load("Game/sprites/tv.png").convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(screenWidth,screenHeight))
    
    def createCrtLine(self):
        lineHeight = 3
        lineAmount = int(screenHeight/lineHeight)
        for line in range(lineAmount):
            yPos = line * lineHeight
            pygame.draw.line(self.tv,"black",(0,yPos),(screenWidth,yPos),1)

    def draw(self):
        self.tv.set_alpha(randint(50,90))
        self.createCrtLine()
        screen.blit(self.tv,(0,0))
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
    crt = CRT()

    #criando evento do laser do alien
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
                ...
        #preenche a tela com uma cor rgb
        screen.fill((30,30,30))
        #Executa a função run do game
        game.run()

        #desenha efeito de tv antiga
        #crt.draw()

        pygame.display.flip()
        clock.tick(60) #60 fps