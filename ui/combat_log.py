import pygame
from core.config import get_font, TEXT_BG, WHITE

class CombatLog:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.logs = []
        self.max_lines = 6
        self.line_height = 20

    def add_log(self, text, color=WHITE):
        self.logs.append((text, color))
        if len(self.logs) > self.max_lines:
            self.logs.pop(0)

    def draw(self, surface):
        pygame.draw.rect(surface, TEXT_BG, self.rect, 0, 5)
        pygame.draw.rect(surface, WHITE, self.rect, 1, 5)
        font = get_font()
        for idx, (text, color) in enumerate(self.logs):
            txt_surf = font.render(text, True, color)
            surface.blit(txt_surf, (self.rect.x + 15, self.rect.y + 12 + (idx * self.line_height)))