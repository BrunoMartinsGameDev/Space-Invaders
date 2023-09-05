import pygame,sys
from Player import Player

#2 - Nesta classe irá ficar a lógica principal do jogo
class Game:
    def __init__(self) -> None:
        #3 - objeto do jogador com a sua posição na tela
        playerSprite = Player((screenWidth/2,screenHeight),screenWidth,5)
        # 3 - Imagem do player
        self.player = pygame.sprite.GroupSingle(playerSprite)
    
    #Nesta função iremos atualizar todos as sprites
    #E desenhar todas as sprites
    def run(self):
        #Lógicas
        self.player.update()
        #Gráficos
        self.player.sprite.lasers.draw(screen )
        self.player.draw(screen)

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