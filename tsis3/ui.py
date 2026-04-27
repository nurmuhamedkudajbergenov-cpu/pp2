import pygame
import sys
from game_states import GameStates
from racer import RacerGame, SCREEN_W, SCREEN_H

# ─── Colors ───────────────────────────────────────────────────────────────────
C_BG      = (15,  15,  25)
C_BTN     = (50,  50,  80)
C_BTN_H   = (80,  80, 140)
C_BTN_T   = (240, 240, 240)
C_TITLE   = (255, 200,  60)
C_WHITE   = (240, 240, 240)
C_GRAY    = (160, 160, 160)
C_GREEN   = (80,  200,  80)
C_RED     = (220,  60,  60)


def draw_bg(surf):
    surf.fill(C_BG)
    for i in range(0, SCREEN_W, 40):
        pygame.draw.line(surf, (25,25,40), (i, 0), (i, SCREEN_H))
    for j in range(0, SCREEN_H, 40):
        pygame.draw.line(surf, (25,25,40), (0, j), (SCREEN_W, j))


class Button:
    def __init__(self, rect, label, color=C_BTN, hover=C_BTN_H):
        self.rect   = pygame.Rect(rect)
        self.label  = label
        self.color  = color
        self.hover  = hover
        self.font   = pygame.font.SysFont(None, 34)

    def draw(self, surf):
        mx, my = pygame.mouse.get_pos()
        c = self.hover if self.rect.collidepoint(mx, my) else self.color
        pygame.draw.rect(surf, c, self.rect, border_radius=10)
        pygame.draw.rect(surf, C_WHITE, self.rect, 2, border_radius=10)
        t = self.font.render(self.label, True, C_BTN_T)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos))


# ─── UI Manager ───────────────────────────────────────────────────────────────
class UI:
    def __init__(self, screen, settings, leaderboard):
        self.screen      = screen
        self.settings    = settings
        self.leaderboard = leaderboard
        self.last_result = (0, 0, 0)
        self.clock       = pygame.time.Clock()

        self.font_sm = pygame.font.SysFont(None, 26)
        self.font_md = pygame.font.SysFont(None, 36)
        self.font_lg = pygame.font.SysFont(None, 60)
        self.font_xl = pygame.font.SysFont(None, 80)

    # ── Dispatcher ────────────────────────────────────────────────────────────
    def run_state(self, state, username):
        if state == GameStates.MAIN_MENU:
            return self._main_menu()
        elif state == GameStates.SET_USERNAME:
            result = self._username_screen()
            return result
        elif state == GameStates.PLAYING:
            return self._play(username)
        elif state == GameStates.GAME_OVER:
            return self._game_over_screen(username)
        elif state == GameStates.LEADERBOARD:
            return self._leaderboard_screen()
        elif state == GameStates.SETTINGS:
            return self._settings_screen()
        return None

    # ── Main Menu ─────────────────────────────────────────────────────────────
    def _main_menu(self):
        btn_play  = Button((SCREEN_W//2-110, 260, 220, 52), "▶  Play")
        btn_lb    = Button((SCREEN_W//2-110, 330, 220, 52), "🏆  Leaderboard")
        btn_set   = Button((SCREEN_W//2-110, 400, 220, 52), "⚙  Settings")
        btn_quit  = Button((SCREEN_W//2-110, 470, 220, 52), "✕  Quit", C_RED)

        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (GameStates.QUIT, None)
                if btn_play.clicked(event):
                    return (GameStates.SET_USERNAME, None)
                if btn_lb.clicked(event):
                    return (GameStates.LEADERBOARD, None)
                if btn_set.clicked(event):
                    return (GameStates.SETTINGS, None)
                if btn_quit.clicked(event):
                    return (GameStates.QUIT, None)

            draw_bg(self.screen)
            t = self.font_xl.render("RACER", True, C_TITLE)
            self.screen.blit(t, t.get_rect(center=(SCREEN_W//2, 140)))
            sub = self.font_md.render("TSIS 3", True, C_GRAY)
            self.screen.blit(sub, sub.get_rect(center=(SCREEN_W//2, 210)))

            for btn in (btn_play, btn_lb, btn_set, btn_quit):
                btn.draw(self.screen)

            pygame.display.flip()

    # ── Username entry ────────────────────────────────────────────────────────
    def _username_screen(self):
        username = ""
        btn_ok = Button((SCREEN_W//2-90, 370, 180, 50), "Start Race")
        error  = ""

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (GameStates.QUIT, None)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if username.strip():
                            return (GameStates.SET_USERNAME, username.strip())
                        else:
                            error = "Please enter a name!"
                    elif len(username) < 16 and event.unicode.isprintable():
                        username += event.unicode
                if btn_ok.clicked(event):
                    if username.strip():
                        return (GameStates.SET_USERNAME, username.strip())
                    else:
                        error = "Please enter a name!"

            draw_bg(self.screen)
            t = self.font_lg.render("Enter Username", True, C_TITLE)
            self.screen.blit(t, t.get_rect(center=(SCREEN_W//2, 180)))

            # Input box
            box = pygame.Rect(SCREEN_W//2-150, 280, 300, 52)
            pygame.draw.rect(self.screen, (40,40,60), box, border_radius=8)
            pygame.draw.rect(self.screen, C_WHITE, box, 2, border_radius=8)
            ut = self.font_md.render(username + "|", True, C_WHITE)
            self.screen.blit(ut, ut.get_rect(center=box.center))

            if error:
                et = self.font_sm.render(error, True, C_RED)
                self.screen.blit(et, et.get_rect(center=(SCREEN_W//2, 345)))

            btn_ok.draw(self.screen)
            pygame.display.flip()

    # ── Playing ───────────────────────────────────────────────────────────────
    def _play(self, username):
        game = RacerGame(self.screen, self.settings, username)

        while True:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (GameStates.QUIT, None)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return (GameStates.MAIN_MENU, None)
                game.handle_event(event)

            game.update(dt)
            game.draw()
            pygame.display.flip()

            if game.game_over:
                # Brief pause
                pygame.time.delay(800)
                return (GameStates.GAME_OVER,
                        (game.score, int(game.distance), game.coin_count))

    # ── Game Over ─────────────────────────────────────────────────────────────
    def _game_over_screen(self, username):
        score, distance, coins = self.last_result
        finished = distance >= 3000

        btn_retry = Button((SCREEN_W//2-120, 460, 240, 52), "▶  Play Again")
        btn_menu  = Button((SCREEN_W//2-120, 525, 240, 52), "⌂  Main Menu")

        # Personal best
        pb = max((e["score"] for e in self.leaderboard
                  if e.get("name") == username), default=0)

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (GameStates.QUIT, None)
                if btn_retry.clicked(event):
                    return (GameStates.SET_USERNAME, None)
                if btn_menu.clicked(event):
                    return (GameStates.MAIN_MENU, None)

            draw_bg(self.screen)

            title_text = "FINISH!" if finished else "GAME OVER"
            title_color = C_GREEN if finished else C_RED
            t = self.font_xl.render(title_text, True, title_color)
            self.screen.blit(t, t.get_rect(center=(SCREEN_W//2, 140)))

            rows = [
                ("Score",    str(score)),
                ("Distance", f"{distance} / 3000"),
                ("Coins",    str(coins)),
                ("Personal Best", str(pb)),
            ]
            for i, (label, value) in enumerate(rows):
                y = 230 + i * 46
                lt = self.font_md.render(label + ":", True, C_GRAY)
                vt = self.font_md.render(value,       True, C_WHITE)
                self.screen.blit(lt, (SCREEN_W//2 - 180, y))
                self.screen.blit(vt, (SCREEN_W//2 + 20,  y))

            btn_retry.draw(self.screen)
            btn_menu.draw(self.screen)
            pygame.display.flip()

    # ── Leaderboard ───────────────────────────────────────────────────────────
    def _leaderboard_screen(self):
        btn_back = Button((SCREEN_W//2-90, 620, 180, 46), "← Back")

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (GameStates.QUIT, None)
                if btn_back.clicked(event):
                    return (GameStates.MAIN_MENU, None)

            draw_bg(self.screen)
            t = self.font_lg.render("🏆 Top 10", True, C_TITLE)
            self.screen.blit(t, t.get_rect(center=(SCREEN_W//2, 60)))

            # Header
            hdr_y = 110
            for text, x in [("#", 50), ("Name", 110), ("Score", 270),
                             ("Dist", 360), ("Coins", 430)]:
                ht = self.font_sm.render(text, True, C_TITLE)
                self.screen.blit(ht, (x, hdr_y))
            pygame.draw.line(self.screen, C_GRAY,
                             (30, hdr_y+24), (SCREEN_W-30, hdr_y+24))

            for i, entry in enumerate(self.leaderboard[:10]):
                y = 145 + i * 45
                color = (255,215,0) if i == 0 else (200,200,200) if i==1 else C_WHITE
                cells = [
                    (str(i+1),              50),
                    (entry.get("name","?")[:10], 110),
                    (str(entry.get("score",0)), 270),
                    (str(entry.get("distance",0)), 360),
                    (str(entry.get("coins",0)),  430),
                ]
                for text, x in cells:
                    ct = self.font_sm.render(text, True, color)
                    self.screen.blit(ct, (x, y))

            btn_back.draw(self.screen)
            pygame.display.flip()

    # ── Settings ──────────────────────────────────────────────────────────────
    def _settings_screen(self):
        s = dict(self.settings)
        sound_on   = s.get("sound", True)
        difficulty = s.get("difficulty", "medium")
        car_color  = list(s.get("car_color", [255,50,50]))

        difficulties = ["easy", "medium", "hard"]
        colors = {
            "Red":    [255, 50,  50],
            "Blue":   [50,  100, 255],
            "Green":  [50,  200, 80],
            "Yellow": [255, 220, 0],
            "Purple": [180, 60,  220],
            "White":  [240, 240, 240],
        }
        color_names = list(colors.keys())
        sel_color_name = next(
            (k for k, v in colors.items() if v == car_color), "Red")

        btn_sound  = Button((SCREEN_W//2-110, 200, 220, 46), "")
        btn_diff_l = Button((SCREEN_W//2-160, 270, 46, 46), "<")
        btn_diff_r = Button((SCREEN_W//2+114, 270, 46, 46), ">")
        btn_col_l  = Button((SCREEN_W//2-160, 340, 46, 46), "<")
        btn_col_r  = Button((SCREEN_W//2+114, 340, 46, 46), ">")
        btn_save   = Button((SCREEN_W//2-110, 450, 220, 52), "✓ Save & Back", C_GREEN)

        col_idx = color_names.index(sel_color_name)

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return (GameStates.QUIT, None)

                if btn_sound.clicked(event):
                    sound_on = not sound_on

                if btn_diff_l.clicked(event):
                    difficulty = difficulties[(difficulties.index(difficulty)-1) % 3]
                if btn_diff_r.clicked(event):
                    difficulty = difficulties[(difficulties.index(difficulty)+1) % 3]

                if btn_col_l.clicked(event):
                    col_idx = (col_idx - 1) % len(color_names)
                if btn_col_r.clicked(event):
                    col_idx = (col_idx + 1) % len(color_names)

                if btn_save.clicked(event):
                    s["sound"]      = sound_on
                    s["difficulty"] = difficulty
                    s["car_color"]  = colors[color_names[col_idx]]
                    return (GameStates.SETTINGS_SAVED, s)

            draw_bg(self.screen)
            t = self.font_lg.render("Settings", True, C_TITLE)
            self.screen.blit(t, t.get_rect(center=(SCREEN_W//2, 110)))

            # Sound toggle
            btn_sound.label = f"Sound: {'ON ✓' if sound_on else 'OFF ✗'}"
            btn_sound.color = C_GREEN if sound_on else C_RED
            btn_sound.draw(self.screen)

            # Difficulty
            dl = self.font_md.render("Difficulty:", True, C_GRAY)
            self.screen.blit(dl, (SCREEN_W//2-108, 278))
            dv = self.font_md.render(difficulty.capitalize(), True, C_WHITE)
            self.screen.blit(dv, dv.get_rect(center=(SCREEN_W//2+30, 293)))
            btn_diff_l.draw(self.screen)
            btn_diff_r.draw(self.screen)

            # Car color
            cl_label = self.font_md.render("Car Color:", True, C_GRAY)
            self.screen.blit(cl_label, (SCREEN_W//2-108, 348))
            cur_color = colors[color_names[col_idx]]
            pygame.draw.rect(self.screen, cur_color,
                             (SCREEN_W//2+10, 342, 60, 30), border_radius=6)
            cn = self.font_sm.render(color_names[col_idx], True, C_WHITE)
            self.screen.blit(cn, (SCREEN_W//2+76, 350))
            btn_col_l.draw(self.screen)
            btn_col_r.draw(self.screen)

            btn_save.draw(self.screen)
            pygame.display.flip()
