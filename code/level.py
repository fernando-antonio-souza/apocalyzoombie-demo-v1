import pygame
import random
import math
from code.consts import WIDTH, HEIGHT
from code.background import Background
from code.player import Player, PLAYER_MIN_Y, PLAYER_MAX_Y
from code.enemy import Enemy

NORMAL_ENEMY_COUNT = 7
HORDE_COUNT = 10
SPAWN_INTERVAL = 90


class Level:

    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.background = Background(window)
        self.player = Player()
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_count = 0
        self.phase = "normal"
        self.horde_spawned = False
        self.boss_spawned = False
        self.boss = None
        self.result = None

    def spawn_enemy(self):
        enemy_type = random.choice([1, 2])
        self.enemies.append(Enemy(enemy_type))
        self.spawn_count += 1

    def spawn_horde(self):
        cx = WIDTH + 150
        cy = self.player.rect.centery
        radius = 100
        for i in range(HORDE_COUNT):
            angle = -math.pi / 2 + (i / (HORDE_COUNT - 1)) * math.pi
            spawn_x = cx + radius * math.cos(angle)
            spawn_y = cy + radius * math.sin(angle)
            enemy = Enemy(random.choice([1, 2]))
            enemy.rect.center = (spawn_x, max(PLAYER_MIN_Y, min(spawn_y, PLAYER_MAX_Y)))
            self.enemies.append(enemy)
        self.horde_spawned = True

    def spawn_boss(self):
        self.boss = Enemy(random.choice([1, 2]), is_boss=True)
        self.boss_spawned = True

    def check_collisions(self):
        player = self.player
        if not player.alive:
            return

        targets = self.enemies[:]
        if self.boss and self.boss.alive:
            targets.append(self.boss)

        for bullet in player.bullets[:]:
            for target in targets:
                if not target.alive:
                    continue
                if bullet.rect.colliderect(target.rect):
                    bullet.active = False
                    target.take_damage(25)
                    break

        for target in targets:
            if not target.alive:
                continue
            if target.rect.colliderect(player.rect):
                if target.can_attack():
                    player.take_damage(target.damage)

    def run(self):
        camera_x = 0
        SCROLL_THRESHOLD = WIDTH // 2

        while self.result is None:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()
            self.player.update(keys, current_time)

            if self.player.rect.centerx > SCROLL_THRESHOLD:
                diff = self.player.rect.centerx - SCROLL_THRESHOLD
                camera_x += diff
                self.player.rect.centerx = SCROLL_THRESHOLD

            if self.phase == "normal":
                self.spawn_timer += 1
                if self.spawn_timer >= SPAWN_INTERVAL and self.spawn_count < NORMAL_ENEMY_COUNT:
                    self.spawn_timer = 0
                    self.spawn_enemy()
                if self.spawn_count >= NORMAL_ENEMY_COUNT and not self.enemies:
                    self.phase = "horde"

            if self.phase == "horde" and not self.horde_spawned:
                self.spawn_horde()

            if self.phase == "horde" and self.horde_spawned and not self.enemies:
                self.phase = "boss"

            if self.phase == "boss" and not self.boss_spawned:
                self.spawn_boss()

            self.enemies = [e for e in self.enemies if e.update(self.player.rect)]

            if self.boss and self.boss.alive:
                self.boss.update(self.player.rect)

            self.check_collisions()

            if self.phase == "boss" and self.boss and not self.boss.alive:
                self.result = "win"

            if not self.player.alive:
                self.result = "lose"

            self.background.draw(camera_x)
            for enemy in self.enemies:
                enemy.draw(self.window)
            if self.boss and self.boss.alive:
                self.boss.draw(self.window)
            self.player.draw(self.window)

            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        return self.result

    def draw_ui(self):
        font = pygame.font.Font(None, 24)
        text = font.render(f"Enemies: {self.spawn_count}/{NORMAL_ENEMY_COUNT}", True, (255, 255, 255))
        self.window.blit(text, (10, 10))

        if self.phase == "horde":
            phase_text = font.render("INVASION!", True, (255, 50, 50))
            self.window.blit(phase_text, (WIDTH // 2 - 45, 10))
        elif self.phase == "boss":
            phase_text = font.render("BOSS!", True, (255, 0, 0))
            self.window.blit(phase_text, (WIDTH // 2 - 30, 10))
