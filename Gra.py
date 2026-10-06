import math
import random
import sys

import pygame


WIDTH, HEIGHT = 1280, 720
WORLD_WIDTH, WORLD_HEIGHT = 2200, 2200
TITLE = "OpenWorld Survival Arena"


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 18
        self.speed = 260
        self.angle = 0
        self.health = 100
        self.max_health = 100
        self.ammo = 30
        self.max_ammo = 30
        self.reload_time = 0.0
        self.fire_cooldown = 0.0
        self.stamina = 100
        self.score = 0
        self.kills = 0

    def update(self, dt, keys, mouse_world_pos):
        move_x = (keys[pygame.K_d] - keys[pygame.K_a])
        move_y = (keys[pygame.K_s] - keys[pygame.K_w])
        if move_x != 0 or move_y != 0:
            length = math.hypot(move_x, move_y)
            move_x /= length
            move_y /= length

            if keys[pygame.K_LSHIFT] and self.stamina > 0:
                speed = self.speed * 1.7
                self.stamina = max(0, self.stamina - 25 * dt)
            else:
                speed = self.speed
                self.stamina = min(100, self.stamina + 18 * dt)

            self.x += move_x * speed * dt
            self.y += move_y * speed * dt

        self.x = max(self.radius, min(WORLD_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(WORLD_HEIGHT - self.radius, self.y))

        dx = mouse_world_pos[0] - self.x
        dy = mouse_world_pos[1] - self.y
        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))

        if self.fire_cooldown > 0:
            self.fire_cooldown -= dt
        if self.reload_time > 0:
            self.reload_time -= dt
            if self.reload_time <= 0:
                self.ammo = self.max_ammo

    def draw(self, screen, camera_x, camera_y):
        pos = (int(self.x - camera_x), int(self.y - camera_y))
        pygame.draw.circle(screen, (50, 180, 255), pos, self.radius)
        pygame.draw.circle(screen, (255, 255, 255), pos, self.radius, 2)

        gun_len = 24
        end_x = pos[0] + math.cos(math.radians(self.angle)) * gun_len
        end_y = pos[1] + math.sin(math.radians(self.angle)) * gun_len
        pygame.draw.line(screen, (30, 30, 30), pos, (int(end_x), int(end_y)), 5)


class Bullet:
    def __init__(self, x, y, angle, speed=700, damage=18):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.radius = 4
        self.life = 1.2

    def update(self, dt):
        self.x += math.cos(math.radians(self.angle)) * self.speed * dt
        self.y += math.sin(math.radians(self.angle)) * self.speed * dt
        self.life -= dt

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.circle(screen, (255, 220, 80), (int(self.x - camera_x), int(self.y - camera_y)), self.radius)


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 16
        self.speed = random.uniform(120, 170)
        self.health = 60
        self.max_health = 60
        self.damage_cooldown = 0.0

    def update(self, dt, player, obstacles):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            move_x = dx / dist
            move_y = dy / dist
            new_x = self.x + move_x * self.speed * dt
            new_y = self.y + move_y * self.speed * dt

            if not any(self._collides_with_obstacle(new_x, self.y, obstacles) for _ in [0]):
                self.x = new_x
            if not any(self._collides_with_obstacle(self.x, new_y, obstacles) for _ in [0]):
                self.y = new_y

        if dist < self.radius + player.radius + 8 and self.damage_cooldown <= 0:
            player.health -= 12
            self.damage_cooldown = 0.6

    def _collides_with_obstacle(self, next_x, next_y, obstacles):
        for obs in obstacles:
            if obs.collidepoint(next_x, next_y):
                return True
        return False

    def draw(self, screen, camera_x, camera_y):
        pos = (int(self.x - camera_x), int(self.y - camera_y))
        pygame.draw.circle(screen, (220, 60, 60), pos, self.radius)
        pygame.draw.circle(screen, (255, 200, 200), pos, self.radius, 2)

        health_bar_width = self.radius * 2
        health_ratio = max(0, self.health / self.max_health)
        bar_x = pos[0] - self.radius
        bar_y = pos[1] - self.radius - 14
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y, health_bar_width, 6))
        pygame.draw.rect(screen, (70, 220, 90), (bar_x, bar_y, health_bar_width * health_ratio, 6))


class Pickup:
    def __init__(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.radius = 12
        self.value = 25 if kind == "health" else 20

    def draw(self, screen, camera_x, camera_y):
        pos = (int(self.x - camera_x), int(self.y - camera_y))
        color = (70, 220, 120) if self.kind == "health" else (255, 200, 80)
        pygame.draw.circle(screen, color, pos, self.radius)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 72)
        self.running = True
        self.game_over = False
        self.wave = 1
        self.camera_x = 0
        self.camera_y = 0
        self.player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
        self.bullets = []
        self.enemies = []
        self.pickups = []
        self.obstacles = []
        self._build_world()
        self._spawn_wave(8)

    def _build_world(self):
        self.obstacles = [
            pygame.Rect(300, 200, 180, 90),
            pygame.Rect(820, 260, 220, 120),
            pygame.Rect(1180, 920, 260, 180),
            pygame.Rect(500, 980, 220, 140),
            pygame.Rect(1480, 500, 190, 120),
            pygame.Rect(1780, 1320, 200, 160),
            pygame.Rect(900, 1480, 260, 180),
            pygame.Rect(200, 1360, 220, 170),
            pygame.Rect(1450, 1650, 280, 190),
        ]

        for i in range(10):
            px = random.randint(100, WORLD_WIDTH - 100)
            py = random.randint(100, WORLD_HEIGHT - 100)
            self.pickups.append(Pickup(px, py, "health" if i % 2 == 0 else "ammo"))

    def _spawn_wave(self, count):
        for _ in range(count):
            while True:
                x = random.randint(50, WORLD_WIDTH - 50)
                y = random.randint(50, WORLD_HEIGHT - 50)
                if math.hypot(x - self.player.x, y - self.player.y) > 350:
                    self.enemies.append(Enemy(x, y))
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    if self.player.reload_time <= 0 and self.player.ammo < self.player.max_ammo:
                        self.player.reload_time = 1.2
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.game_over:
                    self._shoot()

    def _shoot(self):
        if self.player.reload_time > 0:
            return
        if self.player.ammo <= 0:
            self.player.reload_time = 1.1
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = mouse_x + self.camera_x
        world_y = mouse_y + self.camera_y

        angle = math.degrees(math.atan2(world_y - self.player.y, world_x - self.player.x))
        self.bullets.append(Bullet(self.player.x, self.player.y, angle))
        self.player.ammo -= 1
        self.player.fire_cooldown = 0.12

        if self.player.ammo <= 0:
            self.player.reload_time = 1.2

    def update(self, dt):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        world_x = mouse_x + self.camera_x
        world_y = mouse_y + self.camera_y
        self.player.update(dt, keys, (world_x, world_y))

        self.camera_x = self.player.x - WIDTH / 2
        self.camera_y = self.player.y - HEIGHT / 2
        self.camera_x = max(0, min(WORLD_WIDTH - WIDTH, self.camera_x))
        self.camera_y = max(0, min(WORLD_HEIGHT - HEIGHT, self.camera_y))

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.life <= 0:
                self.bullets.remove(bullet)
                continue
            if bullet.x < 0 or bullet.x > WORLD_WIDTH or bullet.y < 0 or bullet.y > WORLD_HEIGHT:
                self.bullets.remove(bullet)
                continue

            for enemy in self.enemies[:]:
                if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) <= enemy.radius + bullet.radius:
                    enemy.health -= bullet.damage
                    self.bullets.remove(bullet)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.player.kills += 1
                        self.player.score += 100
                        if random.random() < 0.3:
                            self.pickups.append(Pickup(enemy.x, enemy.y, "ammo"))
                    break

        for enemy in self.enemies:
            enemy.update(dt, self.player, self.obstacles)

        for pickup in self.pickups[:]:
            if math.hypot(self.player.x - pickup.x, self.player.y - pickup.y) <= self.player.radius + pickup.radius + 4:
                if pickup.kind == "health":
                    self.player.health = min(self.player.max_health, self.player.health + pickup.value)
                else:
                    self.player.ammo = min(self.player.max_ammo, self.player.ammo + pickup.value)
                self.pickups.remove(pickup)

        if self.player.health <= 0:
            self.game_over = True

        if len(self.enemies) == 0:
            self.wave += 1
            self._spawn_wave(6 + self.wave * 2)

        if self.player.ammo <= 0 and self.player.reload_time <= 0:
            self.player.reload_time = 1.1

    def draw(self):
        self.screen.fill((18, 28, 34))

        for y in range(0, WORLD_HEIGHT, 60):
            for x in range(0, WORLD_WIDTH, 60):
                rect = pygame.Rect(x - self.camera_x, y - self.camera_y, 50, 50)
                pygame.draw.rect(self.screen, (28, 42, 52), rect, 1)

        for obs in self.obstacles:
            world_rect = pygame.Rect(obs.x - self.camera_x, obs.y - self.camera_y, obs.width, obs.height)
            pygame.draw.rect(self.screen, (60, 72, 84), world_rect)
            pygame.draw.rect(self.screen, (110, 130, 160), world_rect, 2)

        for pickup in self.pickups:
            pickup.draw(self.screen, self.camera_x, self.camera_y)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.camera_x, self.camera_y)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        self.player.draw(self.screen, self.camera_x, self.camera_y)

        self._draw_hud()
        pygame.display.flip()

    def _draw_hud(self):
        health_text = self.font.render(f"HP: {int(self.player.health)}/{self.player.max_health}", True, (255, 255, 255))
        ammo_text = self.font.render(f"Ammo: {self.player.ammo}/{self.player.max_ammo}", True, (255, 255, 255))
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        wave_text = self.font.render(f"Wave: {self.wave}", True, (255, 255, 255))
        self.screen.blit(health_text, (20, 20))
        self.screen.blit(ammo_text, (20, 50))
        self.screen.blit(score_text, (20, 80))
        self.screen.blit(wave_text, (20, 110))

        stamina_bar_rect = pygame.Rect(20, HEIGHT - 40, 220, 18)
        pygame.draw.rect(self.screen, (30, 30, 30), stamina_bar_rect)
        pygame.draw.rect(self.screen, (95, 200, 120), (20, HEIGHT - 40, 220 * (self.player.stamina / 100), 18))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            game_over_text = self.big_font.render("GAME OVER", True, (255, 80, 80))
            restart_text = self.font.render("Press SPACE to restart", True, (255, 255, 255))
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        print("Gra zamknieta. Press ESC to quit the game.")
        sys.exit()


if __name__ == "__main__":
    Game().run()
