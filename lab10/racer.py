import pygame
import random
import sys

pygame.init()

# настройки экрана
WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)

font = pygame.font.SysFont("Arial", 28)

# позиция игрока
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120
player_speed = 5

# список врагов и монет
enemies = []
coins = []

score = 0
coin_count = 0

# таймеры спавна
enemy_timer = 0
coin_timer = 0

# скролл дороги
road_y = 0

def draw_road():
    # трава по бокам
    screen.fill(GREEN)
    # серая дорога
    pygame.draw.rect(screen, GRAY, (80, 0, 340, HEIGHT))
    # белая разметка посередине
    global road_y
    road_y += 5
    if road_y > 60:
        road_y = 0
    for i in range(-1, HEIGHT // 60 + 2):
        pygame.draw.rect(screen, WHITE, (245, i * 60 + road_y, 10, 40))

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, 50, 80))

def spawn_enemy():
    x = random.randint(85, 370)
    enemies.append([x, -80])

def spawn_coin():
    # монета появляется в случайном месте на дороге
    x = random.randint(90, 370)
    coins.append([x, -20])

def draw_hud():
    score_text = font.render(f"Score: {score // 10}", True, WHITE)
    # счётчик монет в правом верхнем углу
    coin_text = font.render(f"Coins: {coin_count}", True, YELLOW)
    screen.blit(score_text, (90, 10))
    screen.blit(coin_text, (WIDTH - 160, 10))

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # управление стрелками
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 85:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 370:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 80:
        player_y += player_speed

    # спавн врагов каждые 60 кадров
    enemy_timer += 1
    if enemy_timer >= 60:
        spawn_enemy()
        enemy_timer = 0

    # случайный спавн монет
    coin_timer += 1
    if coin_timer >= random.randint(90, 150):
        spawn_coin()
        coin_timer = 0

    # движение врагов вниз
    for enemy in enemies[:]:
        enemy[1] += 5
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # движение монет вниз
    for coin in coins[:]:
        coin[1] += 4
        if coin[1] > HEIGHT:
            coins.remove(coin)

    score += 1

    # прямоугольник игрока для коллизий
    player_rect = pygame.Rect(player_x, player_y, 50, 80)

    # проверка столкновения с врагами
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 80)
        if player_rect.colliderect(enemy_rect):
            draw_road()
            draw_player(player_x, player_y)
            text = font.render("GAME OVER!", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

    # проверка сбора монет
    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0] - 12, coin[1] - 12, 24, 24)
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            coin_count += 1  # увеличиваем счётчик монет

    # отрисовка всего
    draw_road()

    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin[0], coin[1]), 12)

    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 50, 80))

    draw_player(player_x, player_y)
    draw_hud()

    pygame.display.flip()
