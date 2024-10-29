import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
RADIUS = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Ball Game')

# Initial paddle position
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10
paddle_speed = 8

# Initial ball position and velocity
x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS
dx, dy = 0, 0  # Ball starts stationary

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game state
ball_launched = False  # Ball initially rests on the paddle

# Function to generate a random color
def get_random_color():
    return random.choices(range(256), k=3)

# Function to draw a gradient background
def draw_gradient_background(color1, color2):
    for i in range(HEIGHT):
        ratio = i / HEIGHT
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

background_color = get_random_color()

# Main loop
clock = pygame.time.Clock()
paused = False

while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not ball_launched:
                # Launch the ball in a random direction when any key is pressed
                dx = random.choice([-5, 5])
                dy = -5
                ball_launched = True

    # Paddle control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x = max(0, paddle_x - paddle_speed)
    if keys[pygame.K_RIGHT]:
        paddle_x = min(WIDTH - PADDLE_WIDTH, paddle_x + paddle_speed)

    # Update ball position only if it's launched
    if ball_launched:
        x += dx
        y += dy

    # Bounce off walls and change background color
    if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
        dx = -dx
        background_color = get_random_color()

    # Bounce off paddle and increase score
    if ball_launched and y + RADIUS >= paddle_y and paddle_x <= x <= paddle_x + PADDLE_WIDTH:
        dy = -dy
        score += 1
        background_color = get_random_color()

    # Check for game over
    if y + RADIUS >= HEIGHT:
        print(f"Game Over! Your score: {score}")
        pygame.quit()
        sys.exit()

    # Bounce off top and change background color
    if y - RADIUS <= 0:
        dy = -dy
        background_color = get_random_color()

    # Draw gradient background
    draw_gradient_background(background_color, BLACK)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw ball (resting on paddle if not launched)
    if not ball_launched:
        x = paddle_x + PADDLE_WIDTH // 2
        y = paddle_y - RADIUS
    pygame.draw.circle(screen, WHITE, (x, y), RADIUS)

    # Render score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(60)