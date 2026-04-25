import pygame
import sys
import math

pygame.init()

WIDTH = 900
HEIGHT = 600
PANEL = 150  # ширина панели инструментов слева

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK = (50, 50, 50)

font = pygame.font.SysFont("Arial", 16)

# холст — отдельная поверхность
canvas = pygame.Surface((WIDTH - PANEL, HEIGHT))
canvas.fill(WHITE)

# текущий инструмент и цвет
tool = "pencil"
color = BLACK
brush_size = 5

# для рисования фигур (начальная точка)
start_pos = None
drawing = False
last_pos = None

# палитра цветов
palette = [
    (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 200, 0),
    (0, 0, 255), (255, 255, 0), (255, 140, 0), (150, 0, 200),
    (0, 200, 200), (255, 100, 200), (139, 90, 43), (128, 128, 128)
]

def draw_panel():
    # фон панели
    pygame.draw.rect(screen, DARK, (0, 0, PANEL, HEIGHT))

    # заголовок
    t = font.render("TOOLS", True, WHITE)
    screen.blit(t, (10, 10))

    # кнопки инструментов
    tools = ["pencil", "rect", "circle", "eraser"]
    for i, name in enumerate(tools):
        rect = pygame.Rect(10, 35 + i * 40, PANEL - 20, 32)
        btn_color = (80, 120, 200) if tool == name else (70, 70, 90)
        pygame.draw.rect(screen, btn_color, rect, border_radius=5)
        label = font.render(name, True, WHITE)
        screen.blit(label, (rect.x + 5, rect.y + 8))

    # размер кисти
    t2 = font.render("SIZE", True, WHITE)
    screen.blit(t2, (10, 205))

    pygame.draw.rect(screen, (70, 70, 90), (10, 225, 28, 24), border_radius=4)
    screen.blit(font.render("-", True, WHITE), (18, 228))

    pygame.draw.rect(screen, (70, 70, 90), (45, 225, 28, 24), border_radius=4)
    screen.blit(font.render("+", True, WHITE), (53, 228))

    screen.blit(font.render(str(brush_size), True, WHITE), (82, 228))

    # палитра
    t3 = font.render("COLORS", True, WHITE)
    screen.blit(t3, (10, 265))

    for i, c in enumerate(palette):
        col = i % 3
        row = i // 3
        rect = pygame.Rect(10 + col * 42, 285 + row * 42, 36, 36)
        pygame.draw.rect(screen, c, rect, border_radius=4)
        if c == color:
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=4)

    # кнопка очистки
    clear_rect = pygame.Rect(10, HEIGHT - 50, PANEL - 20, 34)
    pygame.draw.rect(screen, (180, 50, 50), clear_rect, border_radius=5)
    ct = font.render("Clear", True, WHITE)
    screen.blit(ct, (clear_rect.x + 30, clear_rect.y + 8))

    return clear_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if mx < PANEL:
                # клик по панели
                tools_list = ["pencil", "rect", "circle", "eraser"]
                for i, name in enumerate(tools_list):
                    rect = pygame.Rect(10, 35 + i * 40, PANEL - 20, 32)
                    if rect.collidepoint(mx, my):
                        tool = name

                # размер кисти
                if pygame.Rect(10, 225, 28, 24).collidepoint(mx, my):
                    brush_size = max(1, brush_size - 2)
                if pygame.Rect(45, 225, 28, 24).collidepoint(mx, my):
                    brush_size = min(50, brush_size + 2)

                # цвета
                for i, c in enumerate(palette):
                    col = i % 3
                    row = i // 3
                    rect = pygame.Rect(10 + col * 42, 285 + row * 42, 36, 36)
                    if rect.collidepoint(mx, my):
                        color = c

                # очистка
                if pygame.Rect(10, HEIGHT - 50, PANEL - 20, 34).collidepoint(mx, my):
                    canvas.fill(WHITE)

            else:
                # клик на холсте — начало рисования
                drawing = True
                start_pos = (mx - PANEL, my)
                last_pos = (mx - PANEL, my)

                if tool == "pencil":
                    pygame.draw.circle(canvas, color, last_pos, brush_size)
                if tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, last_pos, brush_size)

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                mx, my = event.pos
                cur = (mx - PANEL, my)

                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, cur, brush_size * 2)
                    pygame.draw.circle(canvas, color, cur, brush_size)
                    last_pos = cur

                if tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, cur, brush_size * 2)
                    pygame.draw.circle(canvas, WHITE, cur, brush_size)
                    last_pos = cur

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                mx, my = event.pos
                cur = (mx - PANEL, my)

                if tool == "rect" and start_pos:
                    # рисуем прямоугольник от start_pos до cur
                    x = min(start_pos[0], cur[0])
                    y = min(start_pos[1], cur[1])
                    w = abs(cur[0] - start_pos[0])
                    h = abs(cur[1] - start_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

                if tool == "circle" and start_pos:
                    # радиус = расстояние от start до cur
                    radius = int(math.hypot(cur[0] - start_pos[0], cur[1] - start_pos[1]))
                    if radius > 0:
                        pygame.draw.circle(canvas, color, start_pos, radius, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    # отрисовка
    screen.fill(DARK)
    draw_panel()
    screen.blit(canvas, (PANEL, 0))

    # граница холста
    pygame.draw.rect(screen, GRAY, (PANEL, 0, WIDTH - PANEL, HEIGHT), 2)

    pygame.display.flip()
    clock.tick(60)
