import pygame
import sys

pygame.init()  # Pygame'i käivitamine
pygame.mixer.init()  # Helimooduli käivitamine


# Ekraani mõõtmed
screen_width = 640
screen_height = 480

# Värvide defineerimine
taust = (153, 232, 158)         # Heleroheline taust
roheline = (0, 102, 51)    # Tekstid


# Mänguakna loomine
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping pong 2 - Metsjärv")

clock = pygame.time.Clock()  # Kell FPS-i kontrollimiseks
font = pygame.font.SysFont("comicsansms", 24, bold=True)  # Fondi loomine skoori kuvamiseks
pygame.mixer.music.load("Raining tacos.mp3")

# Helitugevus vahemikus 0.0 kuni 1.0
pygame.mixer.music.set_volume(0.1)  # 30% tugevus

pygame.mixer.music.play(-1)
# Muud heliefektid
bounce_sound = pygame.mixer.Sound("Bounce.mp3")
gameover_sound = pygame.mixer.Sound("Surm.mp3")

bounce_sound.set_volume(1.0)
gameover_sound.set_volume(0.8)

# Palli pildi laadimine ja suuruse muutmine
ball_img = pygame.image.load("ball.png")
ball_img = pygame.transform.scale(ball_img, (20, 20))

# Aluse (reketi) pildi laadimine ja suuruse muutmine
paddle_img = pygame.image.load("pad.png")
paddle_img = pygame.transform.scale(paddle_img, (120, 20))

# Palli algasukoht
ball_x = screen_width // 2
ball_y = screen_height // 4

# Palli liikumiskiirus
ball_speed_x = 4
ball_speed_y = 4

# Aluse mõõtmed
paddle_width = 120
paddle_height = 20

paddle_x = (screen_width - paddle_width) // 2  # Asetab aluse ekraani keskele
paddle_y = int(screen_height / 1.1)  # Asetab aluse ekraani alumisse ossa
paddle_speed = 8  # Aluse liikumiskiirus
score = 0  # Mängija algskoor

# Mängu põhitsükkel
running = True
while running:

    for event in pygame.event.get():  # Sündmuste kontrollimine

        # Kui kasutaja sulgeb akna
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Vasak nool
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed

    # Parem nool
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # Palli liikumine
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Vasaku või parema seina põrge
    if ball_x <= 0 or ball_x + 20 >= screen_width:
        ball_speed_x *= -1

    # Ülemine sein
    if ball_y <= 0:
        ball_speed_y *= -1

    if ball_y + 20 >= screen_height:
        gameover_sound.play()

        game_over = True

        while game_over:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_over = False
                    running = False

                if event.type == pygame.KEYDOWN:

                    # Q = välju
                    if event.key == pygame.K_q:
                        game_over = False
                        running = False

                    # C = jätka mängu
                    if event.key == pygame.K_r:
                        # Lähtesta pall
                        ball_x = screen_width // 2
                        ball_y = screen_height // 4

                        ball_speed_x = 4
                        ball_speed_y = 4

                        # Lähtesta alus
                        paddle_x = (screen_width - paddle_width) // 2

                        score = 0
                        game_over = False

            screen.fill(taust)

            gameover_font = pygame.font.SysFont("comicsansms", 30, bold=True)
            score_font = pygame.font.SysFont("comicsansms", 24, bold=True)

            gameover_text = gameover_font.render(
                "Mäng läbi!",
                True,
                roheline
            )

            score_text = score_font.render(
                f"Sinu skoor: {score}",
                True,
                roheline
            )

            continue_text = score_font.render(
                "R - Proovi uuesti",
                True,
                roheline
            )

            quit_text = score_font.render(
                "Q - Quit",
                True,
                roheline
            )

            screen.blit(
                gameover_text,
                (screen_width // 2 - gameover_text.get_width() // 2, 140)
            )

            screen.blit(
                score_text,
                (screen_width // 2 - score_text.get_width() // 2, 200)
            )

            screen.blit(
                continue_text,
                (screen_width // 2 - continue_text.get_width() // 2, 260)
            )

            screen.blit(
                quit_text,
                (screen_width // 2 - quit_text.get_width() // 2, 300)
            )

            pygame.display.flip()

        continue
    # Loome ristkülikud kokkupõrgete kontrollimiseks
    ball_rect = pygame.Rect(ball_x, ball_y, 20, 20)
    paddle_rect = pygame.Rect(
        paddle_x,
        paddle_y,
        paddle_width,
        paddle_height)

    if ball_rect.colliderect(paddle_rect):
        if ball_speed_y > 0:
            ball_speed_y *= -1
            score += 1

            # Mängib põrkeheli
            bounce_sound.play()

            ball_speed_x *= 1.05
            ball_speed_y *= 1.05

    screen.fill(taust)  # Täidab tausta värviga
    screen.blit(ball_img, (ball_x, ball_y))  # Joonistab palli
    screen.blit(paddle_img, (paddle_x, paddle_y))  # Joonistab aluse

    # Kuvab skoori ekraanile
    score_text = font.render(
        f"Skoor: {score}",
        True,
        roheline)

    screen.blit(score_text, (20, 20))  # Skoori asukoht
    pygame.display.flip()  # Uuendab ekraani
    clock.tick(60)  # Piirab mängu kiiruse 60 kaadrini sekundis

# Mängu sulgemine
pygame.quit()
sys.exit()
