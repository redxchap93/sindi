import pygame
import sys
import random
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class SnakeGame:
    def __init__(self, width: int = 800, height: int = 600, cell_size: int = 20):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Game state variables
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.speed = 10  # base speed
        self.invincible = False
        self.power_up_timer = 0  # in milliseconds
        self.power_ups: List[Tuple[int, int, str]] = []

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        # Game objects
        self.snake: List[Tuple[int, int]] = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)  # moving right initially
        self.obstacles: List[Tuple[int, int]] = []
        self.food: Tuple[int, int] = self.generate_food()
        self.game_over = False

        # Generate initial obstacles
        self.generate_obstacles()
        logging.info("Game initialized.")

    def generate_food(self) -> Tuple[int, int]:
        """Generate a new food position not colliding with snake or obstacles."""
        while True:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                return (x, y)

    def generate_obstacles(self):
        """Generate obstacles avoiding snake and food."""
        max_obstacles = 20
        while len(self.obstacles) < max_obstacles:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (
                (x, y) not in self.snake
                and (x, y) not in self.obstacles
                and (x, y) != self.food
            ):
                self.obstacles.append((x, y))

    def generate_power_up(self):
        """Occasionally generate a power‑up."""
        if random.random() < 0.01:  # 1% chance each frame
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (
                (x, y) not in self.snake
                and (x, y) not in self.obstacles
                and (x, y) != self.food
                and (x, y, "invincibility") not in self.power_ups
            ):
                self.power_ups.append((x, y, "invincibility"))
                logging.info(f"Power‑up generated at {(x, y)}")

    def handle_input(self):
        """Process user input to change direction or quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.direction = (1, 0)

    def update(self):
        """Update game state: move snake, handle collisions, power‑ups."""
        # Move snake
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if not (0 <= new_head[0] < self.width // self.cell_size) or not (
            0 <= new_head[1] < self.height // self.cell_size
        ):
            self.game_over = True
            return

        # Check self collision
        if new_head in self.snake and not self.invincible:
            self.game_over = True
            return

        # Check obstacle collision
        if new_head in self.obstacles and not self.invincible:
            self.game_over = True
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.food = self.generate_food()
            # Increase level every 50 points
            if self.score % 50 == 0:
                self.level += 1
        else:
            # Remove tail
            self.snake.pop()

        # Check power‑up collision
        for pu in self.power_ups:
            if new_head == (pu[0], pu[1]):
                if pu[2] == "invincibility":
                    self.invincible = True
                    self.power_up_timer = 5000  # 5 seconds
                self.power_ups.remove(pu)
                break

        # Update power‑up timer
        if self.invincible:
            self.power_up_timer -= self.clock.get_time()
            if self.power_up_timer <= 0:
                self.invincible = False
                self.power_up_timer = 0

        # Generate new power‑up occasionally
        self.generate_power_up()

    def draw(self):
        """Render all game elements."""
        self.screen.fill((0, 0, 0))

        # Draw food
        food_rect = pygame.Rect(
            self.food[0] * self.cell_size,
            self.food[1] * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.rect(self.screen, (255, 0, 0), food_rect)

        # Draw obstacles
        for obs in self.obstacles:
            obs_rect = pygame.Rect(
                obs[0] * self.cell_size,
                obs[1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, (100, 100, 100), obs_rect)

        # Draw power‑ups
        for pu in self.power_ups:
            pu_rect = pygame.Rect(
                pu[0] * self.cell_size,
                pu[1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, (0, 255, 255), pu_rect)

        # Draw snake
        for segment in self.snake:
            seg_rect = pygame.Rect(
                segment[0] * self.cell_size,
                segment[1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, (0, 255, 0), seg_rect)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

        # Draw level
        level_surf = font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(level_surf, (10, 50))

        # Draw invincibility timer
        if self.invincible:
            timer_surf = font.render(
                f"Invincible: {self.power_up_timer // 1000 + 1}s", True, (255, 255, 0)
            )
            self.screen.blit(timer_surf, (10, 90))

        pygame.display.flip()

    def run(self):
        """Main game loop."""
        while not self.game_over:
            self.handle_input()
            self.update()
            self.draw()
            # Speed increases with level
            self.clock.tick(self.speed + (self.level - 1) * 2)

        # Game over screen
        font = pygame.font.SysFont(None, 72)
        over_surf = font.render("Game Over", True, (255, 0, 0))
        over_rect = over_surf.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(over_surf, over_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()