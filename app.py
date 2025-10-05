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
            
            # Game state
            self.snake = [(self.grid_width // 2, self.grid_height // 2)]
            self.direction = (1, 0)  # Start moving right
            self.food = self.generate_food()
            self.score = 0
            self.game_over = False
            self.speed = 10
            
            logging.info("Snake game initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize Snake game: {e}")
            raise

    def generate_food(self) -> Tuple[int, int]:
        """
        Generate food at a random position not occupied by the snake
        
        Returns:
            Tuple of (x, y) coordinates for food
        """
        try:
            while True:
                x = random.randint(0, self.grid_width - 1)
                y = random.randint(0, self.grid_height - 1)
                if (x, y) not in self.snake:
                    return (x, y)
        except Exception as e:
            logging.error(f"Failed to generate food: {e}")
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
            
            return True
        except Exception as e:
            logging.error(f"Error handling events: {e}")
            return False

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
                logging.info(f"Food eaten! Score: {self.score}")
            else:
                # Remove tail if no food eaten
                self.snake.pop()
                
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
                color = self.GREEN if i == 0 else (0, 200, 0)  # Head is brighter green
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)  # Border
            
            # Draw food
            food_rect = pygame.Rect(self.food[0] * self.cell_size, 
                                  self.food[1] * self.cell_size,
                                  self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.RED, food_rect)
            pygame.draw.rect(self.screen, self.WHITE, food_rect, 1)  # Border
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, self.WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # Draw game over message
            if self.game_over:
                game_over_font = pygame.font.Font(None, 72)
                game_over_text = game_over_font.render("GAME OVER", True, self.RED)
                restart_font = pygame.font.Font(None, 36)
                restart_text = restart_font.render("Press SPACE to restart", True, self.WHITE)
                
                # Center the text
                game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 30))
                restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 30))
                
                self.screen.blit(game_over_text, game_over_rect)
                self.screen.blit(restart_text, restart_rect)
            
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
                if not running:
                    break
                    
                self.update()
                self.draw()
                
                # Control game speed
                self.clock.tick(self.speed)
                
            logging.info("Game loop ended")
            
        except Exception as e:
            logging.error(f"Error in main game loop: {e}")
            raise

def main():
    """Main entry point for the Snake game"""
    try:
        logging.info("Starting Snake Game")
        
        # Create and run the game
        game = SnakeGame()
        game.run()
        
        logging.info("Snake Game finished successfully")
        
    except Exception as e:
        logging.error(f"Failed to run Snake game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()