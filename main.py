from game_manager import Game
import pygame

# run the game
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    game = Game()
    game.run()
