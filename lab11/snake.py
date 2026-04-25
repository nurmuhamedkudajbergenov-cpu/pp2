import pygame
import random
import sys

pygame.init()

CELL = 20
COLS = 25
ROWS = 25
WIDTH = CELL * COLS
HEIGHT = CELL * ROWS + 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
RED = (200, 0, 0)
DARK = (30, 30, 30)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
CYAN = (0, 220, 220)
GRAY = (60, 60, 60)

font = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

FOOD_TYPES = [
    {"weight": 1, "color": RED,    "time": 8000},
    {"weight": 3, "color": ORANGE, "time": 5000},
    {"weight": 5, "color": CYAN,   "time": 3000},
]

def generate_food(snake, existing_foods):
    taken = set(snake) | {f["pos"] for f in existing_foods}
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in taken:
            ftype = random.choice(FOOD_TYPES)
            return {
                "pos": (x, y),
                "weight": ftype["weight"],
                "color": ftype["color"],
                "spawn_time": pygame.time.get_ticks(),
                "lifetime": ftype["time"]
            }

def draw_grid():
    screen.fill(DARK)
    for c in range(COLS):
        for r in range(ROWS):
            px = c * CELL
            py = r * CELL + 50
            if c == 0 or c == COLS - 1 or r == 0 or r == ROWS - 1:
                pygame.draw.rect(screen, GRAY, (px, py, CELL, CELL))

def draw_snake(snake):
    for i, (c, r) in enumerate(snake):
        px = c * CELL
        py = r * CELL + 50
        color = (0, 255, 0) if i == 0 else GREEN
        pygame.draw.rect(screen, color, (px + 1, py + 1, CELL - 2, CELL - 2))

def draw_foods(foods):
    now = pygame.time.get_ticks()
    for f in foods:
        c, r = f["pos"]
        px = c * CELL + CELL // 2
        py = r * CELL + 50 + CELL // 2
        elapsed = now - f["spawn_time"]
        left = f["lifetime"] - elapsed
        ratio = left / f["lifetime"]
        radius = max(4, int((CELL // 2 - 2) * ratio) + 3)
        pygame.draw.circle(screen, f["color"], (px, py), CELL // 2 - 1)
        w_text = font_small.render(str(f["weight"]), True, BLACK)
        screen.blit(w_text, (px - 4, py - 6))

def draw_hud(score, level):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    screen.blit(font.render(f"Score: {score}", True, YELLOW), (10, 14))
    screen.blit(font.render(f"Level: {level}", True, CYAN), (WIDTH - 120, 14))

snake = [(12, 12), (11, 12), (10, 12)]
direction = RIGHT
next_dir = RIGHT

foods = [generate_food(snake, [])]

score = 0
level = 1
foods_eaten = 0
speed = 200
last_move = pygame.time.get_ticks()
food_spawn_timer = pygame.time.get_ticks()

running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != DOWN:
                next_dir = UP
            if event.key == pygame.K_DOWN and direction != UP:
                next_dir = DOWN
            if event.key == pygame.K_LEFT and direction != RIGHT:
                next_dir = LEFT
            if event.key == pygame.K_RIGHT and direction != LEFT:
                next_dir = RIGHT

    for f in foods[:]:
        if now - f["spawn_time"] >= f["lifetime"]:
            foods.remove(f)

    if now - food_spawn_timer >= 4000:
        food_spawn_timer = now
        if len(foods) < 3:
            foods.append(generate_food(snake, foods))

    if now - last_move >= speed:
        last_move = now
        direction = next_dir

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        if new_head[0] == 0 or new_head[0] == COLS - 1 or new_head[1] == 0 or new_head[1] == ROWS - 1:
            draw_grid()
            draw_snake(snake)
            draw_foods(foods)
            draw_hud(score, level)
            text = font.render("GAME OVER! Press R", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                        snake = [(12, 12), (11, 12), (10, 12)]
                        direction = RIGHT
                        next_dir = RIGHT
                        foods = [generate_food(snake, [])]
                        score = 0
                        level = 1
                        foods_eaten = 0
                        speed = 200
                        waiting = False

        elif new_head in snake:
            draw_grid()
            draw_snake(snake)
            draw_foods(foods)
            draw_hud(score, level)
            text = font.render("GAME OVER! Press R", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                        snake = [(12, 12), (11, 12), (10, 12)]
                        direction = RIGHT
                        next_dir = RIGHT
                        foods = [generate_food(snake, [])]
                        score = 0
                        level = 1
                        foods_eaten = 0
                        speed = 200
                        waiting = False
        else:
            snake.insert(0, new_head)
            eaten = None
            for f in foods:
                if new_head == f["pos"]:
                    eaten = f
                    break
            if eaten:
                score += 10 * eaten["weight"]
                foods_eaten += 1
                foods.remove(eaten)
                foods.append(generate_food(snake, foods))
                if foods_eaten % 4 == 0:
                    level += 1
                    speed = max(80, speed - 30)
            else:
                snake.pop()

    draw_grid()
    draw_snake(snake)
    draw_foods(foods)
    draw_hud(score, level)

    pygame.display.flip()
    clock.tick(60)
