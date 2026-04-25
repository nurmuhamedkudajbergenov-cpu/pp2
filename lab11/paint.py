import pygame
import sys
import math

pygame.init()

WIDTH = 900
HEIGHT = 600
PANEL = 160

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK = (50, 50, 50)

font = pygame.font.SysFont("Arial", 15)

canvas = pygame.Surface((WIDTH - PANEL, HEIGHT))
canvas.fill(WHITE)

tool = "pencil"
color = BLACK
brush_size = 5

start_pos = None
drawing = False
last_pos = None

palette = [
    (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 200, 0),
    (0, 0, 255), (255, 255, 0), (255, 140, 0), (150, 0, 200),
    (0, 200, 200), (255, 100, 200), (139, 90, 43), (128, 128, 128)
]

tools_list = ["pencil", "rect", "square", "circle", "r.triangle", "e.triangle", "rhombus", "eraser"]

def draw_panel():
    pygame.draw.rect(screen, DARK, (0, 0, PANEL, HEIGHT))
    screen.blit(font.render("TOOLS", True, WHITE), (10, 8))

    for i, name in enumerate(tools_list):
        rect = pygame.Rect(8, 28 + i * 34, PANEL - 16, 28)
        btn_color = (80, 120, 200) if tool == name else (70, 70, 90)
        pygame.draw.rect(screen, btn_color, rect, border_radius=4)
        screen.blit(font.render(name, True, WHITE), (rect.x + 5, rect.y + 7))

    screen.blit(font.render("SIZE", True, WHITE), (10, 318))
    pygame.draw.rect(screen, (70, 70, 90), (8, 336, 26, 22), border_radius=4)
    screen.blit(font.render("-", True, WHITE), (16, 339))
    pygame.draw.rect(screen, (70, 70, 90), (40, 336, 26, 22), border_radius=4)
    screen.blit(font.render("+", True, WHITE), (48, 339))
    screen.blit(font.render(str(brush_size), True, WHITE), (74, 339))

    screen.blit(font.render("COLORS", True, WHITE), (10, 368))
    for i, c in enumerate(palette):
        col = i % 3
        row = i // 3
        rect = pygame.Rect(8 + col * 48, 386 + row * 42, 40, 36)
        pygame.draw.rect(screen, c, rect, border_radius=4)
        if c == color:
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=4)

    clear_rect = pygame.Rect(8, HEIGHT - 44, PANEL - 16, 34)
    pygame.draw.rect(screen, (180, 50, 50), clear_rect, border_radius=5)
    screen.blit(font.render("Clear", True, WHITE), (clear_rect.x + 32, clear_rect.y + 9))

def handle_panel_click(mx, my):
    global tool, brush_size, color

    for i, name in enumerate(tools_list):
        rect = pygame.Rect(8, 28 + i * 34, PANEL - 16, 28)
        if rect.collidepoint(mx, my):
            tool = name
            return

    if pygame.Rect(8, 336, 26, 22).collidepoint(mx, my):
        brush_size = max(1, brush_size - 2)
    if pygame.Rect(40, 336, 26, 22).collidepoint(mx, my):
        brush_size = min(50, brush_size + 2)

    for i, c in enumerate(palette):
        col = i % 3
        row = i // 3
        rect = pygame.Rect(8 + col * 48, 386 + row * 42, 40, 36)
        if rect.collidepoint(mx, my):
            color = c
            return

    if pygame.Rect(8, HEIGHT - 44, PANEL - 16, 34).collidepoint(mx, my):
        canvas.fill(WHITE)

def draw_right_triangle(surface, col, x1, y1, x2, y2, thickness):
    # прямоугольный треугольник: прямой угол снизу-слева
    p1 = (x1, y1)
    p2 = (x1, y2)
    p3 = (x2, y2)
    pygame.draw.polygon(surface, col, [p1, p2, p3], thickness)

def draw_equilateral_triangle(surface, col, x1, y1, x2, y2, thickness):
    cx = (x1 + x2) / 2
    base = abs(x2 - x1)
    h = base * math.sqrt(3) / 2
    p1 = (x1, y2)
    p2 = (x2, y2)
    p3 = (cx, y2 - h)
    pygame.draw.polygon(surface, col, [p1, p2, p3], thickness)

def draw_rhombus(surface, col, x1, y1, x2, y2, thickness):
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    p1 = (cx, y1)
    p2 = (x2, cy)
    p3 = (cx, y2)
    p4 = (x1, cy)
    pygame.draw.polygon(surface, col, [p1, p2, p3, p4], thickness)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if mx < PANEL:
                handle_panel_click(mx, my)
            else:
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
            if drawing and start_pos:
                mx, my = event.pos
                cur = (mx - PANEL, my)
                x1, y1 = start_pos
                x2, y2 = cur

                if tool == "rect":
                    rx = min(x1, x2)
                    ry = min(y1, y2)
                    rw = abs(x2 - x1)
                    rh = abs(y2 - y1)
                    pygame.draw.rect(canvas, color, (rx, ry, rw, rh), brush_size)

                elif tool == "square":
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    rx = min(x1, x2)
                    ry = min(y1, y2)
                    pygame.draw.rect(canvas, color, (rx, ry, side, side), brush_size)

                elif tool == "circle":
                    radius = int(math.hypot(x2 - x1, y2 - y1))
                    if radius > 0:
                        pygame.draw.circle(canvas, color, (x1, y1), radius, brush_size)

                elif tool == "r.triangle":
                    draw_right_triangle(canvas, color, x1, y1, x2, y2, brush_size)

                elif tool == "e.triangle":
                    draw_equilateral_triangle(canvas, color, x1, y1, x2, y2, brush_size)

                elif tool == "rhombus":
                    draw_rhombus(canvas, color, x1, y1, x2, y2, brush_size)

                drawing = False
                start_pos = None
                last_pos = None

    screen.fill(DARK)
    draw_panel()
    screen.blit(canvas, (PANEL, 0))
    pygame.draw.rect(screen, GRAY, (PANEL, 0, WIDTH - PANEL, HEIGHT), 2)

    pygame.display.flip()
    clock.tick(60)
