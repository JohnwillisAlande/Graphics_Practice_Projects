import pygame
import sys
import random  # Import the whole random module

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 600, 400  # Game window size
RADIUS = 20  # Circle radius

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window with the specified size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Bouncing 2D Ball')

# Initial position and velocity of the circle
x, y = WIDTH // 2, HEIGHT // 2  # Start at the center of the screen
dx, dy = 5, 4  # Movement speed

# Initial background color
background_color = (0,0,0)  # Start with white

# Function to generate a random color
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the circle's position
    x += dx
    y += dy

    # Bounce off the walls and change background color on collision
    if x - RADIUS <= 0 or x + RADIUS >= WIDTH:
        dx = -dx  # Reverse x-direction
        background_color = get_random_color()  # Change background color

    if y - RADIUS <= 0 or y + RADIUS >= HEIGHT:
        dy = -dy  # Reverse y-direction
        background_color = get_random_color()  # Change background color

    # Fill the screen with the current background color
    screen.fill(background_color)

    # Draw the circle
    pygame.draw.circle(screen, BLACK, (x, y), RADIUS)

    # Update the display
    pygame.display.flip()

    # Control the frame rate (limit to 60 FPS)
    pygame.time.Clock().tick(60)