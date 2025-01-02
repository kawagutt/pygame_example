import pygame
import random

class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'

    def change_direction(self, new_direction):
        if new_direction == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        if new_direction == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        if new_direction == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        if new_direction == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def move(self, food_position):
        if self.direction == 'RIGHT':
            self.position[0] += 10
        if self.direction == 'LEFT':
            self.position[0] -= 10
        if self.direction == 'UP':
            self.position[1] -= 10
        if self.direction == 'DOWN':
            self.position[1] += 10
        self.body.insert(0, list(self.position))
        if self.position == food_position:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self, width, height):
        if self.position[0] > width - 10 or self.position[0] < 0:
            return True
        if self.position[1] > height - 10 or self.position[1] < 0:
            return True
        for body_part in self.body[1:]:
            if self.position == body_part:
                return True
        return False

    def get_head_position(self):
        return self.position

    def get_body(self):
        return self.body

class Food:
    def __init__(self, width, height):
        self.position = [random.randrange(1, (width//10)) * 10, 
                         random.randrange(1, (height//10)) * 10]
        self.is_food_on_screen = True

    def spawn_food(self, width, height):
        if not self.is_food_on_screen:
            self.position = [random.randrange(1, (width//10)) * 10, 
                             random.randrange(1, (height//10)) * 10]
            self.is_food_on_screen = True
        return self.position

    def set_food_on_screen(self, bool_value):
        self.is_food_on_screen = bool_value

class Game:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food(self.width, self.height)
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                if event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                if event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                if event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')

    def update(self):
        if self.snake.move(self.food.position):
            self.score += 1
            self.food.set_food_on_screen(False)
        self.food.spawn_food(self.width, self.height)
        if self.snake.check_collision(self.width, self.height):
            self.game_over()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for pos in self.snake.get_body():
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(self.food.position[0], self.food.position[1], 10, 10))
        pygame.display.update()

    def game_over(self):
        font = pygame.font.SysFont('times new roman', 90)
        game_over_surface = font.render('Game Over', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect()
        game_over_rect.midtop = (self.width/2, self.height/4)
        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(15)

if __name__ == "__main__":
    game = Game()
    game.run()
