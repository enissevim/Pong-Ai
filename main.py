import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong AI")

# Ball and paddle positions
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
player_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_speed_x, ball_speed_y = random.choice([-5, 5]), random.choice([-5, 5])
player_speed = 0
opponent_speed = 5

# Game variables
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Reset the ball
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

# Draw everything on the screen
def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, opponent_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Display scores
    player_text = font.render(f"{player_score}", True, WHITE)
    opponent_text = font.render(f"{opponent_score}", True, WHITE)
    screen.blit(player_text, (WIDTH - 50, 20))
    screen.blit(opponent_text, (30, 20))

    pygame.display.flip()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -7
            if event.key == pygame.K_DOWN:
                player_speed = 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_speed = 0

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1

    # Ball goes out of bounds
    if ball.left <= 0:
        player_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        opponent_score += 1
        reset_ball()

    # Player paddle movement
    player_paddle.y += player_speed
    player_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, player_paddle.y))

    # Opponent paddle movement (basic AI)
    if ball.centery > opponent_paddle.centery + PADDLE_HEIGHT // 2:
        opponent_paddle.y += opponent_speed
    elif ball.centery < opponent_paddle.centery - PADDLE_HEIGHT // 2:
        opponent_paddle.y -= opponent_speed
    opponent_paddle.y = max(0, min(HEIGHT - PADDLE_HEIGHT, opponent_paddle.y))

    # Draw everything
    draw()

    # Control game speed
    clock.tick(FPS)

pygame.quit()
