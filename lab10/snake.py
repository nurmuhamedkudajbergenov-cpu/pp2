import pygame
import random
import sys

pygame.init()

# размер клетки и поля
CELL = 20
COLS = 25
ROWS = 25

WIDTH = CELL * COLS
HEIGHT = CELL * ROWS + 50  # +50 для HUD сверху

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)
RED = (200, 0, 0)
DARK = (30, 30, 30)
YELLOW = (255, 215, 0)
GRAY = (60, 60, 60)

font = pygame.font.SysFont("Arial", 22, bold=True)

# направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def generate_food(snake):
    # генерируем еду не на стене и не на змейке
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in snake:
            return (x, y)

def draw_grid():
    screen.fill(DARK)
    # стены по краям
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
        color = (0, 255, 0) if i == 0 else GREEN  # голова ярче
        pygame.draw.rect(screen, color, (px + 1, py + 1, CELL - 2, CELL - 2))

def draw_food(food):
    px = food[0] * CELL + CELL // 2
    py = food[1] * CELL + 50 + CELL // 2
    pygame.draw.circle(screen, RED, (px, py), CELL // 2 - 2)

def draw_hud(score, level):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    score_surf = font.render(f"Score: {score}", True, YELLOW)
    level_surf = font.render(f"Level: {level}", True, (100, 200, 255))
    screen.blit(score_surf, (10, 14))
    screen.blit(level_surf, (WIDTH - 120, 14))

# начальное состояние змейки
snake = [(12, 12), (11, 12), (10, 12)]
direction = RIGHT
next_dir = RIGHT

food = generate_food(snake)

score = 0
level = 1
foods_eaten = 0

# скорость (мс между шагами)
speed = 200

last_move = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # меняем направление, нельзя разворачиваться назад
            if event.key == pygame.K_UP and direction != DOWN:
                next_dir = UP
            if event.key == pygame.K_DOWN and direction != UP:
                next_dir = DOWN
            if event.key == pygame.K_LEFT and direction != RIGHT:
                next_dir = LEFT
            if event.key == pygame.K_RIGHT and direction != LEFT:
                next_dir = RIGHT

    # двигаем змейку с интервалом speed мс
    now = pygame.time.get_ticks()
    if now - last_move >= speed:
        last_move = now
        direction = next_dir

        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # проверка столкновения со стеной
        if new_head[0] == 0 or new_head[0] == COLS - 1 or new_head[1] == 0 or new_head[1] == ROWS - 1:
            draw_grid()
            draw_snake(snake)
            draw_food(food)
            draw_hud(score, level)
            text = font.render("GAME OVER! Press R", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            # ждём R или выход
            waiting = True
            while waiting:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                        # перезапуск
                        snake = [(12, 12), (11, 12), (10, 12)]
                        direction = RIGHT
                        next_dir = RIGHT
                        food = generate_food(snake)
                        score = 0
                        level = 1
                        foods_eaten = 0
                        speed = 200
                        waiting = False

        # проверка столкновения с собой
        elif new_head in snake:
            draw_grid()
            draw_snake(snake)
            draw_food(food)
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
                        food = generate_food(snake)
                        score = 0
                        level = 1
                        foods_eaten = 0
                        speed = 200
                        waiting = False
        else:
            # двигаем змейку
            snake.insert(0, new_head)

            if new_head == food:
                # съели еду
                score += 10
                foods_eaten += 1
                food = generate_food(snake)  # генерируем новую еду не на змейке и не на стене

                # повышаем уровень каждые 4 еды
                if foods_eaten % 4 == 0:
                    level += 1
                    speed = max(80, speed - 30)  # увеличиваем скорость
            else:
                snake.pop()  # убираем хвост если еду не съели

    # отрисовка
    draw_grid()
    draw_snake(snake)
    draw_food(food)
    draw_hud(score, level)

    pygame.display.flip()
    clock.tick(60)
