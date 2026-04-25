import pygame
import random
import sys

pygame.init()

WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GRAY = (100, 100, 100)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
CYAN = (0, 220, 220)

font = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 18)

player_x = WIDTH // 2 - 25
player_y = HEIGHT - 120
player_speed = 5

enemies = []
coins = []

coin_count = 0
score = 0

enemy_timer = 0
coin_timer = 0
enemy_speed = 5

road_y = 0

COIN_TYPES = [
    {"weight": 1, "color": YELLOW, "radius": 10},
    {"weight": 3, "color": ORANGE, "radius": 13},
    {"weight": 5, "color": CYAN,   "radius": 16},
]

def draw_road():
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (80, 0, 340, HEIGHT))
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
    x = random.randint(90, 370)
    coin_type = random.choice(COIN_TYPES)
    coins.append([x, -20, coin_type])

def draw_hud():
    score_text = font.render(f"Score: {score // 10}", True, WHITE)
    coin_text = font.render(f"Coins: {coin_count}", True, YELLOW)
    screen.blit(score_text, (90, 10))
    screen.blit(coin_text, (WIDTH - 170, 10))
    spd_text = font_small.render(f"enemy spd: {enemy_speed}", True, WHITE)
    screen.blit(spd_text, (90, 42))

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 85:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < 370:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 80:
        player_y += player_speed

    enemy_timer += 1
    if enemy_timer >= 60:
        spawn_enemy()
        enemy_timer = 0

    coin_timer += 1
    if coin_timer >= random.randint(80, 140):
        spawn_coin()
        coin_timer = 0

    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)

    for coin in coins[:]:
        coin[1] += 4
        if coin[1] > HEIGHT:
            coins.remove(coin)

    score += 1

    player_rect = pygame.Rect(player_x, player_y, 50, 80)

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

    for coin in coins[:]:
        cr = coin[2]["radius"]
        coin_rect = pygame.Rect(coin[0] - cr, coin[1] - cr, cr * 2, cr * 2)
        if player_rect.colliderect(coin_rect):
            coins.remove(coin)
            coin_count += coin[2]["weight"]
            if coin_count % 10 == 0 and coin_count > 0:
                enemy_speed += 1

    draw_road()

    for coin in coins:
        pygame.draw.circle(screen, coin[2]["color"], (coin[0], coin[1]), coin[2]["radius"])
        w_text = font_small.render(str(coin[2]["weight"]), True, BLACK)
        screen.blit(w_text, (coin[0] - 4, coin[1] - 7))

    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], 50, 80))

    draw_player(player_x, player_y)
    draw_hud()

    pygame.display.flip()
