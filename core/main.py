import pygame
from .constants import *
from .game import Game

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mini Metro Clone - Pygame")
    
    game = Game(screen)
    game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()