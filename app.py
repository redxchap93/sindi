```python
import pygame
import sys
import random
import logging
from typing import Tuple, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('snake_game.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 20):
        """
        Initialize the Snake game
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            cell_size: Size of each grid cell in pixels
        """
        try:
            pygame.init()
            self.width = width
            self.height = height
            self.cell_size = cell_size
            self.grid_width = width // cell_size
            self.grid_height = height // cell_size
            
            # Create the screen
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Snake Game")
            
            # Game clock
            self.clock = pygame.time.Clock()
            
            # Colors
            self.BLACK = (0, 0, 0)
            self.WHITE = (255, 255, 255)
            self.GREEN = (0, 255, 0)
            self.RED = (255, 0, 0)
            self.BLUE = (0, 0, 255)
            self.YELLOW = (255, 255, 0)
            self.PURPLE = (128, 0, 128)
            
            # Game state
            self.snake = [(self.grid_width // 2, self.grid_height // 2)]
            self.direction = (1, 0)  # Start moving right
            self.food = self.generate_food()
            self.score = 0
            self.game_over = False
            self.speed = 10
            self.level = 1
            self.high_score = 0
            self.obstacles = []
            self.power_ups = []
            self.power_up_timer = 0
            self.invincible = False
            
            # Generate initial obstacles
            self.generate_obstacles()
            
            logging.info("Snake game initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize Snake game: {e}")
            raise

    def generate_food(self) -> Tuple[int, int]:
        """
        Generate food at a random position not occupied by the snake or obstacles
        
        Returns:
            Tuple of (x, y) coordinates for food
        """
        try:
            while True:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (x, y) not in self.snake and (x, y) not in self.obstacles and (x, y) != self.food:
                    return (x, y)
        except Exception as e:
            logging.error(f"Failed to generate food: {e}")
            raise

    def generate_obstacles(self):
        """Generate random obstacles on the game board"""
        try:
            self.obstacles = []
            num_obstacles = min(10, self.grid_width * self.grid_height // 50)
            
            for _ in range(num_obstacles):
                while True:
                    x = random.randint(0, self.grid_width - 1)
                    y = random.randint(0, self.grid_height - 1)
                    if (x, y) not in self.snake and (x, y) != self.food and (x, y) not in self.obstacles:
                        self.obstacles.append((x, y))
                        break
        except Exception as e:
            logging.error(f"Failed to generate obstacles: {e}")
            raise

    def generate_power_up(self):
        """Generate a power-up at a random position"""
        try:
            if random.random() < 0.3:  # 30% chance to spawn power-up
                while True:
                    x = random.randint(0, self.grid_width - 1)
                    y = random.randint(0, self.grid_height - 1)
                    if (x, y) not in self.snake and (x, y) != self.food and (x, y) not in self.obstacles and (x, y) not in self.power_ups:
                        self.power_ups.append((x, y, random.choice(['speed', 'invincible', 'score'])))
                        break
        except Exception as e:
            logging.error(f"Failed to generate power-up: {e}")
            raise

    def handle_events(self):
        """Handle user input events"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.info("Game window closed by user")
                    return False
                
                elif event.type == pygame.KEYDOWN:
                    if self.game_over and event.key == pygame.K_SPACE:
                        # Restart game
                        self.__init__(self.width, self.height, self.cell_size)
                        return True
                    
                    elif not self.game_over:
                        # Change direction (prevent 180-degree turns)
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.direction = (1, 0)
                        elif event.key == pygame.K_p:
                            # Pause game
                            self.pause_game()
            
            return True
        except Exception as e:
            logging.error(f"Error handling events: {e}")
            return False

    def pause_game(self):
        """Pause the game"""
        try:
            paused = True
            font = pygame.font.Font(None, 72)
            pause_text = font.render("PAUSED", True, self.WHITE)
            pause_rect = pause_text.get_rect(center=(self.width//2, self.height//2))
            
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = False
                
                self.screen.fill(self.BLACK)
                self.draw()
                self.screen.blit(pause_text, pause_rect)
                pygame.display.flip()
                self.clock.tick(60)
        except Exception as e:
            logging.error(f"Error pausing game: {e}")

    def update(self):
        """Update game state"""
        try:
            if self.game_over:
                return
                
            # Move snake
            head_x, head_y = self.snake[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])
            
            # Check for collisions with walls
            if (new_head[0] < 0 or new_head[0] >= self.grid_width or 
                new_head[1] < 0 or new_head[1] >= self.grid_height):
                self.game_over = True
                logging.info("Game over: Snake hit the wall")
                return
            
            # Check for collisions with obstacles
            if not self.invincible and new_head in self.obstacles:
                self.game_over = True
                logging.info("Game over: Snake hit an obstacle")
                return
            
            # Check for collisions with self
            if new_head in self.snake:
                self.game_over = True
                logging.info("Game over: Snake collided with itself")
                return
            
            # Add new head
            self.snake.insert(0, new_head)
            
            # Check if food is eaten
            if new_head == self.food:
                self.score += 10
                self.food = self.generate_food()
                # Increase speed slightly with each food eaten
                self.speed = min(20, 10 + self.score // 50)
                
                # Generate power-up occasionally
                self.generate_power_up()
                
                # Level up every 50 points
                if self.score >= self.level * 50:
                    self.level += 1
                    logging.info(f"Level up! Current level: {self.level}")
                    
                logging.info(f"Food eaten! Score: {self.score}")
            else:
                # Remove tail if no food eaten
                self.snake.pop()
            
            # Update power-up timer
            if self.power_up_timer > 0:
                self.power_up_timer -= 1
                if self.power_up_timer == 0:
                    self.invincible = False
            
            # Check for power-up collection
            for i, power_up in enumerate(self.power_ups):
                if new_head == (power_up[0], power_up[1]):
                    # Apply power-up effect
                    if power_up[2] == 'speed':
                        self.speed = min(25, self.speed + 3)
                        logging.info("Speed power-up activated!")
                    elif power_up[2] == 'invincible':
                        self.invincible = True
                        self.power_up_timer = 300  # 5 seconds at 60 FPS
                        logging.info("Invincibility power-up activated!")
                    elif power_up[2] == 'score':
                        self.score += 50
                        logging.info("Score power-up activated!")
                    
                    # Remove collected power-up
                    self.power_ups.pop(i)
                    break
            
            # Occasionally generate new obstacles
            if random.random() < 0.01 and len(self.obstacles) < 20:
                self.generate_obstacles()
                
        except Exception as e:
            logging.error(f"Error updating game state: {e}")
            raise

    def draw(self):
        """Draw everything on the screen"""
        try:
            # Fill background
            self.screen.fill(self.BLACK)
            
            # Draw snake
            for i, (x, y) in enumerate(self.snake):
                if self.invincible and i == 0:
                    color = self.YELLOW  # Head is yellow when invincible
                else:
                    color = self.GREEN if i == 0 else (0, 200, 0)  # Head is brighter green
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)  # Border
            
            # Draw obstacles
            for (x, y) in self.obstacles:
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.PURPLE, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)  # Border
            
            # Draw power-ups
            for (x, y, power_type) in self.power_ups:
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                if power_type == 'speed':
                    pygame.draw.rect(self.screen, self.BLUE, rect)
                elif power_type == 'invincible':
                    pygame.draw.rect(self.screen, self.YELLOW, rect)
                elif power_type == 'score':
                    pygame.draw.rect(self.screen, self.RED, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)  # Border
            
            # Draw food
            rect = pygame.Rect(self.food[0] * self.cell_size, self.food[1] * self.cell_size, 
                             self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.RED, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 1)  # Border
            
            # Draw score and level
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, self.WHITE)
            level_text = font.render(f"Level: {self.level}", True, self.WHITE)
            high_score_text = font.render(f"High Score: {self.high_score}", True, self.WHITE)
            
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(level_text, (10, 50))
            self.screen.blit(high_score_text, (10, 90))
            
            # Draw invincibility indicator
            if self.invincible:
                invincible_text = font.render("INVINCIBLE", True, self.YELLOW)
                self.screen.blit(invincible_text, (self.width - 150, 10))
            
            # Draw game over screen
            if self.game_over:
                font_large = pygame.font.Font(None, 72)
                game_over_text = font_large.render("GAME OVER", True, self.RED)
                restart_text = font.render("Press SPACE to restart", True, self.WHITE)
                
                game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 50))
                restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
                
                self.screen.blit(game_over_text, game_over_rect)
                self.screen.blit(restart_text, restart_rect)
                
                # Update high score
                if self.score > self.high_score:
                    self.high_score = self.score
            
            pygame.display.flip()
            
        except Exception as e:
            logging.error(f"Error drawing game: {e}")
            raise

    def run(self):
        """Main game loop"""
        try:
            running = True
            while running:
                running = self.handle_events()
                if not self.game_over:
                    self.update()
                self.draw()
                self.clock.tick(60)
        except Exception as e:
            logging.error(f"Error in main game loop: {e}")
            raise

# Create and