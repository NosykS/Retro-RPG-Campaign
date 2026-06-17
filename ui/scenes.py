#TestRPGdev/ui/scenes.py
import sys
import pygame
from core.config import get_font, get_large_font, MENU_BG, WHITE, GOLD, GRAY, DARK_GRAY, HP_GREEN, ENEMY_COLOR


class Scene:
    """ Базовий абстрактний клас сцени """
    def handle_input(self, manager, event): pass
    def update(self, manager, dt): pass
    def render(self, manager, surface): pass


class BattleScene(Scene):
    def handle_input(self, manager, event):
        if event.type == pygame.KEYDOWN:
            if manager.game_state != "BATTLE":
                return

            if event.key == pygame.K_i and manager.player.anim_state == "IDLE":
                manager.game_state = "INVENTORY"
                return

            if manager.player.anim_state == "IDLE" and manager.enemy.anim_state == "IDLE":
                if event.key == pygame.K_UP:
                    manager.current_selection = 0
                elif event.key == pygame.K_DOWN:
                    manager.current_selection = 1
                elif event.key == pygame.K_RETURN:
                    manager.execute_player_turn()

    def render(self, manager, surface):
        manager.player.draw(surface)
        manager.enemy.draw(surface)
        manager.combat_log.draw(surface)

        menu_box = pygame.Rect(50, 370, 230, 150)
        pygame.draw.rect(surface, MENU_BG, menu_box, 0, 5)
        pygame.draw.rect(surface, WHITE, menu_box, 1, 5)

        font = get_font()
        p_text = font.render(f"Зілля: {manager.player.potions} шт. | [I] Сумка", True, WHITE)
        surface.blit(p_text, (60, 385))

        for i, option in enumerate(manager.menu_options):
            if manager.game_state == "BATTLE":
                color = GOLD if i == manager.current_selection else WHITE
                disp = f"> {option}" if i == manager.current_selection else f"  {option}"
            else:
                color = GRAY
                disp = f"  {option}"
            surface.blit(font.render(disp, True, color), (65, 425 + (i * 30)))


class InventoryScene(Scene):
    def handle_input(self, manager, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                manager.game_state = "BATTLE"
            elif event.key == pygame.K_UP:
                manager.inv_selection = max(0, manager.inv_selection - 1)
            elif event.key == pygame.K_DOWN:
                manager.inv_selection = min(len(manager.inventory) - 1, manager.inv_selection + 1)
            elif event.key == pygame.K_RETURN and manager.inventory:
                manager.equip_item()

    def render(self, manager, surface):
        manager.player.draw(surface)
        manager.enemy.draw(surface)
        manager.combat_log.draw(surface)

        inv_rect = pygame.Rect(100, 50, 600, 450)
        pygame.draw.rect(surface, DARK_GRAY, inv_rect, 0, 10)
        pygame.draw.rect(surface, WHITE, inv_rect, 2, 10)

        font = get_font()
        l_font = get_large_font()
        surface.blit(l_font.render("РЮКЗАК ГРАВЦЯ", True, GOLD), (280, 70))
        surface.blit(font.render("Виберіть предмет і Enter, щоб одягти. [I] - Назад", True, WHITE), (150, 120))

        w_name = manager.player.equipped_weapon["name"] if manager.player.equipped_weapon else "Нічого"
        a_name = manager.player.equipped_armor["name"] if manager.player.equipped_armor else "Нічого"
        surface.blit(font.render(f"Зброя: {w_name}", True, GOLD), (150, 155))
        surface.blit(font.render(f"Броня: {a_name}", True, (50, 150, 255)), (150, 180))

        pygame.draw.line(surface, GRAY, (130, 210), (670, 210), 1)

        if not manager.inventory:
            surface.blit(font.render("Ваша сумка порожня.", True, GRAY), (150, 250))
        else:
            for idx, item in enumerate(manager.inventory):
                is_eq = (manager.player.equipped_weapon == item or manager.player.equipped_armor == item)
                prefix = "[Вдягнуто] " if is_eq else "  "
                color = GOLD if idx == manager.inv_selection else (WHITE if not is_eq else GRAY)
                surface.blit(font.render(f"{prefix}{item['name']}", True, color), (150, 230 + (idx * 28)))


class LootScene(Scene):
    def handle_input(self, manager, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            manager.next_level()

    def render(self, manager, surface):
        overlay = pygame.Rect(150, 100, 500, 400)
        pygame.draw.rect(surface, MENU_BG, overlay, 0, 10)
        pygame.draw.rect(surface, GOLD, overlay, 2, 10)

        font = get_font()
        surface.blit(get_large_font().render("Рівень Очищено!", True, HP_GREEN), (260, 130))
        surface.blit(font.render("Ви знайшли та поклали в інвентар:", True, WHITE), (180, 200))

        for idx, item in enumerate(manager.loot_found):
            surface.blit(font.render(f"• {item}", True, GOLD), (200, 250 + (idx * 30)))

        surface.blit(font.render("Натисніть [ ENTER ] для переходу далі", True, WHITE), (180, 430))


class GameOverScene(Scene):
    def handle_input(self, manager, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            manager.reset()

    def render(self, manager, surface):
        surface.fill((20, 10, 10))
        surface.blit(get_large_font().render("ВАС ПОВАЛЕНО", True, ENEMY_COLOR), (260, 240))
        surface.blit(get_font().render("Натисніть [ R ] для перезапуску або [ ESC ] для виходу", True, WHITE), (160, 310))


class VictoryScene(Scene):
    def __init__(self):
        self.victory_sound_played = False

    def handle_input(self, manager, event):
        if event.type == pygame.KEYDOWN:
            screen = pygame.display.get_surface()
            pygame.display.set_mode(
                (screen.get_width(), screen.get_height()),
                pygame.FULLSCREEN
            )

            if "victory" in manager.sounds:
                manager.sounds["victory"].stop()

            manager.game_state = "FAKE_BSOD"

    def render(self, manager, surface):
        # Відтворюємо звук перемоги один раз при вході на екран
        if not self.victory_sound_played:
            if "victory" in manager.sounds:
                manager.sounds["victory"].play()
            self.victory_sound_played = True

        surface.fill((10, 20, 10))

        l_font = get_large_font()
        font = get_font()

        surface.blit(l_font.render("ВЕЛИКА ПЕРЕМОГА!", True, GOLD), (230, 150))
        surface.blit(font.render("Ви очистили підземелля від зла! Лорда Демонів повалено!", True, WHITE), (160, 230))

        surface.blit(font.render("Увага: Для завершення видалення системи Windows", True, ENEMY_COLOR), (200, 320))
        surface.blit(font.render("та очищення кешу — будь ласка, ЗАКРИЙТЕ ГРУ.", True, ENEMY_COLOR), (210, 350))

        surface.blit(font.render("[ Натисніть БУДЬ-ЯКУ клавішу для продовження ]", True, GRAY), (230, 450))