import sys
import pygame
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, init_fonts
from core.game_manager import GameManager


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RPG Campaign: Професійна Архітектура")

    # Ініціалізація шрифтів після запуску pygame
    init_fonts()

    # Створення головного контролера
    manager = GameManager()
    clock = pygame.time.Clock()

    # Головний ігровий цикл (Engine loop)
    while True:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            manager.handle_input(event)

        manager.update(dt)
        manager.render(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()