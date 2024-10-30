import pygame  # Import Pygame library for game development
import sys     # Import sys for system functions, such as exiting the game
import random  # Import random for generating random values

# Initialize Pygame library
pygame.init()

# Constants for game window dimensions and colors
WIDTH, HEIGHT = 600, 400          # Screen width and height
RADIUS = 20                        # Ball radius
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10  # Paddle dimensions
WHITE = (255, 255, 255)            # RGB color for white
BLACK = (0, 0, 0)                  # RGB color for black

# Create the game display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing Ball Game')  # Set window title

# Initial position for paddle and its speed
paddle_x = (WIDTH - PADDLE_WIDTH) // 2  # Center paddle horizontally
paddle_y = HEIGHT - PADDLE_HEIGHT - 10  # Position paddle near bottom of screen
paddle_speed = 8                        # Paddle movement speed

# Initial position and velocity for the ball
x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS  # Start above paddle center
dx, dy = 0, 0  # Ball starts stationary

# Score and game state flags
score = 0            # Player's score
ball_launched = False  # Tracks if the ball has been launched
game_over = False      # Tracks if the game is over

# Set font for displaying text on the screen
font = pygame.font.Font(None, 36)

# Random initial background and target colors
background_color = random.choices(range(256), k=3)  # RGB for gradient background
target_color = random.choices(range(256), k=3)      # Target color for smooth transition


# Smoothly transition colors for background
def smooth_color_transition(current, target, speed=1):
    return tuple(min(255, max(0, current[i] + (speed if current[i] < target[i] else -speed))) for i in range(3))

# Draw gradient background between two colors
def draw_gradient_background(color1, color2):
    for i in range(HEIGHT):
        ratio = i / HEIGHT  # Gradual color blending ratio
        color = (
            int(color1[0] * (1 - ratio) + color2[0] * ratio),
            int(color1[1] * (1 - ratio) + color2[1] * ratio),
            int(color1[2] * (1 - ratio) + color2[2] * ratio),
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))  # Draw a horizontal line for each row


# Main game loop
clock = pygame.time.Clock()
while True:
    # Handle events, such as quitting the game or pressing keys
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Close the game window
            sys.exit()     # Exit the program
        elif event.type == pygame.KEYDOWN and not ball_launched and not game_over:
            dx, dy = random.choice([-5, 5]), -5  # Launch ball in random horizontal direction
            ball_launched = True  # Mark ball as launched

    # Paddle movement controls
    keys = pygame.key.get_pressed()  # Check pressed keys
    if keys[pygame.K_LEFT]:          # Move paddle left if within screen bounds
        paddle_x = max(0, paddle_x - paddle_speed)
    if keys[pygame.K_RIGHT]:         # Move paddle right if within screen bounds
        paddle_x = min(WIDTH - PADDLE_WIDTH, paddle_x + paddle_speed)

    # Only update game state if the game is not over
    if not game_over:
        if ball_launched:
            x += dx  # Update ball's x-coordinate
            y += dy  # Update ball's y-coordinate

        # Ball collision with left and right walls
        if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
            dx = -dx  # Reverse ball's horizontal direction
            target_color = random.choices(range(256), k=3)  # Change background target color

        # Ball collision with the top wall
        if y - RADIUS <= 0:
            dy = -dy  # Reverse ball's vertical direction
            target_color = random.choices(range(256), k=3)  # Change background target color

        # Ball collision with the paddle
        if dy > 0 and y + RADIUS >= paddle_y and paddle_x <= x <= paddle_x + PADDLE_WIDTH:
            dy = -dy  # Reverse ball's vertical direction
            score += 1  # Increase score
            target_color = random.choices(range(256), k=3)  # Change background target color

        # Game over if ball falls below the paddle
        if y + RADIUS >= HEIGHT:
            game_over = True  # Set game state to over
            dy = 0  # Stop ball movement

    # Update gradient background color
    background_color = smooth_color_transition(background_color, target_color, speed=2)
    if background_color == target_color:
        target_color = random.choices(range(256), k=3)  # Update target color if transition complete
    draw_gradient_background(background_color, BLACK)

    # Draw paddle and ball
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))  # Paddle
    if not ball_launched:
        x = paddle_x + PADDLE_WIDTH // 2  # Position ball above center of paddle
        y = paddle_y - RADIUS
    pygame.draw.circle(screen, WHITE, (x, y), RADIUS)  # Ball

    # Display score or game over message
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
        final_score_text = font.render(f'Final Score: {score}', True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 40))

        # Restart game if 'R' key is pressed
        if keys[pygame.K_r]:
            x, y = paddle_x + PADDLE_WIDTH // 2, paddle_y - RADIUS  # Reset ball position
            dx, dy = 0, 0  # Reset ball velocity
            score = 0  # Reset score
            ball_launched = False  # Ball not launched yet
            game_over = False  # Game is active again
            background_color = random.choices(range(256), k=3)  # Reset background color
            target_color = random.choices(range(256), k=3)      # Reset target color
    else:
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))  # Display score at top-left

    # Refresh display and cap the frame rate
    pygame.display.flip()  # Update the screen
    clock.tick(60)         # Maintain 60 frames per second