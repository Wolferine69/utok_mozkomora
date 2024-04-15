import pygame
import random

# Inicializace Pygame a nastavení základních proměnných pro hru
pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Útok mozkomora")

# Nastavení frekvence snímků a časovače
fps = 60
clock = pygame.time.Clock()

# Definice základních herních proměnných
player_start_lives = 5  # Počáteční počet životů hráče
mozkomor_start_speed = 2  # Počáteční rychlost mozkomora
mozkomor_speed_update = 0.5  # Zrychlení mozkomora po úspěšném zásahu
score = 0  # Skóre hráče

# Aktuální herní stav
player_lives = player_start_lives
mozkomor_speed = mozkomor_start_speed

# Náhodný směr pohybu mozkomora
mozkomor_x = random.choice([-1, 1])
mozkomor_y = random.choice([-1, 1])

# Načtení obrázků pro pozadí a mozkomora
background = pygame.image.load("img/hogwarts-castle.jpg")
mozkomor = pygame.image.load("img/mozkomor.png")
mozkomor_rect = mozkomor.get_rect(center=(width / 2, height / 2))

# Nastavení fontů a textů
dark_yellow = pygame.Color("#938f0c")
potter_font_big = pygame.font.Font("fonts/Harry.ttf", 50)
potter_font_middle = pygame.font.Font("fonts/Harry.ttf", 30)
score_text = potter_font_middle.render(f"Score: {score}", True, dark_yellow)
score_text_rect = score_text.get_rect(topright=(width - 30, 10))
lives_text = potter_font_middle.render(f"Lives: {player_lives}", True, dark_yellow)
lives_text_rect = lives_text.get_rect(topright=(width - 30, 50))
game_over_text = potter_font_big.render("Game over", True, dark_yellow)
game_over_text_rext = game_over_text.get_rect(center=(width / 2, height / 2))
contine_text = potter_font_middle.render("Click anywhere to continue", True, dark_yellow)
contine_text_rect = contine_text.get_rect(center=(width / 2, height / 2 + 50))

# Načtení zvukových efektů a hudby
success_click = pygame.mixer.Sound("media/success_click.wav")
miss_click = pygame.mixer.Sound("media/miss_click.wav")
pygame.mixer.music.load("media/bg-music-hp.wav")
success_click.set_volume(0.2)
miss_click.set_volume(0.2)

# Spuštění hudby na pozadí
pygame.mixer.music.play(-1)

# Hlavní herní smyčka
pokracovat = True
while pokracovat:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pokracovat = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Detekce, zda hráč trefil mozkomora
            if mozkomor_rect.collidepoint(event.pos):
                success_click.play()
                score += 1
                mozkomor_speed += mozkomor_speed_update
                # Změna směru mozkomora
                prev_x = mozkomor_x
                prev_y = mozkomor_y
                while prev_x == mozkomor_x and prev_y == mozkomor_y:
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])
            else:
                miss_click.play()
                player_lives -= 1

    # Pohyb mozkomora
    mozkomor_rect.x += mozkomor_x * mozkomor_speed
    mozkomor_rect.y += mozkomor_y * mozkomor_speed

    # Odrážení mozkomora od okrajů obrazovky
    if mozkomor_rect.left <= 0:
        mozkomor_x = 1
    elif mozkomor_rect.right >= width:
        mozkomor_x = -1
    elif mozkomor_rect.top <= 0:
        mozkomor_y = 1
    elif mozkomor_rect.bottom >= height:
        mozkomor_y = -1

    # Aktualizace a vykreslení skóre a životů
    score_text = potter_font_middle.render(f"Score: {score}", True, dark_yellow)
    lives_text = potter_font_middle.render(f"Lives: {player_lives}", True, dark_yellow)
    screen.blit(background, (0, 0))
    screen.blit(mozkomor, mozkomor_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    pygame.display.update()

    # Zobrazování obrazovky Game Over při vyčerpání životů
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rext)
        screen.blit(contine_text, contine_text_rect)
        pygame.display.update()
        pygame.mixer_music.stop()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset hry
                    score = 0
                    player_lives = player_start_lives
                    mozkomor_speed = mozkomor_start_speed
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])
                    mozkomor_rect = mozkomor.get_rect(center=(width / 2, height / 2))
                    pygame.mixer.music.play(-1)
                    paused = False
                elif event.type is pygame.QUIT:
                    paused = False
                    pokracovat = False

    clock.tick(fps)

# Ukončení Pygame
pygame.quit()
