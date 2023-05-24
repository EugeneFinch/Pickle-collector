import pygame
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Collect the Coins")

player_width = 70
player_height = 70
coin_width = 50
coin_height = 50

font = pygame.font.Font(None, 36)  # Initialize font before using it

# Set up the game clock
clock = pygame.time.Clock()

# Initialize mixer module
mixer.init()

# Load background image
background_image = pygame.image.load("background.jpg").convert()

# Load player and coin images
player_image = pygame.image.load("player_image.png").convert_alpha()
coin_image = pygame.image.load("coin_image.png").convert_alpha()

player_image = pygame.transform.scale(player_image, (player_width, player_height))
coin_image = pygame.transform.scale(coin_image, (coin_width, coin_height))

# Load background music
mixer.music.load("music.mp3")
mixer.music.play(-1)  # Set -1 to loop the music indefinitely
sweep_sound = pygame.mixer.Sound("sound.wav")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)  # Cyan

# Define game objects
player_x = screen_width // 2
player_y = screen_height - player_height
player_speed = 6  # Adjust the player speed here
player = pygame.Rect(player_x, player_y, player_width, player_height)

coin_x = random.randint(0, screen_width - coin_width)
coin_y = random.randint(0, screen_height // 2)
coin_speed = 4  # Adjust the coin speed here
coin = pygame.Rect(coin_x, coin_y, coin_width, coin_height)

score = 0
level = 0
attempts = 3  # Initialize number of attempts to 3
game_over = False
play_again = False
quit_game = False
startup = True

start_button = pygame.Rect(screen_width // 2 - 80, screen_height // 2, 160, 40)
start_button_text = font.render("Start", True, WHITE)

score_font = pygame.font.Font(None, 36)


def create_levels(score):
    global level
    if score >= 10:
        level = 1
        while score >= 10 * (1.3 ** level):
            level += 1

def display_level():
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (10, 40))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

       	if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if startup and start_button.collidepoint(mouse_pos):
                startup = False

            # Handle play again button click
            if (
                game_over
                and play_again
                and screen_width // 2 - 80 <= mouse_pos[0] <= screen_width // 2 + 80
                and screen_height // 2 <= mouse_pos[1] <= screen_height // 2 + 40
            ):
                score = 0
                attempts = 3
                game_over = False
                play_again = False
                quit_game = False
                pygame.mixer.music.play(-1)

            # Handle quit button click
            if (
                game_over
                and quit_game
                and screen_width // 2 - 80 <= mouse_pos[0] <= screen_width // 2 + 80
                and screen_height // 2 + 60 <= mouse_pos[1] <= screen_height // 2 + 100
            ):
                pygame.quit()
                quit()

    if startup:
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, start_button)
        screen.blit(
            start_button_text, (screen_width // 2 - 30, screen_height // 2 + 10)
        )

    elif not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        elif keys[pygame.K_RIGHT] and player.x < screen_width - player_width:
            player.x += player_speed

        coin.y += coin_speed
        if coin.y > screen_height:
            coin.x = random.randint(0, screen_width - coin_width)
            coin.y = random.randint(0, screen_height // 2)
            attempts -= 1  # Deduct one attempt when the player misses a coin

        if player.colliderect(coin):
            sweep_sound.play()
            coin.x = random.randint(0, screen_width - coin_width)
            coin.y = random.randint(0, screen_height // 2)
            score += 1
            create_levels(score)  # Update the level based on the score


        if attempts == 0:
            game_over = True
            play_again = True
            quit_game = True
            pygame.mixer.music.stop()

        screen.blit(background_image, (0, 0))
        screen.blit(player_image, (player.x, player.y))
        screen.blit(coin_image, (coin.x, coin.y))

        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        attempts_text = font.render(f"Attempts: {attempts}", True, WHITE)
        screen.blit(attempts_text, (10, 70))

        display_level()  # Display the current level on the screen


        if game_over:
            game_over_text = font.render("Game Over!", True, RED)
            play_again_text = font.render("Play Again?", True, BLUE)
            quit_text = font.render("Quit", True, BLUE)

            screen.blit(
                game_over_text, (screen_width // 2 - 80, screen_height // 2 - 50)
            )
            screen.blit(play_again_text, (screen_width // 2 - 70, screen_height // 2))
            screen.blit(quit_text, (screen_width // 2 - 30, screen_height // 2 + 60))

        if play_again:
            pygame.draw.rect(
                screen, BLUE, (screen_width // 2 - 80, screen_height // 2, 160, 40)
            )
            play_again_button_text = font.render("Play Again", True, WHITE)
            screen.blit(
                play_again_button_text,
                (screen_width // 2 - 60, screen_height // 2 + 10),
            )

        if quit_game:
            pygame.draw.rect(
                screen, BLUE, (screen_width // 2 - 80, screen_height // 2 + 60, 160, 40)
            )
            quit_button_text = font.render("Quit", True, WHITE)
            screen.blit(
                quit_button_text, (screen_width // 2 - 25, screen_height // 2 + 70)
            )

    pygame.display.update()
    clock.tick(60)
