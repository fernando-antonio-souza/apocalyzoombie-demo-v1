import pygame
from code.consts import WIDTH, HEIGHT

PLAYER_SIZE = 64
PLAYER_MIN_Y = HEIGHT * 3 // 5
PLAYER_MAX_Y = HEIGHT - PLAYER_SIZE - 10


class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 8, 4)
        self.speed = 10 * direction
        self.active = True

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.active = False

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 0), self.rect)


class Player:
    def __init__(self):
        self.reset()

    def reset(self):
        s = PLAYER_SIZE
        self.rect = pygame.Rect(80, HEIGHT // 2 - s // 2, s, s)
        self.speed = 4
        self.direction = 1
        self.health = 100
        self.max_health = 100
        self.alive = True
        self.invulnerable = False
        self.invulnerable_timer = 0

        self.animations = self.load_animations()
        self.current_anim = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.shoot_cooldown = 250
        self.last_shot_time = 0
        self.bullets = []

    def load_animations(self):
        path = "./assets/player/"
        names = {
            "idle": "player_idle.png",
            "run": "player_run.png",
        }
        animations = {}
        for name, filename in names.items():
            sheet = pygame.image.load(f"{path}{filename}").convert_alpha()
            frames = []
            fw = sheet.get_height()
            cols = sheet.get_width() // fw
            for i in range(cols):
                frame = sheet.subsurface((i * fw, 0, fw, fw))
                frame = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))
                animations.setdefault(name, []).append(frame)
        return animations

    def handle_input(self, keys, current_time):
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = -1
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 1
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self.rect.x += dx
        self.rect.y += dy

        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(PLAYER_MIN_Y, min(self.rect.y, PLAYER_MAX_Y))

        moving = dx != 0 or dy != 0
        next_anim = "run" if moving else "idle"
        if next_anim != self.current_anim:
            self.current_anim = next_anim
            self.frame_index = 0

        if keys[pygame.K_SPACE]:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        bx = self.rect.right if self.direction == 1 else self.rect.left
        by = self.rect.centery - 2
        self.bullets.append(Bullet(bx, by, self.direction))

    def update(self, keys, current_time):
        if not self.alive:
            return

        self.handle_input(keys, current_time)

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_anim])

        for b in self.bullets:
            b.update()
        self.bullets = [b for b in self.bullets if b.active]

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def take_damage(self, amount):
        if self.invulnerable or not self.alive:
            return
        self.health -= amount
        self.invulnerable = True
        self.invulnerable_timer = 30
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def draw(self, window):
        if not self.alive:
            return

        if self.invulnerable and self.invulnerable_timer % 4 < 2:
            return

        frame = self.animations[self.current_anim][self.frame_index]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, self.rect)

        for b in self.bullets:
            b.draw(window)

        self.draw_health_bar(window)

    def draw_health_bar(self, window):
        bar_w = self.rect.width
        bar_h = 5
        bx = self.rect.x
        by = self.rect.top - 10
        fill = int((self.health / self.max_health) * bar_w)
        pygame.draw.rect(window, (60, 60, 60), (bx, by, bar_w, bar_h))
        pygame.draw.rect(window, (255, 0, 0), (bx, by, fill, bar_h))
        pygame.draw.rect(window, (255, 255, 255), (bx, by, bar_w, bar_h), 1)
