#TestRPGdev/ui/scenes_joke.py
import sys
import pygame
from core.config import get_font, get_large_font, WHITE, GOLD, GRAY
from ui.scenes import Scene


class FakeBlueScreenScene(Scene):
    def __init__(self):
        self.joke_timer = 0
        self.progress = 0

    def handle_input(self, manager, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def update(self, manager, dt):
        self.joke_timer += dt

        if self.progress < 100:
            self.progress = min(100, int((self.joke_timer / 4.0) * 100))

        if self.joke_timer > 5.0:
            manager.game_state = "REVEAL_JOKE"

    def render(self, manager, surface):
        surface.fill((0, 120, 215))

        l_font = get_large_font()
        # Створюємо системні шрифти локально для реалістичного відображення BSOD
        sys_font = pygame.font.SysFont("Segoe UI", 22)
        sys_font_large = pygame.font.SysFont("Segoe UI", 32)

        surface.blit(l_font.render(":(", True, WHITE), (100, 100))

        surface.blit(
            sys_font_large.render("На вашому ПК виникла помилка, і його необхідно перезавантажити.", True, WHITE),
            (100, 200))
        surface.blit(sys_font.render(f"Збирання інформації про помилку ({self.progress}% завершено)", True, WHITE),
                     (100, 280))

        surface.blit(sys_font.render("Stop code: CRITICAL_PROCESS_DIED_BY_DEMON", True, GRAY), (100, 360))
        surface.blit(sys_font.render("[ Натисніть ESC для екстреного виходу ]", True, (180, 210, 245)), (100, 420))


class RevealJokeScene(Scene):
    def __init__(self):
        self.exit_timer = 0

    def handle_input(self, manager, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def update(self, manager, dt):
        self.exit_timer += dt
        if self.exit_timer > 4.0:
            screen = pygame.display.get_surface()
            pygame.display.set_mode((screen.get_width(), screen.get_height()))
            pygame.quit()
            sys.exit()

    def render(self, manager, surface):
        surface.fill((20, 20, 20))

        l_font = get_large_font()
        font = get_font()

        surface.blit(l_font.render("ТА ЦЕ Ж ЖАРТ! :D", True, GOLD), (230, 200))
        surface.blit(font.render("Нічого видалено не було. Твій Windows у безпеці!", True, WHITE), (190, 290))
        surface.blit(font.render("Дякуємо за гру! Закриття програми...", True, GRAY), (270, 350))