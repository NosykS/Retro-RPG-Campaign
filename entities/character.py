import random
import pygame
from core.config import get_font, HP_GREEN, WHITE, GRAY


class Character:
    def __init__(self, name, max_hp, attack_power, defense, sprite, x, y, potions=0):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.base_attack = attack_power
        self.base_defense = defense
        self.sprite = sprite

        self.base_x = x
        self.base_y = y
        self.rect = pygame.Rect(x, y, 100, 100)
        self.potions = potions

        self.equipped_weapon = None
        self.equipped_armor = None

        # Анімації
        self.anim_offset_x = 0
        self.anim_state = "IDLE"
        self.flash_timer = 0
        self.heal_effect_timer = 0

    @property
    def attack_power(self):
        bonus = self.equipped_weapon["value"] if self.equipped_weapon else 0
        return self.base_attack + bonus

    @property
    def defense(self):
        bonus = self.equipped_armor["value"] if self.equipped_armor else 0
        return self.base_defense + bonus

    def attack(self, target, direction):
        self.anim_state = "ATTACKING"
        self.anim_direction = direction

        raw_damage = self.attack_power + random.randint(-2, 2)
        is_crit = random.randint(1, 5) == 1
        if is_crit: raw_damage *= 2

        final_damage = max(1, raw_damage - target.defense)
        target.current_hp = max(0, target.current_hp - final_damage)
        target.flash_timer = 10
        return final_damage, is_crit

    def heal(self):
        if self.potions > 0:
            heal_amount = 40
            self.current_hp = min(self.max_hp, self.current_hp + heal_amount)
            self.potions -= 1
            self.heal_effect_timer = 20
            return heal_amount
        return 0

    def update_animations(self):
        if self.anim_state == "ATTACKING":
            self.anim_offset_x += 15 * self.anim_direction
            if abs(self.anim_offset_x) >= 60:
                self.anim_state = "RETURNING"
        elif self.anim_state == "RETURNING":
            self.anim_offset_x -= 10 * self.anim_direction
            if (self.anim_direction == 1 and self.anim_offset_x <= 0) or (
                    self.anim_direction == -1 and self.anim_offset_x >= 0):
                self.anim_offset_x = 0
                self.anim_state = "IDLE"

        self.rect.x = self.base_x + self.anim_offset_x
        if self.flash_timer > 0: self.flash_timer -= 1
        if self.heal_effect_timer > 0: self.heal_effect_timer -= 1

    def draw(self, surface):
        surface.blit(self.sprite, (self.rect.x, self.rect.y))

        if self.flash_timer > 0:
            flash_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, 120))
            surface.blit(flash_surf, (self.rect.x, self.rect.y))

        if self.heal_effect_timer > 0:
            pygame.draw.rect(surface, HP_GREEN, self.rect, 3, 8)

        # UI над головою
        hp_bar_bg = pygame.Rect(self.rect.x - 10, self.rect.y - 35, 120, 10)
        pygame.draw.rect(surface, (60, 60, 60), hp_bar_bg)
        hp_ratio = self.current_hp / self.max_hp
        if hp_ratio > 0:
            pygame.draw.rect(surface, HP_GREEN,
                             pygame.Rect(self.rect.x - 10, self.rect.y - 35, int(120 * hp_ratio), 10))

        font = get_font()
        name_txt = font.render(f"{self.name}", True, WHITE)
        hp_txt = font.render(f"HP: {self.current_hp}/{self.max_hp}", True, WHITE)
        stats_txt = font.render(f"АТК: {self.attack_power}  ЗХСТ: {self.defense}", True, GRAY)

        surface.blit(name_txt, (self.rect.x, self.rect.y - 85))
        surface.blit(hp_txt, (self.rect.x, self.rect.y - 60))
        surface.blit(stats_txt, (self.rect.x - 10, self.rect.y + 110))