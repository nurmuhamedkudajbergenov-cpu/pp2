import pygame
import sys
from config import *
from game import SnakeGame
from db import init_db, save_session, get_top10, get_personal_best
from settings_manager import load_settings, save_settings

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake Game — TSIS 4")
clock  = pygame.time.Clock()

font_sm = pygame.font.SysFont(None, 26)
font_md = pygame.font.SysFont(None, 36)
font_lg = pygame.font.SysFont(None, 58)
font_xl = pygame.font.SysFont(None, 80)

db_ok    = init_db()
settings = load_settings()


def draw_bg():
    screen.fill(C_BG)
    for i in range(0, SCREEN_W, 40):
        pygame.draw.line(screen, (22, 22, 32), (i, 0), (i, SCREEN_H))
    for j in range(0, SCREEN_H, 40):
        pygame.draw.line(screen, (22, 22, 32), (0, j), (SCREEN_W, j))


class Button:
    def __init__(self, rect, label, color=C_BTN, hover=C_BTN_H):
        self.rect  = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.hover = hover

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        c = self.hover if self.rect.collidepoint(mx, my) else self.color
        pygame.draw.rect(screen, c, self.rect, border_radius=10)
        pygame.draw.rect(screen, C_WHITE, self.rect, 2, border_radius=10)
        t = font_md.render(self.label, True, C_WHITE)
        screen.blit(t, t.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                and self.rect.collidepoint(event.pos))


def center_x(w):
    return SCREEN_W // 2 - w // 2



def screen_main_menu():
    btn_play = Button((center_x(220), 260, 220, 52), "▶  Play")
    btn_lb   = Button((center_x(220), 326, 220, 52), "🏆  Leaderboard")
    btn_set  = Button((center_x(220), 392, 220, 52), "⚙  Settings")
    btn_quit = Button((center_x(220), 458, 220, 52), "✕  Quit", C_RED, (200,30,30))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_play.clicked(event):  return "username"
            if btn_lb.clicked(event):    return "leaderboard"
            if btn_set.clicked(event):   return "settings"
            if btn_quit.clicked(event):  pygame.quit(); sys.exit()

        draw_bg()
        t = font_xl.render("SNAKE", True, C_TITLE)
        screen.blit(t, t.get_rect(center=(SCREEN_W//2, 140)))
        sub = font_md.render("TSIS 4", True, C_GRAY)
        screen.blit(sub, sub.get_rect(center=(SCREEN_W//2, 210)))
        if not db_ok:
            warn = font_sm.render("⚠ DB offline — scores not saved", True, C_RED)
            screen.blit(warn, warn.get_rect(center=(SCREEN_W//2, SCREEN_H-30)))

        for b in (btn_play, btn_lb, btn_set, btn_quit):
            b.draw()
        pygame.display.flip()


def screen_username():
    username = ""
    error    = ""
    btn_ok   = Button((center_x(180), 370, 180, 50), "Start")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key == pygame.K_RETURN:
                    if username.strip():
                        return username.strip()
                    error = "Enter a username!"
                elif len(username) < 16 and event.unicode.isprintable():
                    username += event.unicode
            if btn_ok.clicked(event):
                if username.strip():
                    return username.strip()
                error = "Enter a username!"

        draw_bg()
        t = font_lg.render("Enter Username", True, C_TITLE)
        screen.blit(t, t.get_rect(center=(SCREEN_W//2, 180)))

        box = pygame.Rect(center_x(300), 280, 300, 52)
        pygame.draw.rect(screen, (35, 35, 55), box, border_radius=8)
        pygame.draw.rect(screen, C_WHITE, box, 2, border_radius=8)
        ut = font_md.render(username + "|", True, C_WHITE)
        screen.blit(ut, ut.get_rect(center=box.center))

        if error:
            et = font_sm.render(error, True, C_RED)
            screen.blit(et, et.get_rect(center=(SCREEN_W//2, 344)))

        btn_ok.draw()
        pygame.display.flip()


def screen_play(username):
    pb   = get_personal_best(username) if db_ok else 0
    game = SnakeGame(screen, settings, username, personal_best=pb)

    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None, None
            game.handle_event(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

        if game.game_over:
            pygame.time.delay(600)
            if db_ok:
                save_session(username, game.score, game.level)
            return game.score, game.level


def screen_game_over(username, score, level):
    pb = get_personal_best(username) if db_ok else score
    is_pb = score >= pb

    btn_retry = Button((center_x(240), 430, 240, 52), "▶  Play Again")
    btn_menu  = Button((center_x(240), 496, 240, 52), "⌂  Main Menu")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_retry.clicked(event): return "retry"
            if btn_menu.clicked(event):  return "menu"

        draw_bg()
        t = font_xl.render("GAME OVER", True, C_RED)
        screen.blit(t, t.get_rect(center=(SCREEN_W//2, 120)))

        rows = [
            ("Score",         str(score),  C_WHITE),
            ("Level Reached", str(level),  C_WHITE),
            ("Personal Best", str(pb),     C_TITLE if is_pb else C_WHITE),
        ]
        for i, (label, value, vc) in enumerate(rows):
            y = 210 + i * 60
            lt = font_md.render(label + ":", True, C_GRAY)
            vt = font_md.render(value, True, vc)
            screen.blit(lt, (center_x(300), y))
            screen.blit(vt, (center_x(300) + 220, y))

        if is_pb:
            pb_t = font_sm.render("🎉 New Personal Best!", True, C_TITLE)
            screen.blit(pb_t, pb_t.get_rect(center=(SCREEN_W//2, 395)))

        btn_retry.draw()
        btn_menu.draw()
        pygame.display.flip()


def screen_leaderboard():
    top10    = get_top10() if db_ok else []
    btn_back = Button((center_x(180), SCREEN_H-70, 180, 46), "← Back")

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_back.clicked(event): return

        draw_bg()
        t = font_lg.render("🏆 Leaderboard", True, C_TITLE)
        screen.blit(t, t.get_rect(center=(SCREEN_W//2, 50)))

        if not db_ok:
            wt = font_sm.render("Database offline", True, C_RED)
            screen.blit(wt, wt.get_rect(center=(SCREEN_W//2, 110)))
        elif not top10:
            nt = font_sm.render("No scores yet — play first!", True, C_GRAY)
            screen.blit(nt, nt.get_rect(center=(SCREEN_W//2, 200)))
        else:
            headers = [("#", 30), ("Username", 80), ("Score", 280), ("Level", 390), ("Date", 460)]
            hy = 95
            for h, x in headers:
                ht = font_sm.render(h, True, C_TITLE)
                screen.blit(ht, (x, hy))
            pygame.draw.line(screen, C_GRAY, (20, hy+22), (SCREEN_W-20, hy+22))

            for i, row in enumerate(top10):
                y = 128 + i * 44
                color = (255,215,0) if i==0 else (200,200,200) if i==1 else C_WHITE
                cells = [
                    (str(i+1),                           30),
                    (row.get("username","?")[:12],       80),
                    (str(row.get("score",0)),            280),
                    (str(row.get("level_reached","?")),  390),
                    (str(row.get("date","?")),           460),
                ]
                for text, x in cells:
                    ct = font_sm.render(text, True, color)
                    screen.blit(ct, (x, y))

        btn_back.draw()
        pygame.display.flip()


def screen_settings():
    global settings
    s          = dict(settings)
    sound_on   = s.get("sound", True)
    grid_on    = s.get("grid_overlay", True)
    snake_color= list(s.get("snake_color", [80, 220, 80]))

    colors = {
        "Green":  [80,  220,  80],
        "Red":    [255,  60,  60],
        "Blue":   [60,  120, 255],
        "Yellow": [255, 220,   0],
        "Purple": [180,  60, 220],
        "Cyan":   [0,   210, 210],
        "White":  [240, 240, 240],
    }
    cnames  = list(colors.keys())
    col_idx = next((i for i,v in enumerate(colors.values()) if v==snake_color), 0)

    btn_sound  = Button((center_x(220), 175, 220, 46), "")
    btn_grid   = Button((center_x(220), 235, 220, 46), "")
    btn_cl     = Button((center_x(220)-80, 305, 46, 46), "<")
    btn_cr     = Button((center_x(220)+160, 305, 46, 46), ">")
    btn_save   = Button((center_x(220), 430, 220, 52), "✓ Save & Back", C_GREEN, (50,160,50))

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if btn_sound.clicked(event): sound_on = not sound_on
            if btn_grid.clicked(event):  grid_on  = not grid_on
            if btn_cl.clicked(event):    col_idx  = (col_idx-1) % len(cnames)
            if btn_cr.clicked(event):    col_idx  = (col_idx+1) % len(cnames)
            if btn_save.clicked(event):
                s["sound"]        = sound_on
                s["grid_overlay"] = grid_on
                s["snake_color"]  = colors[cnames[col_idx]]
                save_settings(s)
                settings = s
                return

        draw_bg()
        t = font_lg.render("Settings", True, C_TITLE)
        screen.blit(t, t.get_rect(center=(SCREEN_W//2, 90)))

        # Sound
        btn_sound.label = f"Sound: {'ON  ✓' if sound_on else 'OFF ✗'}"
        btn_sound.color = C_GREEN if sound_on else C_RED
        btn_sound.draw()

        # Grid
        btn_grid.label = f"Grid: {'ON  ✓' if grid_on else 'OFF ✗'}"
        btn_grid.color = C_GREEN if grid_on else C_RED
        btn_grid.draw()

        # Snake color
        cl = font_md.render("Snake Color:", True, C_GRAY)
        screen.blit(cl, (center_x(220), 275))
        cur = colors[cnames[col_idx]]
        pygame.draw.rect(screen, cur, (center_x(220)+10, 305, 130, 46), border_radius=8)
        cn = font_sm.render(cnames[col_idx], True, C_WHITE)
        screen.blit(cn, cn.get_rect(center=(center_x(220)+75, 328)))
        btn_cl.draw(); btn_cr.draw()

        btn_save.draw()
        pygame.display.flip()


# ─── State Machine ────────────────────────────────────────────────────────────
def main():
    username = "Player"
    state    = "menu"

    while True:
        if state == "menu":
            state = screen_main_menu()

        elif state == "username":
            username = screen_username()
            state    = "play"

        elif state == "play":
            result = screen_play(username)
            score, level = result
            if score is None:
                state = "menu"
            else:
                state = screen_game_over(username, score, level)
                if state == "retry":
                    state = "play"
                else:
                    state = "menu"

        elif state == "leaderboard":
            screen_leaderboard()
            state = "menu"

        elif state == "settings":
            screen_settings()
            state = "menu"


if __name__ == "__main__":
    main()
