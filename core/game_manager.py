import os
import sys
import random
import pygame
from core.config import BACKGROUND_COLOR, PLAYER_COLOR, ENEMY_COLOR, GOLD, WHITE, HP_GREEN, CRIT_COLOR, PURPLE
from entities.character import Character
from ui.combat_log import CombatLog
from ui.scenes import BattleScene, InventoryScene, LootScene, GameOverScene, VictoryScene, FakeBlueScreenScene, RevealJokeScene


def resource_path(relative_path):
    """ Отримує абсолютний шлях до ресурсів, працює для dev та для PyInstaller """
    try:
        # PyInstaller створює тимчасову папку _MEIPASS при виконанні .exe
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class GameManager:
    def __init__(self):
        self.scenes = {
            "BATTLE": BattleScene(),
            "INVENTORY": InventoryScene(),
            "LOOT_SCREEN": LootScene(),
            "GAME_OVER": GameOverScene(),
            "VICTORY": VictoryScene(),
            "FAKE_BSOD": FakeBlueScreenScene(),
            "REVEAL_JOKE": RevealJokeScene()
        }
        self.joke_timer = 0
        self.reset()

    def reset(self):
        self.current_level = 1
        self.game_state = "BATTLE"
        self.enemy_timer = 0
        self.current_selection = 0
        self.inv_selection = 0
        self.menu_options = ["Атакувати", "Випити зілля"]

        # Завантаження спрайтів
        p_sprite = self.load_sprite("assets/player.png", PLAYER_COLOR)

        self.player = Character("Лицар (Гравець)", 120, 16, 5, p_sprite, 150, 200, potions=3)
        self.combat_log = CombatLog(x=300, y=370, width=450, height=150)
        self.inventory = []
        self.loot_found = []

        self.spawn_enemy()

    def load_sprite(self, path, fallback_color):
        # Автоматично адаптуємо шлях під PyInstaller
        adapted_path = resource_path(path)
        try:
            surf = pygame.image.load(adapted_path).convert_alpha()
            return pygame.transform.scale(surf, (100, 100))
        except pygame.error:
            surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            surf.fill(fallback_color)
            pygame.draw.rect(surf, WHITE, surf.get_rect(), 2, 8)
            return surf

    def spawn_enemy(self):
        if self.current_level == 1:
            sprite = self.load_sprite("assets/goblin.png", ENEMY_COLOR)
            self.enemy = Character("Гоблін (Рівень 1)", 80, 14, 3, sprite, 550, 200)
            self.combat_log.add_log("РІВЕНЬ 1: На вас напав Гоблін!", GOLD)
        elif self.current_level == 2:
            sprite = self.load_sprite("assets/orc.png", (180, 100, 50))
            self.enemy = Character("Орк-Воїн (Рівень 2)", 120, 19, 6, sprite, 550, 200)
            self.combat_log.add_log("РІВЕНЬ 2: На вас виходить лютий Орк!", GOLD)
        elif self.current_level == 3:
            sprite = self.load_sprite("assets/demon.png", (100, 20, 20))
            self.enemy = Character("Лорд Демонів (БОС)", 180, 25, 8, sprite, 550, 200)
            self.combat_log.add_log("БОС: Перед вами Лорд Демонів!", PURPLE)

    def execute_player_turn(self):
        if self.current_selection == 0:
            dmg, crit = self.player.attack(self.enemy, direction=1)
            msg = f"Ви нанесли {dmg} шкоди!" if not crit else f"КРИТ! Ви вгатили на {dmg} HP!"
            self.combat_log.add_log(msg, GOLD if crit else WHITE)

            if self.enemy.current_hp <= 0:
                self.game_state = "PLAYER_WINNING_DELAY"
                self.enemy_timer = 0
            else:
                self.game_state = "ENEMY_TURN"
                self.enemy_timer = 0
        elif self.current_selection == 1:
            if self.player.potions > 0:
                healed = self.player.heal()
                self.combat_log.add_log(f"Зілля зцілило на +{healed} HP.", HP_GREEN)
                self.game_state = "ENEMY_TURN"
                self.enemy_timer = 0
            else:
                self.combat_log.add_log("Немає зіллів!", ENEMY_COLOR)

    def equip_item(self):
        chosen = self.inventory[self.inv_selection]
        if chosen["type"] == "weapon":
            self.player.equipped_weapon = chosen
            self.combat_log.add_log(f"Екіпіровано: {chosen['name']}", GOLD)
        elif chosen["type"] == "armor":
            self.player.equipped_armor = chosen
            self.combat_log.add_log(f"Вдягнуто: {chosen['name']}", PLAYER_COLOR)
        self.game_state = "BATTLE"

    def generate_loot(self):
        self.loot_found = []
        if random.randint(1, 100) <= 80:
            self.player.potions += 1
            self.loot_found.append("Зілля здоров'я (+1 шт)")
        if random.randint(1, 100) <= 60:
            bonus_atk = random.randint(3, 7)
            item = {"type": "weapon", "name": f"Меч ручної роботи (+{bonus_atk} АТК)", "value": bonus_atk}
            self.inventory.append(item)
            self.loot_found.append(item["name"])
        if random.randint(1, 100) <= 50:
            bonus_def = random.randint(2, 4)
            item = {"type": "armor", "name": f"Залізний щит (+{bonus_def} ЗХСТ)", "value": bonus_def}
            self.inventory.append(item)
            self.loot_found.append(item["name"])

    def next_level(self):
        self.current_level += 1
        self.spawn_enemy()
        self.game_state = "BATTLE"

    def update(self, dt):
        self.player.update_animations()
        self.enemy.update_animations()

        if self.game_state == "PLAYER_WINNING_DELAY":
            self.enemy_timer += dt
            if self.enemy_timer >= 600:
                self.player.current_hp = self.player.max_hp
                self.combat_log.add_log("Ваше HP відновлено до 100%!", HP_GREEN)
                if self.current_level == 3:
                    self.game_state = "VICTORY"
                    self.joke_timer = 0  # Обнуляємо таймер для безпеки перед фіналом
                else:
                    self.generate_loot()
                    self.game_state = "LOOT_SCREEN"

        if self.game_state == "ENEMY_TURN" and self.player.anim_state == "IDLE":
            self.enemy_timer += dt
            if self.enemy_timer >= 1000:
                dmg, crit = self.enemy.attack(self.player, direction=-1)
                self.combat_log.add_log(f"{self.enemy.name} б'є на {dmg} шкоди.", CRIT_COLOR if crit else WHITE)
                self.game_state = "GAME_OVER" if self.player.current_hp <= 0 else "BATTLE"

        # --- НОВИЙ КОД ДЛЯ ЖАРТУ (ДОДАЄМО СЮДИ) ---

        # 1. Рахуємо час на синьому екрані (2000 мілісекунд = 2 секунди)
        if self.game_state == "FAKE_BSOD":
            self.joke_timer += dt
            if self.joke_timer >= 3000:
                self.game_state = "REVEAL_JOKE"
                self.joke_timer = 0  # Скидаємо для наступного екрану

        # 2. Показуємо екран "ТА ЦЕ Ж ЖАРТ!" і м'яко закриваємо гру
        elif self.game_state == "REVEAL_JOKE":
            self.joke_timer += dt
            if self.joke_timer >= 2500:
                # М'яко повертаємо віконний режим перед тим як закрити програму
                screen = pygame.display.get_surface()
                pygame.display.set_mode((screen.get_width(), screen.get_height()))

                pygame.quit()
                sys.exit()

    def handle_input(self, event):
        # Глобальна кнопка виходу (ESC) тепер працює ТІЛЬКИ якщо це НЕ фінальний розіграш
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.game_state not in ["VICTORY", "FAKE_BSOD", "REVEAL_JOKE"]:
                pygame.quit()
                sys.exit()

        # Якщо стан відноситься до бою, передаємо його бойовій сцені
        if self.game_state in ["BATTLE", "ENEMY_TURN", "PLAYER_WINNING_DELAY"]:
            self.scenes["BATTLE"].handle_input(self, event)
        # Передаємо ввід фінальним сценам (тепер VictoryScene зловить навіть ESC!)
        elif self.game_state in ["VICTORY", "FAKE_BSOD", "REVEAL_JOKE"]:
            self.scenes[self.game_state].handle_input(self, event)
        else:
            self.scenes[self.game_state].handle_input(self, event)

    def render(self, surface):
        surface.fill(BACKGROUND_COLOR)

        # Визначаємо, яку саме сцену малювати
        if self.game_state in ["BATTLE", "ENEMY_TURN", "PLAYER_WINNING_DELAY"]:
            state = "BATTLE"
        elif self.game_state in ["VICTORY", "FAKE_BSOD", "REVEAL_JOKE"]:
            state = self.game_state
        else:
            state = self.game_state

        self.scenes[state].render(self, surface)