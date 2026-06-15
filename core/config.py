import pygame

# Налаштування екрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Кольори (RGB)
BACKGROUND_COLOR = (25, 25, 35)
PLAYER_COLOR = (50, 150, 255)
ENEMY_COLOR = (220, 60, 60)
HP_GREEN = (45, 180, 45)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
DARK_GRAY = (50, 50, 60)
MENU_BG = (35, 35, 45)
TEXT_BG = (15, 15, 20)
GOLD = (255, 215, 0)
PURPLE = (160, 32, 240)
CRIT_COLOR = (255, 140, 0)

# Шрифти (Ініціалізуються після pygame.init())
_font = None
_large_font = None

def init_fonts():
    global _font, _large_font
    _font = pygame.font.SysFont("Arial", 18)
    _large_font = pygame.font.SysFont("Arial", 40)

def get_font(): return _font
def get_large_font(): return _large_font