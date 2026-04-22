import pygame
import os

pygame.init()
pygame.mixer.init()

# окно
WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

font = pygame.font.SysFont(None, 36)

# музыка
import os

current_path = os.path.dirname(__file__)
music_folder = os.path.join(current_path, "music")
songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]

if not songs:
    print("No music found in 'musics' folder")
    exit()

current = 0

def play_song():
    pygame.mixer.music.load(os.path.join(music_folder, songs[current]))
    pygame.mixer.music.play()

def stop_song():
    pygame.mixer.music.stop()

def next_song():
    global current
    current = (current + 1) % len(songs)
    play_song()

def prev_song():
    global current
    current = (current - 1) % len(songs)
    play_song()

def draw_button(text, x, y):
    label = font.render(text, True, WHITE)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)
    return rect

play_song()

running = True

while running:
    screen.fill(BLACK)

    # UI
    title = font.render("Music Player", True, GRAY)
    screen.blit(title, (170, 20))

    song_name = font.render(songs[current], True, WHITE)
    screen.blit(song_name, (120, 60))

    play_btn = draw_button("Play (P)", 250, 120)
    stop_btn = draw_button("Stop (S)", 250, 160)
    next_btn = draw_button("Next (N)", 250, 200)
    prev_btn = draw_button("Back (B)", 250, 240)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # клавиши
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                play_song()

            elif event.key == pygame.K_s:
                stop_song()

            elif event.key == pygame.K_n:
                next_song()

            elif event.key == pygame.K_b:
                prev_song()

            elif event.key == pygame.K_q:
                running = False

        # мышка (кликабельные кнопки)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_btn.collidepoint(event.pos):
                play_song()
            elif stop_btn.collidepoint(event.pos):
                stop_song()
            elif next_btn.collidepoint(event.pos):
                next_song()
            elif prev_btn.collidepoint(event.pos):
                prev_song()

    pygame.display.update()

pygame.quit()