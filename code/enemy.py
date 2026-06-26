import pygame
import random
from code.consts import WIDTH
from code.player import PLAYER_MIN_Y, PLAYER_MAX_Y

ENEMY_SIZE_1 = 48
ENEMY_SIZE_2 = 64
ENEMY_BOSS_SIZE = 96

ENEMY_STATS = {
    1: {"health": 30, "damage": 10, "speed": 2.0, "size": ENEMY_SIZE_1},
    2: {"health": 60, "damage": 20, "speed": 1.5, "size": ENEMY_SIZE_2},
}


class Enemy:
    def __init__(self, enemy_type, is_boss=False):
        self.enemy_type = enemy_type
        self.is_boss = is_boss
        stats = ENEMY_STATS[enemy_type]
        size = ENEMY_BOSS_SIZE if is_boss else stats["size"]
        self.size = size
        self.health = 500 if is_boss else stats["health"]
        self.max_health = self.health
        self.damage = 40 if is_boss else stats["damage"]
        self.speed = 1.5 if is_boss else stats["speed"]
        self.alive = True

        y = random.randint(PLAYER_MIN_Y, PLAYER_MAX_Y)
        self.rect = pygame.Rect(WIDTH + 50, y, size, size)

        self.animations = self.load_animations(enemy_type, size)
        self.current_anim = "run"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 10

        self.attack_cooldown = 60
        self.attack_timer = 0

    def load_animations(self, enemy_type, size):
        path = f"./assets/enemies/enemie{enemy_type}/"
        names = {
            "idle": f"enemie{enemy_type}_idle.png",
            "run": f"enemie{enemy_type}_run.png",
        }
        animations = {}
        for name, filename in names.items():
            sheet = pygame.image.load(f"{path}{filename}").convert_alpha()
            frames = []
            fw = sheet.get_height()
            cols = sheet.get_width() // fw
            for i in range(cols):
                frame = sheet.subsurface((i * fw, 0, fw, fw))
                frame = pygame.transform.scale(frame, (size, size))
                animations.setdefault(name, []).append(frame)
        return animations

    def update(self, player_rect):
        if not self.alive:
            return False

        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dist = (dx * dx + dy * dy) ** 0.5
        if dist > 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed

        self.rect.y = max(PLAYER_MIN_Y, min(self.rect.y, PLAYER_MAX_Y))

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])

        if self.attack_timer > 0:
            self.attack_timer -= 1

        return True

    def take_damage(self, amount):
        if not self.alive:
            return False
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            return True
        return False

    def can_attack(self):
        if self.attack_timer > 0:
            return False
        self.attack_timer = self.attack_cooldown
        return True

    def draw(self, window):
        if not self.alive:
            return
        frame = self.animations[self.current_anim][self.frame_index]
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, self.rect)

        if self.is_boss:
            bar_w = self.rect.width
            bar_h = 6
            bx = self.rect.x
            by = self.rect.top - 12
            fill = int((self.health / self.max_health) * bar_w)
            pygame.draw.rect(window, (60, 60, 60), (bx, by, bar_w, bar_h))
            pygame.draw.rect(window, (255, 0, 0), (bx, by, fill, bar_h))
            pygame.draw.rect(window, (255, 255, 255), (bx, by, bar_w, bar_h), 1)
