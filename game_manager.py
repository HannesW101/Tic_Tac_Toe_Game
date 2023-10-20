import pygame
from game_states import MenuState, PlayState


class Game:
    def __init__(self):
        # window settings
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Tic Tac Toe")
        icon = pygame.image.load('Assets/Icons/tictactoe_icon.png')
        pygame.display.set_icon(icon)
        self.current_state = MenuState()

    # main game loop
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                result = self.current_state.handle_event(event)
                if result == "PLAY":
                    self.current_state = PlayState()

            self.current_state.update()
            self.current_state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
