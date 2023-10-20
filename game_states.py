import pygame
import GUI


class GameState:
    def __init__(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.btn_play = GUI.Button((150, 275, 200, 70), (65, 145, 151), "Play",
                                   'Assets/Fonts/Action_Man.ttf', hover_color=(120, 214, 198))
        self.game_title = GUI.Title((250, 110), "Tic Tac Toe", "Assets/Fonts/Action_Man.ttf",
                                    75)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.btn_play.rect.collidepoint(event.pos):
                return "PLAY"

    def draw(self, screen):
        screen.fill((18, 72, 107))
        self.btn_play.draw(screen)
        self.game_title.draw(screen)


class PlayState(GameState):
    def __init__(self):
        super().__init__()
        # dimensions for the Tic Tac Toe grid
        self.grid_size = 480
        self.cell_size = self.grid_size / 3
        self.grid_pos = (10, 10)  # top-left position of the grid
        self.board = [[0, 0, 0] for _ in range(3)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.restart_button = GUI.Button((200, 300, 100, 50), (65, 145, 151), "Restart",
                                         hover_color=(120, 214, 198))
        self.animations = []

    def check_win(self):
        # check rows, columns, diagonals
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)) or \
                    all(self.board[j][i] == self.current_player for j in range(3)):
                return True

        if all(self.board[i][i] == self.current_player for i in range(3)) or \
                all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True

        return False

    def place_marker(self, x, y):
        # placing the X or O and animation for them
        if self.board[y][x] != 0 or self.game_over:
            return

        self.board[y][x] = self.current_player

        if self.board[y][x] == 1:
            self.animations.append(XAnimation(x, y, self.cell_size))
        elif self.board[y][x] == 2:
            self.animations.append(OAnimation(x, y, self.cell_size))

        # check if current player has won or if the board is full (tie)
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
        elif all(cell != 0 for row in self.board for cell in row):
            self.game_over = True
            self.winner = 0
        else:
            self.current_player = 3 - self.current_player  # Switch players

    def update(self):
        new_animations = []
        for anim in self.animations:
            done = anim.update()
            if not done:
                new_animations.append(anim)
        self.animations = new_animations

    def draw_grid(self, screen):
        # draw vertical lines
        for x in range(1, 3):
            pygame.draw.line(screen, (255, 255, 255),
                             (self.grid_pos[0] + x * self.cell_size, self.grid_pos[1]),
                             (self.grid_pos[0] + x * self.cell_size, self.grid_pos[1] + self.grid_size),
                             5)
        # draw horizontal lines
        for y in range(1, 3):
            pygame.draw.line(screen, (255, 255, 255),
                             (self.grid_pos[0], self.grid_pos[1] + y * self.cell_size),
                             (self.grid_pos[0] + self.grid_size, self.grid_pos[1] + y * self.cell_size),
                             5)

    def draw_X(self, x, y, screen):
        # assuming cell_size is the width of a cell
        margin = self.cell_size * 0.2  # margin from cell border
        start_x = x * self.cell_size + margin
        start_y = y * self.cell_size + margin
        end_x = (x + 1) * self.cell_size - margin
        end_y = (y + 1) * self.cell_size - margin
        pygame.draw.line(screen, (120, 214, 198), (start_x, start_y), (end_x, end_y), 5)
        pygame.draw.line(screen, (120, 214, 198), (end_x, start_y), (start_x, end_y), 5)

    def draw_O(self, x, y, screen):
        center_x = (x + 0.5) * self.cell_size
        center_y = (y + 0.5) * self.cell_size
        pygame.draw.circle(screen, (245, 252, 205), (int(center_x), int(center_y)),
                           int(self.cell_size * 0.3), 5)

    def draw(self, screen):
        screen.fill((18, 72, 107))
        self.draw_grid(screen)

        # first get all cells that are currently animated
        animated_cells = [(anim.x, anim.y) for anim in self.animations]

        for y in range(3):
            for x in range(3):
                if (x, y) not in animated_cells:  # only draw static symbols for non-animated cells
                    if self.board[y][x] == 1:
                        self.draw_X(x, y, screen)
                    elif self.board[y][x] == 2:
                        self.draw_O(x, y, screen)

        if self.game_over:
            font = pygame.font.Font("Assets/Fonts/Action_Man.ttf", 50)
            if self.winner == 0:
                text = "It's a Tie!"
            elif self.winner == 1:
                text = f"Player X Won!"
            else:
                text = f"Player O Won!"
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(250, 170))

            # drawing a background rectangle for the text with rounded corners
            padding = 10  # space around the text
            bg_rect = pygame.Rect(text_rect.left - padding,
                                  text_rect.top - padding,
                                  text_rect.width + 2 * padding,
                                  text_rect.height + 2 * padding)
            pygame.draw.rect(screen, (65, 145, 151), bg_rect, border_radius=15)  # the color of the block

            screen.blit(text_surf, text_rect)
            self.restart_button.draw(screen)

        for anim in self.animations:
            anim.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = (event.pos[0] - self.grid_pos[0]) // self.cell_size, (
                        event.pos[1] - self.grid_pos[1]) // self.cell_size
            if 0 <= x < 3 and 0 <= y < 3:
                self.place_marker(int(x), int(y))
            if self.game_over and self.restart_button.rect.collidepoint(event.pos):
                # reset game state for another round
                self.__init__()


class XAnimation:
    def __init__(self, x, y, cell_size):
        self.x, self.y, self.cell_size = x, y, cell_size
        self.progress = 0  # 0 to 1

    def update(self):
        self.progress += 0.001  # control the speed of the animation (lower = slower)
        if self.progress >= 1:
            return True  # animation completed
        return False

    def draw(self, screen):
        margin = self.cell_size * 0.2
        start_x = self.x * self.cell_size + margin
        start_y = self.y * self.cell_size + margin
        end_x = (self.x + 1) * self.cell_size - margin
        end_y = (self.y + 1) * self.cell_size - margin

        # adjust the endpoints based on progress for first line of X
        current_end_x1 = start_x + (end_x - start_x) * self.progress
        current_end_y1 = start_y + (end_y - start_y) * self.progress
        pygame.draw.line(screen, (120, 214, 198), (start_x, start_y), (current_end_x1,
                                                                       current_end_y1), 5)

        # adjust the endpoints based on progress for second line of X
        current_end_x2 = end_x - (end_x - start_x) * self.progress
        current_end_y2 = start_y + (end_y - start_y) * self.progress
        pygame.draw.line(screen, (120, 214, 198), (end_x, start_y), (current_end_x2,
                                                                     current_end_y2), 5)


class OAnimation:
    def __init__(self, x, y, cell_size):
        self.x, self.y, self.cell_size = x, y, cell_size
        self.progress = 0  # 0 to 1

    def update(self):
        self.progress += 0.001  # control the speed of the animation (lower = slower)
        if self.progress >= 1:
            return True  # animation completed
        return False

    def draw(self, screen):
        max_radius = self.cell_size * 0.3
        current_radius = max_radius * self.progress
        pygame.draw.circle(screen, (245, 252, 205),
                           (int((self.x + 0.5) * self.cell_size), int((self.y + 0.5) * self.cell_size)),
                           int(current_radius),
                           5)
