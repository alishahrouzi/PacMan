import pygame
import random

# تنظیمات اولیه
pygame.init()

# ابعاد هر سلول در ماز
TILE_SIZE = 30
layout = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "######.##..........##.######",
    "#........###..###..........#",
    "#.####.###......###.####.###",
    "#..........................#",
    "############################"
]

# محاسبه ابعاد صفحه
GRID_WIDTH = len(layout[0])
GRID_HEIGHT = len(layout)
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

# تنظیم صفحه نمایش
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# رنگ‌ها
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

BULLET_SPEED = 5
bullets = []

# تولید ماز
def create_maze():
    walls = []
    empty_spaces = []
    for y, row in enumerate(layout):
        for x, char in enumerate(row):
            if char == "#":
                walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif char == ".":
                empty_spaces.append((x * TILE_SIZE, y * TILE_SIZE))
    return walls, empty_spaces

# کلاس دشمن (Enemy)
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE - 5, TILE_SIZE - 5)
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move(self, walls):
        old_position = self.rect.copy()
        if self.direction == "UP":
            self.rect.y -= 2
        elif self.direction == "DOWN":
            self.rect.y += 2
        elif self.direction == "LEFT":
            self.rect.x -= 2
        elif self.direction == "RIGHT":
            self.rect.x += 2

        # بررسی برخورد با دیوارها
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = old_position
                self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                break

    def draw(self):
        pygame.draw.ellipse(screen, RED, self.rect)

# تابع اصلی
def main():
    clock = pygame.time.Clock()
    running = True
    enemy_spawn_threshold = 150

    # تولید ماز
    walls, empty_spaces = create_maze()

    # ایجاد پک‌من
    pacman_position = random.choice(empty_spaces)
    pacman = pygame.Rect(pacman_position[0], pacman_position[1], TILE_SIZE - 5, TILE_SIZE - 5)
    empty_spaces.remove(pacman_position)

    # تابع برای مدیریت شلیک گلوله
    def shoot_bullet(pacman, direction):
        if direction == "LEFT":
            bullet = pygame.Rect(pacman.x, pacman.y + TILE_SIZE // 4, TILE_SIZE // 2, 5)
            bullets.append((bullet, direction))
        elif direction == "RIGHT":
            bullet = pygame.Rect(pacman.x + TILE_SIZE, pacman.y + TILE_SIZE // 4, TILE_SIZE // 2, 5)
            bullets.append((bullet, direction))
        elif direction == "UP":
            bullet = pygame.Rect(pacman.x + TILE_SIZE // 4, pacman.y, 5, TILE_SIZE // 2)
            bullets.append((bullet, direction))
        elif direction == "DOWN":
            bullet = pygame.Rect(pacman.x + TILE_SIZE // 4, pacman.y + TILE_SIZE, 5, TILE_SIZE // 2)
            bullets.append((bullet, direction))

    # اضافه کردن متغیر جهت پک‌من
    pacman_direction = "RIGHT"

    # ایجاد دشمن‌ها
    enemies = []
    for _ in range(5):
        enemy_position = random.choice(empty_spaces)
        enemies.append(Enemy(enemy_position[0], enemy_position[1]))
        empty_spaces.remove(enemy_position)

    # ایجاد غذاها
    foods = []
    for food_position in random.sample(empty_spaces, len(empty_spaces) // 2):
        foods.append(pygame.Rect(food_position[0] + TILE_SIZE // 4, food_position[1] + TILE_SIZE // 4, TILE_SIZE // 2, TILE_SIZE // 2))

    # تنظیم فونت امتیاز
    font = pygame.font.Font(None, 36)
    score = 0  # امتیاز اولیه

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot_bullet(pacman, pacman_direction)

        # حرکت پک‌من
        keys = pygame.key.get_pressed()
        old_pacman = pacman.copy()
        if keys[pygame.K_LEFT]:
            pacman.x -= 3
            pacman_direction = "LEFT"
        if keys[pygame.K_RIGHT]:
            pacman.x += 3
            pacman_direction = "RIGHT"
        if keys[pygame.K_UP]:
            pacman.y -= 3
            pacman_direction = "UP"
        if keys[pygame.K_DOWN]:
            pacman.y += 3
            pacman_direction = "DOWN"

        # جلوگیری از برخورد پک‌من با دیوارها
        for wall in walls:
            if pacman.colliderect(wall):
                pacman = old_pacman

        # حرکت دشمن‌ها
        for enemy in enemies:
            old_position = enemy.rect.copy()
            enemy.move(walls)

            # بررسی برخورد با سایر دشمن‌ها
            for other_enemy in enemies:
                if enemy != other_enemy and enemy.rect.colliderect(other_enemy.rect):
                    enemy.rect = old_position
                    enemy.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                    break

            # بررسی برخورد دشمن با پک‌من
            if pacman.colliderect(enemy.rect):
                print("Game Over!")
                running = False

        # خوردن غذاها
        for food in foods[:]:
            if pacman.colliderect(food):
                foods.remove(food)
                score += 10

                # بررسی افزودن دشمن جدید
                if score >= enemy_spawn_threshold:
                    enemy_spawn_threshold += 50  # آستانه امتیاز بعدی
                    while True:
                        x = random.randint(1, GRID_WIDTH - 2) * TILE_SIZE
                        y = random.randint(1, GRID_HEIGHT - 2) * TILE_SIZE
                        new_enemy = Enemy(x, y)
                        if not any(new_enemy.rect.colliderect(wall) for wall in walls) and \
                           not any(new_enemy.rect.colliderect(enemy.rect) for enemy in enemies):
                            enemies.append(new_enemy)
                            break

        # برخورد گلوله‌ها
        for bullet, direction in bullets[:]:
            if direction == "LEFT":
                bullet.x -= BULLET_SPEED
            elif direction == "RIGHT":
                bullet.x += BULLET_SPEED
            elif direction == "UP":
                bullet.y -= BULLET_SPEED
            elif direction == "DOWN":
                bullet.y += BULLET_SPEED

            if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                bullets.remove((bullet, direction))

            for wall in walls:
                if bullet.colliderect(wall):
                    bullets.remove((bullet, direction))
                    break

            for enemy in enemies[:]:
                if bullet.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    bullets.remove((bullet, direction))
                    score += 20
                    break

        # رسم عناصر بازی
        screen.fill(BLACK)
        for wall in walls:
            pygame.draw.rect(screen, GREEN, wall)
        for food in foods:
            pygame.draw.circle(screen, BLUE, food.center, TILE_SIZE // 4)
        for enemy in enemies:
            enemy.draw()
        for bullet, _ in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        pygame.draw.ellipse(screen, YELLOW, pacman)

        # نمایش امتیاز
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)


    pygame.quit()

if __name__ == "__main__":
    main()
