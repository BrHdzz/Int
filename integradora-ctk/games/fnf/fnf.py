import pygame
from games.fnf.config_fnf import WIDTH, HEIGHT, FPS, COLOR_BG
from games.fnf import fnf_game

def start(app, xd, id):
    try:
        if not pygame.init():
            pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("FNF Buenestar")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(COLOR_BG)
            pygame.display.flip()
            clock.tick(FPS)

            fnf_game.iniciar_juego()
        
        pygame.quit()
    except:
        pass