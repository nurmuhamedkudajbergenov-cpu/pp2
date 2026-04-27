import pygame
import sys
from game_states import GameStates
from ui import UI
from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard


def main():
    pygame.init()
    pygame.mixer.init()

    settings    = load_settings()
    leaderboard = load_leaderboard()

    SCREEN_W, SCREEN_H = 480, 700
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Racer Game — TSIS 3")

    ui       = UI(screen, settings, leaderboard)
    state    = GameStates.MAIN_MENU
    username = "Player"

    while True:
        result = ui.run_state(state, username)

        if result is None:
            pygame.quit()
            sys.exit()

        new_state, data = result

        if new_state == GameStates.QUIT:
            pygame.quit()
            sys.exit()

        elif new_state == GameStates.SETTINGS_SAVED:
            settings = data
            save_settings(settings)
            ui.settings = settings
            state = GameStates.MAIN_MENU

        elif new_state == GameStates.SET_USERNAME:
            # data is None  → go show username input screen
            # data is a str → username was just entered, start playing
            if data is not None:
                username = data
                state    = GameStates.PLAYING
            else:
                state = GameStates.SET_USERNAME

        elif new_state == GameStates.GAME_OVER:
            score, distance, coins = data
            entry = {
                "name":     username,
                "score":    score,
                "distance": distance,
                "coins":    coins,
            }
            leaderboard.append(entry)
            leaderboard.sort(key=lambda x: x["score"], reverse=True)
            leaderboard = leaderboard[:10]
            save_leaderboard(leaderboard)
            ui.leaderboard = leaderboard
            ui.last_result = (score, distance, coins)
            state = GameStates.GAME_OVER

        else:
            state = new_state


if __name__ == "__main__":
    main()
