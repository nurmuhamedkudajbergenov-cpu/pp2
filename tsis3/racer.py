import pygame
import random
import math

# ─── Constants ────────────────────────────────────────────────────────────────
SCREEN_W, SCREEN_H = 480, 700
LANE_COUNT   = 4
ROAD_LEFT    = 60
ROAD_RIGHT   = 420
ROAD_W       = ROAD_RIGHT - ROAD_LEFT
LANE_W       = ROAD_W // LANE_COUNT

CAR_W, CAR_H = 44, 80
FINISH_DIST  = 3000   # px of scrolled road = finish line

# Difficulty presets  { base_speed, traffic_interval, obstacle_interval }
DIFFICULTY = {
    "easy":   {"base_speed": 4,  "traffic_interval": 2200, "obstacle_interval": 2800},
    "medium": {"base_speed": 6,  "traffic_interval": 1600, "obstacle_interval": 2000},
    "hard":   {"base_speed": 9,  "traffic_interval": 1100, "obstacle_interval": 1400},
}

# Colors
C_BG       = (30,  30,  30)
C_ROAD     = (60,  60,  60)
C_LANE     = (220, 220, 100)
C_KERB     = (200, 200, 200)
C_COIN     = (255, 215,   0)
C_COIN2    = (180, 100,   0)  # weighted coin (dark gold)
C_COIN3    = (100, 200, 255)  # bonus coin
C_OBSTACLE = (100,  40,  10)
C_OIL      = (20,   20,  60)
C_NITRO    = (255, 140,   0)
C_SHIELD   = (100, 200, 255)
C_REPAIR   = (80,  200,  80)
C_TRAFFIC  = [(200,0,0),(0,150,200),(180,100,0),(150,0,200)]
C_HUD      = (240, 240, 240)
C_NITRO_STRIP = (255, 200, 0)
C_SPEED_BUMP  = (160, 80, 0)

# ─── Helper ───────────────────────────────────────────────────────────────────
def lane_x(lane: int) -> int:
    """Center x of a lane (0-based)."""
    return ROAD_LEFT + lane * LANE_W + LANE_W // 2

def lane_of(x: int) -> int:
    return max(0, min(LANE_COUNT - 1, (x - ROAD_LEFT) // LANE_W))


# ─── Game objects ─────────────────────────────────────────────────────────────
class PlayerCar:
    def __init__(self, color):
        self.lane   = 1
        self.x      = float(lane_x(self.lane))
        self.y      = float(SCREEN_H - 140)
        self.color  = color
        self.shield = False
        self.rect   = pygame.Rect(0, 0, CAR_W, CAR_H)
        self._update_rect()

    def _update_rect(self):
        self.rect.centerx = int(self.x)
        self.rect.centery  = int(self.y)

    def move(self, target_x: float, speed: float, dt: float):
        dx = target_x - self.x
        step = min(abs(dx), speed * 6 * dt)
        self.x += math.copysign(step, dx) if dx else 0
        self._update_rect()

    def draw(self, surf):
        r = self.rect
        # Body
        pygame.draw.rect(surf, self.color, r, border_radius=6)
        # Windshield
        ws = pygame.Rect(r.x+6, r.y+8, r.w-12, 18)
        pygame.draw.rect(surf, (180,230,255), ws, border_radius=3)
        # Wheels
        for wx, wy in [(r.x-4, r.y+8),(r.x-4, r.bottom-22),
                       (r.right-2, r.y+8),(r.right-2, r.bottom-22)]:
            pygame.draw.rect(surf, (20,20,20), (wx, wy, 8, 14), border_radius=2)
        if self.shield:
            pygame.draw.circle(surf, C_SHIELD,
                               r.center, max(r.w, r.h)//2+8, 3)


class Coin:
    TYPES = {
        "normal":   {"color": C_COIN,  "value": 1,  "weight": 60},
        "weighted": {"color": C_COIN2, "value": 3,  "weight": 30},
        "bonus":    {"color": C_COIN3, "value": 5,  "weight": 10},
    }
    def __init__(self, lane, y):
        kind = random.choices(list(self.TYPES.keys()),
                              weights=[v["weight"] for v in self.TYPES.values()])[0]
        self.kind  = kind
        self.color = self.TYPES[kind]["color"]
        self.value = self.TYPES[kind]["value"]
        self.x     = lane_x(lane)
        self.y     = float(y)
        self.radius = 12

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (self.x, int(self.y)), self.radius)
        pygame.draw.circle(surf, (255,255,255), (self.x, int(self.y)), self.radius, 2)
        if self.kind == "bonus":
            font = pygame.font.SysFont(None, 18)
            surf.blit(font.render(str(self.value), True, (0,0,0)),
                      (self.x-5, int(self.y)-7))


class Obstacle:
    TYPES = ["barrier","oil","pothole","speed_bump","nitro_strip"]
    def __init__(self, lane, y, otype=None):
        self.otype = otype or random.choice(["barrier","oil","pothole","speed_bump"])
        self.lane  = lane
        self.x     = lane_x(lane)
        self.y     = float(y)
        if self.otype == "nitro_strip":
            self.w, self.h = LANE_W - 4, 20
        elif self.otype == "oil":
            self.w, self.h = LANE_W - 6, 30
        else:
            self.w, self.h = LANE_W - 8, 24
        self.rect = pygame.Rect(self.x - self.w//2,
                                int(self.y) - self.h//2,
                                self.w, self.h)

    def update_rect(self):
        self.rect.centerx = int(self.x)
        self.rect.centery  = int(self.y)

    @property
    def color(self):
        return {
            "barrier":    C_OBSTACLE,
            "oil":        C_OIL,
            "pothole":    (40, 40, 40),
            "speed_bump": C_SPEED_BUMP,
            "nitro_strip":C_NITRO_STRIP,
        }.get(self.otype, C_OBSTACLE)

    def draw(self, surf):
        self.update_rect()
        pygame.draw.rect(surf, self.color, self.rect, border_radius=4)
        if self.otype == "nitro_strip":
            font = pygame.font.SysFont(None, 18)
            surf.blit(font.render("NITRO", True, (80,40,0)),
                      (self.rect.x+4, self.rect.y+3))
        elif self.otype == "oil":
            pygame.draw.ellipse(surf, (0,0,80), self.rect)


class TrafficCar:
    def __init__(self, lane, y, speed):
        self.lane  = lane
        self.x     = float(lane_x(lane))
        self.y     = float(y)
        self.speed = speed
        self.color = random.choice(C_TRAFFIC)
        self.rect  = pygame.Rect(0, 0, CAR_W, CAR_H)
        self._update_rect()

    def _update_rect(self):
        self.rect.centerx = int(self.x)
        self.rect.centery  = int(self.y)

    def update(self, road_speed, dt):
        self.y += (road_speed + self.speed) * dt * 60
        self._update_rect()

    def draw(self, surf):
        r = self.rect
        pygame.draw.rect(surf, self.color, r, border_radius=6)
        ws = pygame.Rect(r.x+6, r.bottom-26, r.w-12, 18)
        pygame.draw.rect(surf, (180,230,255), ws, border_radius=3)
        for wx, wy in [(r.x-4, r.y+8),(r.x-4, r.bottom-22),
                       (r.right-2, r.y+8),(r.right-2, r.bottom-22)]:
            pygame.draw.rect(surf, (20,20,20), (wx, wy, 8, 14), border_radius=2)


class PowerUp:
    TYPES = {
        "nitro":  {"color": C_NITRO,  "label": "N", "duration": 4000},
        "shield": {"color": C_SHIELD, "label": "S", "duration": 0},
        "repair": {"color": C_REPAIR, "label": "R", "duration": 0},
    }
    TIMEOUT = 6000   # disappears after 6 s if not collected

    def __init__(self, lane, y):
        self.kind  = random.choice(list(self.TYPES.keys()))
        self.x     = lane_x(lane)
        self.y     = float(y)
        self.color = self.TYPES[self.kind]["color"]
        self.label = self.TYPES[self.kind]["label"]
        self.spawn_time = pygame.time.get_ticks()
        self.size  = 22
        self.rect  = pygame.Rect(self.x - self.size,
                                 int(self.y) - self.size,
                                 self.size*2, self.size*2)

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.TIMEOUT

    def update_rect(self):
        self.rect.centerx = int(self.x)
        self.rect.centery  = int(self.y)

    def draw(self, surf):
        self.update_rect()
        pygame.draw.circle(surf, self.color, (self.x, int(self.y)), self.size)
        pygame.draw.circle(surf, (255,255,255), (self.x, int(self.y)), self.size, 2)
        font = pygame.font.SysFont(None, 26)
        txt = font.render(self.label, True, (0,0,0))
        surf.blit(txt, txt.get_rect(center=(self.x, int(self.y))))


# ─── Road stripes ─────────────────────────────────────────────────────────────
class RoadStripes:
    def __init__(self):
        self.stripes = [{"y": float(i * 80)} for i in range(10)]

    def update(self, speed, dt):
        for s in self.stripes:
            s["y"] += speed * dt * 60
        self.stripes = [s for s in self.stripes if s["y"] < SCREEN_H + 40]
        while len(self.stripes) < 10:
            min_y = min(s["y"] for s in self.stripes)
            self.stripes.append({"y": min_y - 80})

    def draw(self, surf):
        for s in self.stripes:
            for lane in range(1, LANE_COUNT):
                x = ROAD_LEFT + lane * LANE_W
                pygame.draw.rect(surf, C_LANE,
                                 (x - 2, int(s["y"]), 4, 40))


# ─── Main Game ────────────────────────────────────────────────────────────────
class RacerGame:
    def __init__(self, screen, settings, username):
        self.screen   = screen
        self.settings = settings
        self.username = username

        diff = DIFFICULTY[settings.get("difficulty", "medium")]
        self.base_speed     = diff["base_speed"]
        self.road_speed     = float(self.base_speed)
        self.traffic_int    = diff["traffic_interval"]
        self.obstacle_int   = diff["obstacle_interval"]

        self.player = PlayerCar(tuple(settings.get("car_color", [255,50,50])))
        self.target_lane = self.player.lane

        self.coins     : list[Coin]      = []
        self.obstacles : list[Obstacle]  = []
        self.traffic   : list[TrafficCar]= []
        self.powerups  : list[PowerUp]   = []
        self.stripes   = RoadStripes()

        self.score    = 0
        self.distance = 0.0
        self.coin_count = 0

        # Active power-up state
        self.active_pu      = None   # "nitro" | "shield" | None
        self.pu_end_time    = 0
        self.nitro_active   = False

        # Timers
        now = pygame.time.get_ticks()
        self.next_coin_time     = now + 800
        self.next_obstacle_time = now + self.obstacle_int
        self.next_traffic_time  = now + self.traffic_int
        self.next_powerup_time  = now + 5000

        self.font_sm = pygame.font.SysFont(None, 26)
        self.font_md = pygame.font.SysFont(None, 36)
        self.font_lg = pygame.font.SysFont(None, 52)

        self.game_over  = False
        self.finished   = False
        self.crash_count = 0   # for repair tracking

        # Road kerb scroll
        self.kerb_offset = 0.0

        # lane hazard info (slow lanes)
        self.slow_lanes: set = set()
        self._randomize_slow_lanes()

    # ── Internal helpers ──────────────────────────────────────────────────────
    def _randomize_slow_lanes(self):
        """Mark 0-1 lanes as slow zones periodically."""
        self.slow_lanes = set(random.sample(range(LANE_COUNT),
                                            k=random.randint(0, 1)))

    def _occupied_xs(self):
        xs = {self.player.rect.centerx}
        for t in self.traffic:
            xs.add(t.rect.centerx)
        return xs

    def _free_lane(self, exclude=None):
        lanes = list(range(LANE_COUNT))
        if exclude is not None:
            lanes = [l for l in lanes if l != exclude]
        random.shuffle(lanes)
        player_lane = lane_of(int(self.player.x))
        safe = [l for l in lanes if abs(l - player_lane) >= 1]
        return safe[0] if safe else lanes[0]

    def _spawn_coin(self):
        lane = random.randint(0, LANE_COUNT - 1)
        self.coins.append(Coin(lane, -30))

    def _spawn_obstacle(self):
        lane = self._free_lane(exclude=lane_of(int(self.player.x)))
        # Occasionally spawn nitro strip as a road event
        otype = "nitro_strip" if random.random() < 0.12 else None
        if otype is None and lane in self.slow_lanes:
            otype = random.choice(["oil", "speed_bump"])
        self.obstacles.append(Obstacle(lane, -40, otype))

    def _spawn_traffic(self):
        lane = self._free_lane()
        spd  = self.road_speed * random.uniform(0.2, 0.5)
        self.traffic.append(TrafficCar(lane, -90, spd))

    def _spawn_powerup(self):
        if not self.powerups:
            lane = random.randint(0, LANE_COUNT - 1)
            self.powerups.append(PowerUp(lane, -40))

    # ── Update ────────────────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.target_lane > 0:
                self.target_lane -= 1
            elif event.key == pygame.K_RIGHT and self.target_lane < LANE_COUNT - 1:
                self.target_lane += 1

    def update(self, dt):
        if self.game_over or self.finished:
            return

        now = pygame.time.get_ticks()

        # Nitro / active power-up expiry
        if self.active_pu and now > self.pu_end_time:
            self._deactivate_powerup()

        # Difficulty scaling: speed up every 300 distance units
        scale = 1.0 + (self.distance / 300) * 0.08
        self.road_speed = min(self.base_speed * scale, self.base_speed * 2.5)
        actual_speed = self.road_speed * (1.8 if self.nitro_active else 1.0)

        # Move player towards target lane
        tx = float(lane_x(self.target_lane))
        self.player.move(tx, actual_speed, dt)

        # Slow lane penalty
        pl = lane_of(int(self.player.x))
        if pl in self.slow_lanes and not self.nitro_active:
            actual_speed *= 0.6

        self.distance += actual_speed * dt * 60 / 60
        self.score     = int(self.distance) + self.coin_count * 10

        self.stripes.update(actual_speed, dt)
        self.kerb_offset = (self.kerb_offset + actual_speed * dt * 60) % 40

        # Spawn events
        if now > self.next_coin_time:
            self._spawn_coin()
            self.next_coin_time = now + random.randint(500, 1200)

        if now > self.next_obstacle_time:
            self._spawn_obstacle()
            density = max(0.5, 1.0 - self.distance / 2000)
            self.next_obstacle_time = now + int(self.obstacle_int * density)

        if now > self.next_traffic_time:
            # Spawn 1-3 traffic cars based on difficulty scaling
            count = 1 + int(self.distance / 600)
            for _ in range(min(count, 3)):
                self._spawn_traffic()
            density = max(0.4, 1.0 - self.distance / 2500)
            self.next_traffic_time = now + int(self.traffic_int * density)

        if now > self.next_powerup_time:
            self._spawn_powerup()
            self.next_powerup_time = now + random.randint(7000, 12000)

        # Scroll everything
        for obj in self.coins + self.obstacles + self.traffic + self.powerups:
            obj.y += actual_speed * dt * 60

        # Cull off-screen
        self.coins     = [c for c in self.coins     if c.y < SCREEN_H + 50]
        self.obstacles = [o for o in self.obstacles if o.y < SCREEN_H + 50]
        self.traffic   = [t for t in self.traffic   if t.y < SCREEN_H + 150]
        self.powerups  = [p for p in self.powerups  if p.y < SCREEN_H + 50
                          and not p.expired()]

        # Collisions
        self._check_collisions()

        # Occasionally reshuffle slow lanes
        if int(self.distance) % 400 == 0 and int(self.distance) > 0:
            self._randomize_slow_lanes()

        # Finish
        if self.distance >= FINISH_DIST:
            self.finished  = True
            self.game_over = True

    def _check_collisions(self):
        pr = self.player.rect

        # Coins
        for coin in self.coins[:]:
            if abs(coin.x - pr.centerx) < CAR_W//2 + coin.radius and \
               abs(coin.y - pr.centery)  < CAR_H//2 + coin.radius:
                self.coin_count += coin.value
                self.score += coin.value * 10
                self.coins.remove(coin)

        # Power-ups
        for pu in self.powerups[:]:
            pu.update_rect()
            if pr.colliderect(pu.rect):
                self._activate_powerup(pu)
                self.powerups.remove(pu)

        # Obstacles
        for obs in self.obstacles[:]:
            obs.update_rect()
            if pr.colliderect(obs.rect):
                if obs.otype == "nitro_strip":
                    self.nitro_active = True
                    self.pu_end_time  = pygame.time.get_ticks() + 3000
                    self.obstacles.remove(obs)
                elif obs.otype in ("oil", "speed_bump"):
                    self.obstacles.remove(obs)
                    # slow effect handled via slow_lanes, just remove
                else:
                    self._handle_crash()
                    self.obstacles.remove(obs)

        # Traffic
        for car in self.traffic[:]:
            if pr.colliderect(car.rect):
                self._handle_crash()
                self.traffic.remove(car)

    def _activate_powerup(self, pu):
        now = pygame.time.get_ticks()
        if pu.kind == "nitro":
            self.nitro_active = True
            self.active_pu    = "nitro"
            self.pu_end_time  = now + PowerUp.TYPES["nitro"]["duration"]
        elif pu.kind == "shield":
            self.player.shield = True
            self.active_pu     = "shield"
            self.pu_end_time   = now + 99999
        elif pu.kind == "repair":
            # Restore: clear one crash penalty (give back distance bonus)
            self.score += 50
            self.crash_count = max(0, self.crash_count - 1)

    def _deactivate_powerup(self):
        if self.active_pu == "nitro":
            self.nitro_active = False
        elif self.active_pu == "shield":
            self.player.shield = False
        self.active_pu = None

    def _handle_crash(self):
        if self.player.shield:
            self.player.shield = False
            self.active_pu     = None
            return
        self.crash_count += 1
        self.game_over = True

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self):
        s = self.screen
        s.fill(C_BG)

        # Road
        pygame.draw.rect(s, C_ROAD, (ROAD_LEFT, 0, ROAD_W, SCREEN_H))

        # Kerb stripes (animated)
        kerb_colors = [(220,50,50),(255,255,255)]
        for i in range(-1, SCREEN_H//40 + 2):
            y = i*40 + int(self.kerb_offset) - 40
            c = kerb_colors[i % 2]
            pygame.draw.rect(s, c, (ROAD_LEFT-14, y, 14, 40))
            pygame.draw.rect(s, c, (ROAD_RIGHT,   y, 14, 40))

        # Slow lane tint
        for lane in self.slow_lanes:
            lx = ROAD_LEFT + lane * LANE_W
            surf = pygame.Surface((LANE_W, SCREEN_H), pygame.SRCALPHA)
            surf.fill((80, 0, 0, 40))
            s.blit(surf, (lx, 0))

        self.stripes.draw(s)

        for coin in self.coins:      coin.draw(s)
        for obs  in self.obstacles:  obs.draw(s)
        for car  in self.traffic:    car.draw(s)
        for pu   in self.powerups:   pu.draw(s)

        self.player.draw(s)

        self._draw_hud()

    def _draw_hud(self):
        s = self.screen
        now = pygame.time.get_ticks()

        # Top bar
        pygame.draw.rect(s, (20,20,20,200), (0, 0, SCREEN_W, 48))

        def txt(text, x, y, font=None, color=C_HUD):
            f = font or self.font_sm
            surf = f.render(text, True, color)
            s.blit(surf, (x, y))

        txt(f"Score: {self.score}",    8,  8, self.font_md)
        txt(f"Coins: {self.coin_count}", 210, 14)
        txt(f"Dist: {int(self.distance)}/{FINISH_DIST}", 330, 14)

        # Distance bar
        prog = min(self.distance / FINISH_DIST, 1.0)
        pygame.draw.rect(s, (80,80,80), (ROAD_LEFT, 52, ROAD_W, 8))
        pygame.draw.rect(s, (50,220,50), (ROAD_LEFT, 52, int(ROAD_W*prog), 8))

        # Active power-up HUD
        if self.active_pu:
            remain = max(0, self.pu_end_time - now) / 1000
            color  = PowerUp.TYPES.get(self.active_pu, {}).get("color", C_HUD)
            label  = self.active_pu.upper()
            pygame.draw.rect(s, color, (ROAD_LEFT, SCREEN_H-40, 140, 30), border_radius=6)
            txt(f"{label}  {remain:.1f}s", ROAD_LEFT+6, SCREEN_H-33,
                color=(0,0,0))

        # Slow lane warning
        pl = lane_of(int(self.player.x))
        if pl in self.slow_lanes:
            txt("⚠ SLOW ZONE", SCREEN_W//2 - 55, SCREEN_H//2 - 20,
                color=(255, 80, 80))

        # Username
        txt(self.username, SCREEN_W - 120, 14)
