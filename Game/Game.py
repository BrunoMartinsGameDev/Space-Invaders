import pygame,sys
from Player import Player
import Obstacle

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
    
    #Nesta função iremos atualizar todos as sprites
    #E desenhar todas as sprites
    def run(self):
        #Lógicas
        self.player.update()
        
        #Gráficos
        self.player.sprite.lasers.draw(screen )
        self.player.draw(screen)
        self.blocks.draw(screen)

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

    #loop do game
    while True:
        #verifica eventos 
        for event in pygame.event.get():

            #verifica se o evento é de sair
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #preenche a tela com uma cor rgb
        screen.fill((30,30,30))
        #2 - Executa a função run do game
        game.run()

        pygame.display.flip()
        clock.tick(60) #60 fps