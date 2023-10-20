import pygame


class Button:
    def __init__(self, rect, color, text, font_path=None, font_size=36, border_radius=10, hover_color=(0, 0, 0)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.border_radius = border_radius

        # initialize font
        self.font = pygame.font.Font(font_path, font_size)
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # initialize color
        self.original_color = color
        self.hover_color = hover_color

    def draw(self, screen):
        # check if the mouse position is over the button then change color accordingly
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.original_color

        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        screen.blit(self.text_surf, self.text_rect)


class Title:
    def __init__(self, position, text, font_path, font_size, color=(255, 255, 255)):
        self.position = position
        self.text = text

        # initialize font and render the title text
        self.font = pygame.font.Font(font_path, font_size)
        self.text_surf = self.font.render(self.text, True, color)
        self.text_rect = self.text_surf.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.text_surf, self.text_rect)
