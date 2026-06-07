import pygame
import sys

pygame.init() # Pygame'i käivitamine
pygame.mixer.init() # Helimooduli käivitamine

# Ekraani mõõtmed
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Värvide defineerimine
TAUST = (153, 232, 158)      # Heleroheline taust
SCORE_COLOR = (0, 102, 51)   # Tume roheline skoor

# Mänguakna loomine
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping pong - Metsjärv")

clock = pygame.time.Clock() # Kell FPS-i kontrollimiseks
font = pygame.font.SysFont("comicsansms", 24, bold=True) # Fondi loomine skoori kuvamiseks
pygame.mixer.music.load("dino_2026.mp3") # Taustamuusika laadimine
pygame.mixer.music.play(-1) # Muusika mängimine lõputus tsüklis (-1)

# Palli pildi laadimine ja suuruse muutmine
ball_img = pygame.image.load("ball.png")
ball_img = pygame.transform.scale(ball_img, (20, 20))

# Aluse (reketi) pildi laadimine ja suuruse muutmine
paddle_img = pygame.image.load("pad.png")
paddle_img = pygame.transform.scale(paddle_img, (120, 20))

# Palli algasukoht
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 4

# Palli liikumiskiirus
ball_speed_x = 4
ball_speed_y = 4

# Aluse mõõtmed
paddle_width = 120
paddle_height = 20

paddle_x = (SCREEN_WIDTH - paddle_width) // 2 # Asetab aluse ekraani keskele
paddle_y = int(SCREEN_HEIGHT / 1.1) # Asetab aluse ekraani alumisse ossa
paddle_speed = 8 # Aluse liikumiskiirus
score = 0 # Mängija algskoor

# Mängu põhitsükkel
running = True
while running:

    for event in pygame.event.get(): # Sündmuste kontrollimine

        # Kui kasutaja sulgeb akna
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Vasak nool
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed

    # Parem nool
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Palli liikumine
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Vasaku või parema seina põrge
    if ball_x <= 0 or ball_x + 20 >= SCREEN_WIDTH:
        ball_speed_x *= -1

    # Ülemine sein
    if ball_y <= 0:
        ball_speed_y *= -1

    # Kui pall puudutab ekraani alumist serva
    if ball_y + 20 >= SCREEN_HEIGHT:
        print(f"Mäng läbi! Sinu skoor: {score}")
        running = False

    # Loome ristkülikud kokkupõrgete kontrollimiseks
    ball_rect = pygame.Rect(ball_x, ball_y, 20, 20)
    paddle_rect = pygame.Rect(
        paddle_x,
        paddle_y,
        paddle_width,
        paddle_height)

    if ball_rect.colliderect(paddle_rect): # Kontrollib, kas pall puudutab alust
        if ball_speed_y > 0: # Ainult siis, kui pall liigub alla
            ball_speed_y *= -1 # Muudab vertikaalse liikumissuuna vastupidiseks
            score += 1 # Suurendab skoori

            # Muudab palli iga põrkega veidi kiiremaks
            ball_speed_x *= 1.05
            ball_speed_y *= 1.05

    screen.fill(TAUST) # Täidab tausta värviga
    screen.blit(ball_img, (ball_x, ball_y)) # Joonistab palli
    screen.blit(paddle_img, (paddle_x, paddle_y)) # Joonistab aluse

    # Kuvab skoori ekraanile
    score_text = font.render(
        f"Skoor: {score}",
        True,
        SCORE_COLOR)
        
    screen.blit(score_text, (20, 20)) # Skoori asukoht
    pygame.display.flip() # Uuendab ekraani
    clock.tick(60) # Piirab mängu kiiruse 60 kaadrini sekundis

# Mängu sulgemine
pygame.quit()
sys.exit()
