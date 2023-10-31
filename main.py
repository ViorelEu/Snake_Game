import pygame
import sys
import random

class SnakeGame:
    def __init__(self, grid_size, window_width, window_height):
        self.grid_size = grid_size
        self.window_width = window_width
        self.window_height = window_height
        self.grid_width = window_width // grid_size
        self.grid_height = window_height // grid_size
        self.snake_head_img = pygame.image.load('snake_head.png')
        self.snake_body_img = pygame.image.load('snake_body.png')
        self.food_img = pygame.image.load('food.png')

        # Scaling factor for assets
        self.scale_factor = grid_size //10

        # Golden background color (RGB: 255, 215, 0)
        self.background_color = (255, 215, 0)

    def initialize(self):
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake Game')
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.snake_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.clock = pygame.time.Clock()

    def spawn_food(self):
        return (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake_direction != (0, 1):
                    self.snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.snake_direction != (0, -1):
                    self.snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.snake_direction != (1, 0):
                    self.snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.snake_direction != (-1, 0):
                    self.snake_direction = (1, 0)

    def move_snake(self):
        x, y = self.snake[0]
        new_head = ((x + self.snake_direction[0]) % self.grid_width, (y + self.snake_direction[1]) % self.grid_height)

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        # Set the background color to golden
        self.screen.fill(self.background_color)
        self.screen.blit(pygame.transform.scale(self.food_img, (self.grid_size * self.scale_factor, self.grid_size * self.scale_factor)), (self.food[0] * self.grid_size, self.food[1] * self.grid_size))
        for i, segment in enumerate(self.snake):
            if i == 0:
                self.screen.blit(pygame.transform.scale(self.snake_head_img, (self.grid_size * self.scale_factor, self.grid_size * self.scale_factor)), (segment[0] * self.grid_size, segment[1] * self.grid_size))
            else:
                self.screen.blit(pygame.transform.scale(self.snake_body_img, (self.grid_size * self.scale_factor, self.grid_size * self.scale_factor)), (segment[0] * self.grid_size, segment[1] * self.grid_size))
        pygame.display.update()

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.move_snake()
            self.draw()
            self.clock.tick(10)

        self.show_game_over()

    def show_game_over(self):
        font = pygame.font.Font(None, 36)
        game_over_text = font.render(f'Game Over! Score: {self.score}', True, (0, 0, 0))
        self.screen.blit(game_over_text, (self.window_width // 2 - 100, self.window_height // 2 - 18))
        pygame.display.update()
        pygame.time.wait(2000)

if __name__ == '__main__':
    pygame.init()
    window_width = 500  # Adjust the window dimensions as desired
    window_height = 800
    game = SnakeGame(20, window_width, window_height)
    game.initialize()
    game.run()
    pygame.quit()
    sys.exit()
