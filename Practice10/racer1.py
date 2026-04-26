import pygame
import random
import sys

pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 400, 600
ROAD_LEFT, ROAD_RIGHT = 60, 340
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // 3
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer PRO")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24, True)
big = pygame.font.SysFont("Arial", 50, True)

# --- COLORS ---
WHITE = (255,255,255)
GRAY = (80,80,80)
GREEN = (30,150,30)
RED = (200,40,40)
BLUE = (40,100,200)
YELLOW = (255,220,0)

# --- ROAD ---
class Road:
    def __init__(self):
        self.offset = 0
        self.speed = 5

    def update(self):
        self.offset = (self.offset + self.speed) % 80

    def draw(self):
        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT-ROAD_LEFT, HEIGHT))

        for i in range(3):
            x = ROAD_LEFT + i * LANE_WIDTH
            y = self.offset - 80
            while y < HEIGHT:
                pygame.draw.rect(screen, WHITE, (x+LANE_WIDTH-5, y, 5, 40))
                y += 80

# --- PLAYER ---
class Player:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT - 100
        self.speed = 5

    def move(self, keys):
        spd = self.speed * (2 if keys[pygame.K_LSHIFT] else 1)

        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT:
            self.x -= spd
        if keys[pygame.K_RIGHT] and self.x < ROAD_RIGHT-30:
            self.x += spd

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 30, 60))

    def rect(self):
        return pygame.Rect(self.x, self.y, 30, 60)

# --- ENEMY ---
class Enemy:
    def __init__(self, speed):
        self.x = random.randint(ROAD_LEFT, ROAD_RIGHT-30)
        self.y = -60
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, 30, 60))

    def rect(self):
        return pygame.Rect(self.x, self.y, 30, 60)

# --- MENU ---
def draw_menu():
    screen.fill((0,0,0))
    title = big.render("RACER", True, WHITE)
    start = font.render("Press SPACE to Start", True, WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, 200))
    screen.blit(start, (WIDTH//2 - start.get_width()//2, 300))

    pygame.display.flip()

# --- MAIN GAME ---
def main():
    road = Road()
    player = Player()
    enemies = []

    score = 0
    spawn_timer = 0
    paused = False
    game_over = False

    while True:
        clock.tick(FPS)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if game_over and event.key == pygame.K_r:
                    main()
                if game_over and event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()

        if not paused and not game_over:
            player.move(keys)
            road.update()

            spawn_timer += 1
            if spawn_timer > 60:
                enemies.append(Enemy(4 + score//5))
                spawn_timer = 0

            for en in enemies[:]:
                en.update()

                if en.y > HEIGHT:
                    enemies.remove(en)
                    score += 1

                if en.rect().colliderect(player.rect()):
                    game_over = True

        # DRAW
        road.draw()
        player.draw()

        for en in enemies:
            en.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10,10))

        if paused:
            pause = big.render("PAUSE", True, YELLOW)
            screen.blit(pause, (WIDTH//2 - pause.get_width()//2, 250))

        if game_over:
            over = big.render("GAME OVER", True, RED)
            restart = font.render("R - Restart | Q - Quit", True, WHITE)

            screen.blit(over, (WIDTH//2 - over.get_width()//2, 220))
            screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 300))

        pygame.display.flip()

# --- START SCREEN LOOP ---
while True:
    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            main()
