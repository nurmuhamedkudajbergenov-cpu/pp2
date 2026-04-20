import pygame
from player import Player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Music Player")

clock = pygame.time.Clock()

playlist = [
    "music_player/music/track1.wav",
    "music_player/music/track2.wav"
]

current = 0
player = Player(playlist[current])

status = "Stopped"

font = pygame.font.SysFont(None, 30)
small_font = pygame.font.SysFont(None, 22)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                player.play_music()
                status = "Playing"

            if event.key == pygame.K_s:
                player.stop_music()
                status = "Stopped"

            if event.key == pygame.K_n:
                current = (current + 1) % len(playlist)
                player = Player(playlist[current])
                player.play_music()
                status = "Playing"

            if event.key == pygame.K_b:
                current = (current - 1) % len(playlist)
                player = Player(playlist[current])
                player.play_music()
                status = "Playing"

            if event.key == pygame.K_q:
                running = False
    screen.fill((25, 25, 25))

    title = font.render("Music Player", True, (255, 255, 255))
    screen.blit(title, (180, 30))

    track_name = playlist[current].split("/")[-1]

    track_text = small_font.render(
        f"Track: {track_name}",
        True,
        (200, 200, 200)
    )
    screen.blit(track_text, (50, 100))

    status_text = small_font.render(
        f"Status: {status}",
        True,
        (0, 255, 0) if status == "Playing" else (255, 80, 80)
    )
    screen.blit(status_text, (50, 140))

    controls = small_font.render(
        "P-Play | S-Stop | N-Next | B-Back | Q-Quit",
        True,
        (150, 150, 150)
    )
    screen.blit(controls, (50, 220))

    pygame.display.flip()

pygame.quit()