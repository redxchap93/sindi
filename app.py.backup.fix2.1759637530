```python
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
        self.speed = 10  # Not used to control movement speed directly
        self.invincible = False
        self.power_up_timer = 0
        self.power_ups: List[Tuple[int, int, str]] = []

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        # Game objects
        self.snake: List[Tuple[int, int]] = [(10, 10), (9, 10), (8, 10)]
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
        if random.random() < 0.3:
            x = random.randint(0, (self.width // self.cell_size) - 1)
            y = random.randint(0, (self.height // self.cell_size) - 1)
            if (
                (x, y) not in self.snake
                and (x, y) not in self.obstacles
                and (x, y) != self.food
                and (x, y, "none") not in self.power_ups
            ):
                power_type = random