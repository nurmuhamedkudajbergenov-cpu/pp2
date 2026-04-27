import pygame
import random
from config import *


UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)
OPPOSITES = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def cell_to_px(col, row):
    """Top-left pixel of a grid cell."""
    return (GRID_X + col * CELL_SIZE, GRID_Y + row * CELL_SIZE)


def random_cell(exclude: set) -> tuple[int, int]:
    while True:
        c = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if c not in exclude:
            return c


class Food:
    TYPES = {
        "normal": {"color": C_FOOD_NORMAL, "points": 10, "weight": 60},
        "bonus":  {"color": C_FOOD_BONUS,  "points": 30, "weight": 25},
        "rare":   {"color": C_FOOD_RARE,   "points": 50, "weight": 15},
    }
    LIFETIME = 8000   # ms before disappearing

    def __init__(self, pos, kind=None):
        if kind is None:
            kind = random.choices(
                list(self.TYPES.keys()),
                weights=[v["weight"] for v in self.TYPES.values()]
            )[0]
        self.kind    = kind
        self.pos     = pos
        self.color   = self.TYPES[kind]["color"]
        self.points  = self.TYPES[kind]["points"]
        self.born    = pygame.time.get_ticks()
        self.poison  = False

    def expired(self):
        return pygame.time.get_ticks() - self.born > self.LIFETIME

    def time_left_pct(self):
        return max(0.0, 1.0 - (pygame.time.get_ticks()-self.born)/self.LIFETIME)

    def draw(self, surf, grid_on):
        x, y = cell_to_px(*self.pos)
        r = pygame.Rect(x+1, y+1, CELL_SIZE-2, CELL_SIZE-2)
        pygame.draw.rect(surf, self.color, r, border_radius=4)
        # Timer bar
        bar_w = int((CELL_SIZE-2) * self.time_left_pct())
        pygame.draw.rect(surf, (255,255,255),
                         (x+1, y+CELL_SIZE-4, bar_w, 3))


class PoisonFood(Food):
    def __init__(self, pos):
        super().__init__(pos, kind="normal")
        self.poison = True
        self.color  = C_FOOD_POISON
        self.points = 0
        self.born   = pygame.time.get_ticks()
        self.LIFETIME = 10000

    def draw(self, surf, grid_on):
        x, y = cell_to_px(*self.pos)
        r = pygame.Rect(x+1, y+1, CELL_SIZE-2, CELL_SIZE-2)
        pygame.draw.rect(surf, self.color, r, border_radius=4)
        # Skull symbol
        font = pygame.font.SysFont(None, 18)
        t = font.render("☠", True, (200, 0, 0))
        surf.blit(t, (x+2, y+1))
        bar_w = int((CELL_SIZE-2) * self.time_left_pct())
        pygame.draw.rect(surf, (180,20,20),
                         (x+1, y+CELL_SIZE-4, bar_w, 3))


class PowerUp:
    TYPES = {
        "speed":  {"color": C_PU_SPEED,  "label": "⚡", "duration": 5000},
        "slow":   {"color": C_PU_SLOW,   "label": "❄",  "duration": 5000},
        "shield": {"color": C_PU_SHIELD, "label": "🛡", "duration": 0},
    }
    FIELD_TIMEOUT = 8000  # disappears from field after 8s

    def __init__(self, pos, kind=None):
        self.kind  = kind or random.choice(list(self.TYPES.keys()))
        self.pos   = pos
        self.color = self.TYPES[self.kind]["color"]
        self.label = self.TYPES[self.kind]["label"]
        self.born  = pygame.time.get_ticks()

    def expired(self):
        return pygame.time.get_ticks() - self.born > self.FIELD_TIMEOUT

    def draw(self, surf, grid_on):
        x, y = cell_to_px(*self.pos)
        r = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surf, self.color, r, border_radius=5)
        pygame.draw.rect(surf, C_WHITE, r, 1, border_radius=5)
        font = pygame.font.SysFont(None, 18)
        t = font.render(self.label, True, (0,0,0))
        surf.blit(t, t.get_rect(center=r.center))


# ─── Snake ────────────────────────────────────────────────────────────────────
class Snake:
    def __init__(self, color):
        cx, cy = COLS//2, ROWS//2
        self.body      = [(cx, cy), (cx-1, cy), (cx-2, cy)]
        self.direction = RIGHT
        self.color     = color
        self.shield    = False

    def head(self):
        return self.body[0]

    def set_direction(self, d):
        if d != OPPOSITES.get(self.direction):
            self.direction = d

    def move(self, grow=False):
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def shrink(self, n=2):
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()

    def cells(self):
        return set(self.body)

    def draw(self, surf, grid_on):
        for i, (c, r) in enumerate(self.body):
            x, y = cell_to_px(c, r)
            color = self.color if i > 0 else C_SNAKE_HEAD
            rect  = pygame.Rect(x+1, y+1, CELL_SIZE-2, CELL_SIZE-2)
            pygame.draw.rect(surf, color, rect, border_radius=4 if i==0 else 2)
        if self.shield:
            hx, hy = cell_to_px(*self.head())
            pygame.draw.rect(surf, C_PU_SHIELD,
                             (hx, hy, CELL_SIZE, CELL_SIZE), 2, border_radius=4)


# ─── Obstacle block ───────────────────────────────────────────────────────────
class Obstacle:
    def __init__(self, pos):
        self.pos = pos

    def draw(self, surf, grid_on):
        x, y = cell_to_px(*self.pos)
        pygame.draw.rect(surf, C_OBSTACLE,
                         (x+1, y+1, CELL_SIZE-2, CELL_SIZE-2), border_radius=2)
        pygame.draw.rect(surf, (60, 30, 5),
                         (x+1, y+1, CELL_SIZE-2, CELL_SIZE-2), 1, border_radius=2)


# ─── Main Game ────────────────────────────────────────────────────────────────
class SnakeGame:
    def __init__(self, screen, settings, username, personal_best=0):
        self.screen        = screen
        self.settings      = settings
        self.username      = username
        self.personal_best = personal_best

        self.snake    = Snake(tuple(settings.get("snake_color", [80,220,80])))
        self.foods    : list[Food]    = []
        self.poison   : list[PoisonFood] = []
        self.powerups : list[PowerUp] = []
        self.obstacles: list[Obstacle] = []

        self.score      = 0
        self.level      = 1
        self.foods_eaten = 0   # normal food counter for level-up

        # Active power-up
        self.active_pu      = None
        self.pu_end_time    = 0

        # Timers
        now = pygame.time.get_ticks()
        self.next_food_time   = now
        self.next_poison_time = now + 4000
        self.next_pu_time     = now + 6000
        self.move_timer       = 0.0

        self.game_over = False
        self.paused    = False

        self.font_sm = pygame.font.SysFont(None, 24)
        self.font_md = pygame.font.SysFont(None, 34)
        self.font_lg = pygame.font.SysFont(None, 54)

        # Spawn initial food
        self._spawn_food()

    # ── Speed ─────────────────────────────────────────────────────────────────
    def _move_interval(self):
        speed = BASE_SPEED + (self.level - 1) * 1.5
        if self.active_pu == "speed":
            speed *= 1.6
        elif self.active_pu == "slow":
            speed *= 0.55
        return 1.0 / speed

    # ── Blocked cells ─────────────────────────────────────────────────────────
    def _blocked(self):
        s = self.snake.cells()
        s |= {o.pos for o in self.obstacles}
        return s

    # ── Spawn helpers ─────────────────────────────────────────────────────────
    def _spawn_food(self):
        if len(self.foods) < 2:
            pos = random_cell(self._blocked() |
                              {f.pos for f in self.foods} |
                              {p.pos for p in self.poison})
            self.foods.append(Food(pos))

    def _spawn_poison(self):
        blocked = (self._blocked() |
                   {f.pos for f in self.foods} |
                   {p.pos for p in self.poison})
        pos = random_cell(blocked)
        self.poison.append(PoisonFood(pos))

    def _spawn_powerup(self):
        if not self.powerups:
            blocked = (self._blocked() |
                       {f.pos for f in self.foods} |
                       {p.pos for p in self.poison})
            pos = random_cell(blocked)
            self.powerups.append(PowerUp(pos))

    def _spawn_obstacles(self):
        """Place obstacle blocks for the new level. Ensure snake head stays reachable."""
        count = 4 + (self.level - 3) * 2
        count = min(count, 20)
        head  = self.snake.head()
        blocked = self._blocked() | {f.pos for f in self.foods}
        added = 0
        attempts = 0
        while added < count and attempts < 300:
            attempts += 1
            pos = random_cell(blocked)
            # Don't place within 3 cells of snake head (Manhattan)
            if abs(pos[0]-head[0]) + abs(pos[1]-head[1]) < 4:
                continue
            self.obstacles.append(Obstacle(pos))
            blocked.add(pos)
            added += 1

    # ── Level up ──────────────────────────────────────────────────────────────
    def _level_up(self):
        self.level += 1
        self.foods_eaten = 0
        if self.level >= 3:
            self._spawn_obstacles()

    # ── Power-up activation ───────────────────────────────────────────────────
    def _activate_pu(self, pu: PowerUp):
        now = pygame.time.get_ticks()
        if pu.kind == "shield":
            self.snake.shield = True
            self.active_pu    = "shield"
            self.pu_end_time  = now + 99_999_999
        else:
            self.active_pu   = pu.kind
            self.pu_end_time = now + PowerUp.TYPES[pu.kind]["duration"]

    def _check_pu_expiry(self):
        if self.active_pu and pygame.time.get_ticks() > self.pu_end_time:
            if self.active_pu == "shield":
                self.snake.shield = False
            self.active_pu = None

    # ── Input ─────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.snake.set_direction(UP)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.snake.set_direction(DOWN)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.snake.set_direction(LEFT)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.snake.set_direction(RIGHT)
            elif event.key == pygame.K_p:
                self.paused = not self.paused

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self, dt):
        if self.game_over or self.paused:
            return

        now = pygame.time.get_ticks()
        self._check_pu_expiry()

        # Spawn timers
        if now > self.next_food_time:
            self._spawn_food()
            self.next_food_time = now + 1500

        if now > self.next_poison_time:
            self._spawn_poison()
            self.next_poison_time = now + random.randint(5000, 9000)

        if now > self.next_pu_time:
            self._spawn_powerup()
            self.next_pu_time = now + random.randint(8000, 14000)

        # Expire foods / poison / power-ups
        self.foods   = [f for f in self.foods   if not f.expired()]
        self.poison  = [p for p in self.poison  if not p.expired()]
        self.powerups= [p for p in self.powerups if not p.expired()]

        # Move snake
        self.move_timer += dt
        if self.move_timer >= self._move_interval():
            self.move_timer = 0.0
            self._step()

    def _step(self):
        self.snake.move(grow=False)
        head = self.snake.head()

        # Wall collision
        hx, hy = head
        if not (0 <= hx < COLS and 0 <= hy < ROWS):
            self._die()
            return

        # Self collision
        if head in set(self.snake.body[1:]):
            self._die()
            return

        # Obstacle collision
        if any(o.pos == head for o in self.obstacles):
            self._die()
            return

        # Food
        for food in self.foods[:]:
            if food.pos == head:
                self.snake.move(grow=True)
                self.snake.body.pop(0)  # undo the extra grow from move()
                # Actually just grow properly:
                # Re-do: grow=True already inserts head and skips pop
                self.score += food.points * self.level
                if not food.poison:
                    self.foods_eaten += 1
                self.foods.remove(food)
                if self.foods_eaten >= FOODS_PER_LEVEL:
                    self._level_up()
                self._spawn_food()
                return

        # Poison food
        for pf in self.poison[:]:
            if pf.pos == head:
                self.snake.move(grow=True)
                self.snake.body.pop(0)
                self.poison.remove(pf)
                self.snake.shrink(2)
                if len(self.snake.body) <= 1:
                    self._die()
                return

        # Power-up
        for pu in self.powerups[:]:
            if pu.pos == head:
                self._activate_pu(pu)
                self.powerups.remove(pu)
                break

    def _die(self):
        if self.snake.shield:
            self.snake.shield = False
            self.active_pu = None
            return
        self.game_over = True

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self):
        s = self.screen
        s.fill(C_BG)

        grid_on = self.settings.get("grid_overlay", True)

        # Grid
        if grid_on:
            for c in range(COLS + 1):
                x = GRID_X + c * CELL_SIZE
                pygame.draw.line(s, C_GRID, (x, GRID_Y), (x, GRID_Y + ROWS*CELL_SIZE))
            for r in range(ROWS + 1):
                y = GRID_Y + r * CELL_SIZE
                pygame.draw.line(s, C_GRID, (GRID_X, y), (GRID_X + COLS*CELL_SIZE, y))

        # Border
        border = pygame.Rect(GRID_X-2, GRID_Y-2,
                             COLS*CELL_SIZE+4, ROWS*CELL_SIZE+4)
        pygame.draw.rect(s, C_BORDER, border, 2)

        for o  in self.obstacles: o.draw(s, grid_on)
        for f  in self.foods:     f.draw(s, grid_on)
        for pf in self.poison:    pf.draw(s, grid_on)
        for pu in self.powerups:  pu.draw(s, grid_on)
        self.snake.draw(s, grid_on)

        self._draw_hud()

        if self.paused:
            self._draw_overlay("PAUSED", C_TITLE)

    def _draw_hud(self):
        s = self.screen
        now = pygame.time.get_ticks()

        pygame.draw.rect(s, (20,20,30), (0, 0, SCREEN_W, GRID_Y-2))

        def txt(text, x, y, font=None, color=C_HUD):
            f = font or self.font_sm
            surf = f.render(text, True, color)
            s.blit(surf, (x, y))

        txt(f"Score: {self.score}",  8,   8, self.font_md)
        txt(f"Level: {self.level}",  8,  38, self.font_sm)
        txt(f"PB: {self.personal_best}", 160, 8,  self.font_sm, C_GRAY)
        txt(f"Foods: {self.foods_eaten}/{FOODS_PER_LEVEL}", 160, 28, self.font_sm)
        txt(self.username, SCREEN_W-130, 8, self.font_sm)
        txt(f"Len: {len(self.snake.body)}", SCREEN_W-130, 28, self.font_sm, C_GRAY)

        # Active power-up
        if self.active_pu:
            remain = max(0, self.pu_end_time - now) / 1000
            colors = {"speed": C_PU_SPEED, "slow": C_PU_SLOW, "shield": C_PU_SHIELD}
            c = colors.get(self.active_pu, C_WHITE)
            label = self.active_pu.upper()
            if self.active_pu == "shield":
                txt(f"[{label}]", SCREEN_W//2-30, 12, color=c)
            else:
                txt(f"[{label} {remain:.1f}s]", SCREEN_W//2-50, 12, color=c)

    def _draw_overlay(self, text, color):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))
        t = self.font_lg.render(text, True, color)
        self.screen.blit(t, t.get_rect(center=(SCREEN_W//2, SCREEN_H//2)))
