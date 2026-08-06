import os
import sys
import pygame

RUTA_RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(RUTA_RAIZ, "src"))

from src.game import AvatarGame

if not pygame.get_init():
    pygame.init()
    
game = AvatarGame(title="Memory Avatar Challenge")

if __name__ == "__main__":
    game.run_independently()