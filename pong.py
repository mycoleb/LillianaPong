

import pygame
import sys
import random
import time
import logging
import os

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='pong_debug.log'
)

# Also print to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console_handler)

# Log startup information
logging.info("Starting Lilliana Pong...")
# Load and scale images
# Define hitbox dimensions FIRST
BALL_WIDTH = 40  # Your current ball hitbox width
BALL_HEIGHT = 40  # Your current ball hitbox height
PADDLE_WIDTH = 100  # Your current paddle width (240 * 0.25)
# PADDLE_HEIGHT = 75  # Your current paddle height (300 * 0.25)



# Scale the paddle image
#paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
# First initialize pygame
pygame.init()

# Define initial dimensions
BALL_WIDTH = 100  # Your current ball hitbox width
BALL_HEIGHT = 100  # Your current ball hitbox height
PADDLE_WIDTH = 100  # Initial paddle width

# Then load and scale images
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    ball_path = os.path.join(current_dir, "ball.png")
    paddle_path = os.path.join(current_dir, "paddle.png")
    
    logging.info(f"Attempting to load ball image from: {ball_path}")
    ball_img = pygame.image.load(ball_path)
    logging.info("Successfully loaded ball image")
    
    logging.info(f"Attempting to load paddle image from: {paddle_path}")
    paddle_img = pygame.image.load(paddle_path)
    logging.info("Successfully loaded paddle image")

    # Now calculate paddle height based on aspect ratio
    paddle_orig_width = paddle_img.get_width()
    paddle_orig_height = paddle_img.get_height()
    paddle_aspect = paddle_orig_width / paddle_orig_height
    PADDLE_HEIGHT = int(PADDLE_WIDTH / paddle_aspect)  # This will maintain the ratio

    # Scale the images
    ball_img = pygame.transform.scale(ball_img, (BALL_WIDTH, BALL_HEIGHT))
    paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))
    
    logging.info(f"Scaled ball to {BALL_WIDTH}x{BALL_HEIGHT}")
    logging.info(f"Scaled paddle to {PADDLE_WIDTH}x{PADDLE_HEIGHT}")

except pygame.error as e:
    logging.error(f"Failed to load game images: {e}")
    logging.error("Make sure 'ball.png' and 'paddle.png' are in the same directory as the script")
    pygame.quit()
    sys.exit(1)
except Exception as e:
    logging.error(f"Unexpected error loading images: {e}")
    pygame.quit()
    sys.exit(1)
# Initialize Pygame
pygame.init()


# Set up fonts
font = pygame.font.Font(None, 36)  # Default font, size 36

# Set up custom pixelated font for 8-bit style
# Set up custom pixelated font for 8-bit style
# Update the 'L' pattern in your PixelFont class
class PixelFont:
    def __init__(self):
        self.font_data = {
            'L': ['█    ', # Changed from '  ███ '
                 '█    ', # Changed from ' █    '
                 '█    ', # Changed from '  ██  '
                 '█    ', # Changed from '    █ '
                 '████ '], # Changed from ' ███  '
            'I': [' ███ ', '  █  ', '  █  ', '  █  ', ' ███ '],
            'O': [' ███ ', '█   █', '█   █', '█   █', ' ███ '],
            'B': ['███  ', '█  █ ', '███  ', '█  █ ', '███  '],
            'H': ['█   █', '█   █', '█████', '█   █', '█   █'],
            'A': [' ███ ', '█   █', '█████', '█   █', '█   █'],
            'N': ['█   █', '██  █', '█ █ █', '█  ██', '█   █'],
            'P': ['████ ', '█   █', '████ ', '█    ', '█    '],
            'G': [' ███ ', '█    ', '█  ██', '█   █', ' ███ '],
            'T': ['█████', '  █  ', '  █  ', '  █  ', '  █  ']
        }
        self.char_width = 6
        self.char_height = 5
        self.scale = 2

    def render(self, text, surface, x, y, color):
        current_x = x
        for char in text.upper():
            if char in self.font_data:
                char_pattern = self.font_data[char]
                for row_idx, row in enumerate(char_pattern):
                    for col_idx, pixel in enumerate(row):
                        if pixel == '█':
                            pygame.draw.rect(surface, color,
                                          (current_x + col_idx * self.scale,
                                           y + row_idx * self.scale,
                                           self.scale, self.scale))
            current_x += self.char_width * self.scale

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650  # Made taller to accommodate the banner
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("LILLIANA PONG")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# # Make the ball about half the current size
# BALL_WIDTH = 40  # Smaller ball size
# BALL_HEIGHT = 40

# # Make paddle proportionally smaller too
# PADDLEADJUSTOR = 1  # Changed from 0.5 to 0.25
# PADDLE_WIDTH = 240 * PADDLEADJUSTOR  # Will equal 60
# PADDLE_HEIGHT = 300 * PADDLEADJUSTOR  # Will equal 75

def update_ball():
    previous_pos = ball.rect.copy()
    
    # Move the ball
    ball.rect.x += ball.speed_x
    ball.rect.y += ball.speed_y
    
    # Ball collision with top and bottom
    if ball.rect.top <= 0 or ball.rect.bottom >= WINDOW_HEIGHT:
        logging.debug(f"Ball hit horizontal boundary at y={ball.rect.y}")
        ball.speed_y *= -1

    # Ball collision with paddles
    if ball.rect.colliderect(player.rect):
        logging.debug("Ball collided with player paddle")
        ball.speed_x *= -1
    elif ball.rect.colliderect(opponent.rect):
        logging.debug("Ball collided with opponent paddle")
        ball.speed_x *= -1

    # Score points and reset ball position
    if ball.rect.left <= 0:  # Ball goes past left edge
        opponent.score += 1
        ball.reset_pos()
        logging.debug("Ball reset after left edge score")
    elif ball.rect.right >= WINDOW_WIDTH:  # Ball goes past right edge
        player.score += 1
        ball.reset_pos()
        logging.debug("Ball reset after right edge score")

    # Log significant position changes
    if abs(previous_pos.x - ball.rect.x) > 10 or abs(previous_pos.y - ball.rect.y) > 10:
        logging.debug(f"Ball moved from {previous_pos} to {ball.rect}")
# Game objects
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WINDOW_WIDTH//2 - BALL_WIDTH//2,
                              WINDOW_HEIGHT//2 - BALL_HEIGHT//2,
                              BALL_WIDTH, BALL_HEIGHT)
        self.speed_x = 4 * random.choice((1, -1))
        self.speed_y = 4 * random.choice((1, -1))
        logging.info(f"Ball initialized with speed_x: {self.speed_x}, speed_y: {self.speed_y}")
        self.reset_pos()
        
    def reset_pos(self):
        self.rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.speed_x = 4 * random.choice((1, -1))
        self.speed_y = 4 * random.choice((1, -1))
        logging.debug(f"Ball reset to position: {self.rect.center} with speeds: ({self.speed_x}, {self.speed_y})")
class Paddle:
    def __init__(self, x, y, is_player=True):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 5 if is_player else 1  # AI moves much slower
        self.score = 0
        self.is_player = is_player
        self.last_move_time = time.time()
        self.move_count = 0
        
    def update_debug_info(self):
        if not self.is_player:
            current_time = time.time()
            self.move_count += 1
            if current_time - self.last_move_time >= 1:  # Every second
                print(f"AI Updates in last second: {self.move_count}")
                print(f"Current AI Position: {self.rect.y}")
                print(f"Current AI Speed: {self.speed}")
                self.move_count = 0
                self.last_move_time = current_time

# Initialize objects - place this after all class definitions
pixel_font = PixelFont()
player = Paddle(50, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, is_player=True)  # Left paddle
opponent = Paddle(WINDOW_WIDTH - 70, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2, is_player=False)  # Right paddle
ball = Ball()
def handle_paddle_movement():
    # Player paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.rect.top > 0:
        player.rect.y -= player.speed
    if keys[pygame.K_DOWN] and player.rect.bottom < WINDOW_HEIGHT:
        player.rect.y += player.speed

    # Simple AI for opponent paddle with debug info
    if opponent.rect.centery < ball.rect.centery and opponent.rect.bottom < WINDOW_HEIGHT:
        opponent.rect.y += opponent.speed
        opponent.update_debug_info()
    if opponent.rect.centery > ball.rect.centery and opponent.rect.top > 0:
        opponent.rect.y -= opponent.speed
        opponent.update_debug_info()
# After the Paddle class but before initialization of objects:

def draw_game():
    window.fill(BLACK)
    
    # Draw 8-bit banner
    pixel_font.render("LILLIANA PONG", window, 
                     WINDOW_WIDTH//2 - 120, 20, WHITE)
    
    # Draw paddles using images
    window.blit(paddle_img, player.rect)
    window.blit(paddle_img, opponent.rect)
    
    # Draw ball using image
    window.blit(ball_img, ball.rect)
    
    # Draw scores with labels
    # Human player score
    human_label = font.render("HUMAN", True, WHITE)
    player_text = font.render(str(player.score), True, WHITE)
    window.blit(human_label, (WINDOW_WIDTH//4 - 50, 20))
    window.blit(player_text, (WINDOW_WIDTH//4 + 50, 20))
    
    # Computer score - adjusted to put score right after the text
    computer_label = font.render("COMPUTER", True, WHITE)
    opponent_text = font.render(str(opponent.score), True, WHITE)
    window.blit(computer_label, (3*WINDOW_WIDTH//4 - 115, 20))  # Move label slightly left
    window.blit(opponent_text, (3*WINDOW_WIDTH//4 + 35, 20))    # Put score right after "COMPUTER"
    
    # Draw debug information on screen
    debug_font = pygame.font.Font(None, 24)
    debug_text = debug_font.render(
        f"AI Speed: {opponent.speed:.2f} | Y Pos: {opponent.rect.y}",
        True, WHITE
    )
    window.blit(debug_text, (10, WINDOW_HEIGHT - 30))
    
    # Draw center line
    pygame.draw.aaline(window, WHITE, 
                      (WINDOW_WIDTH//2, 0), 
                      (WINDOW_WIDTH//2, WINDOW_HEIGHT))
    
    pygame.display.flip()
    
# Create a key to toggle AI speed for testing
def handle_debug_keys():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:  # Press 1 to slow down AI
        opponent.speed = max(0.05, opponent.speed - 0.01)
    if keys[pygame.K_2]:  # Press 2 to speed up AI
        opponent.speed = min(5, opponent.speed + 0.01)
clock = pygame.time.Clock()
FPS = 60

# Modified game loop with debug controls and performance monitoring
frame_count = 0
start_time = time.time()

while True:
    current_time = time.time()
    
    # Log FPS every second
    frame_count += 1
    if current_time - start_time >= 1:
        fps = frame_count / (current_time - start_time)
        logging.info(f"Current FPS: {fps:.2f}")
        frame_count = 0
        start_time = current_time
    
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game quit requested")
                pygame.quit()
                sys.exit()

        handle_paddle_movement()
        handle_debug_keys()
        update_ball()
        draw_game()
        clock.tick(FPS)
        
    except Exception as e:
        logging.error(f"Error in game loop: {e}", exc_info=True)
        pygame.quit()
        sys.exit(1)