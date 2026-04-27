import pygame
import datetime

pygame.init()

WIDTH, HEIGHT = 1100, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - TSIS 2")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

canvas = pygame.Surface((1000, 700))
canvas.fill(WHITE)
drawing = False
start_pos = None
current_color = BLACK
brush_size = 2
tool = 'pencil'
temp_text = ""
text_pos = None

font = pygame.font.SysFont("Arial", 14)

buttons = [
    {'label': 'Pencil', 'tool': 'pencil'},
    {'label': 'Line', 'tool': 'line'},
    {'label': 'Rect', 'tool': 'rect'},
    {'label': 'Circle', 'tool': 'circle'},
    {'label': 'Square', 'tool': 'square'},
    {'label': 'R-Tri', 'tool': 'right_triangle'},
    {'label': 'E-Tri', 'tool': 'equilateral_triangle'},
    {'label': 'Rhombus', 'tool': 'rhombus'},
    {'label': 'Fill', 'tool': 'fill'},
    {'label': 'Text', 'tool': 'text'},
    {'label': 'Eraser', 'tool': 'eraser'},
    {'label': 'Size 2', 'size': 2},
    {'label': 'Size 5', 'size': 5},
    {'label': 'Size 10', 'size': 10}
]

def flood_fill(surface, x, y, new_color):
    if x < 0 or x >= 1000 or y < 0 or y >= 700: return
    target_color = surface.get_at((x, y))
    if target_color == new_color: return
    pixels = [(x, y)]
    while pixels:
        cx, cy = pixels.pop()
        if surface.get_at((cx, cy)) != target_color: continue
        surface.set_at((cx, cy), new_color)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < 1000 and 0 <= ny < 700:
                if surface.get_at((nx, ny)) == target_color:
                    pixels.append((nx, ny))

def draw_shape(surface, tool_type, start, end, color, size):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    if tool_type == 'line':
        pygame.draw.line(surface, color, start, end, size)
    elif tool_type == 'rect':
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), abs(dx), abs(dy)), size)
    elif tool_type == 'circle':
        radius = int((dx**2 + dy**2)**0.5)
        pygame.draw.circle(surface, color, start, radius, size)
    elif tool_type == 'square':
        side = max(abs(dx), abs(dy))
        pygame.draw.rect(surface, color, (x1, y1, side if dx > 0 else -side, side if dy > 0 else -side), size)
    elif tool_type == 'right_triangle':
        pygame.draw.polygon(surface, color, [(x1, y1), (x1, y2), (x2, y2)], size)
    elif tool_type == 'equilateral_triangle':
        pygame.draw.polygon(surface, color, [(x1, y2), (x2, y2), ((x1 + x2) // 2, y1)], size)
    elif tool_type == 'rhombus':
        pygame.draw.polygon(surface, color, [(x1 + dx//2, y1), (x2, y1 + dy//2), (x1 + dx//2, y2), (x1, y1 + dy//2)], size)

running = True
while running:
    SCREEN.fill(DARK_GRAY)
    SCREEN.blit(canvas, (100, 0))
    
    for i, btn in enumerate(buttons):
        rect = pygame.Rect(5, 5 + i * 45, 90, 40)
        color = BLACK if tool == btn.get('tool') or brush_size == btn.get('size') else WHITE
        pygame.draw.rect(SCREEN, color, rect)
        lbl = font.render(btn['label'], True, WHITE if color == BLACK else BLACK)
        SCREEN.blit(lbl, (rect.x + 5, rect.y + 12))
        btn['rect'] = rect

    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                pygame.image.save(canvas, f"paint_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            if tool == 'text' and text_pos:
                if event.key == pygame.K_RETURN:
                    canvas.blit(font.render(temp_text, True, current_color), text_pos)
                    temp_text, text_pos = "", None
                elif event.key == pygame.K_BACKSPACE: temp_text = temp_text[:-1]
                else: temp_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[0] < 100:
                for btn in buttons:
                    if btn['rect'].collidepoint(mouse_pos):
                        if 'tool' in btn:
                            tool = btn['tool']
                            if tool == 'eraser': current_color = WHITE
                            else: current_color = BLACK
                        if 'size' in btn: brush_size = btn['size']
            else:
                c_pos = (mouse_pos[0] - 100, mouse_pos[1])
                if tool == 'fill': flood_fill(canvas, c_pos[0], c_pos[1], current_color)
                elif tool == 'text': text_pos, temp_text = c_pos, ""
                else: drawing, start_pos = True, c_pos
            
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool not in ['pencil', 'eraser']:
                c_pos = (mouse_pos[0] - 100, mouse_pos[1])
                draw_shape(canvas, tool, start_pos, c_pos, current_color, brush_size)
            drawing = False
            
        if event.type == pygame.MOUSEMOTION and drawing:
            c_pos = (mouse_pos[0] - 100, mouse_pos[1])
            if tool in ['pencil', 'eraser']:
                pygame.draw.line(canvas, current_color, start_pos, c_pos, brush_size)
                start_pos = c_pos

    if drawing and tool not in ['pencil', 'eraser', 'fill', 'text']:
        c_pos = (mouse_pos[0] - 100, mouse_pos[1])
        preview_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
        draw_shape(preview_surf, tool, start_pos, c_pos, current_color, brush_size)
        SCREEN.blit(preview_surf, (100, 0))

    if tool == 'text' and text_pos:
        SCREEN.blit(font.render(temp_text + "|", True, current_color), (text_pos[0] + 100, text_pos[1]))

    pygame.display.flip()

pygame.quit()