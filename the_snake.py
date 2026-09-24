"""Игра «Змейка» на Pygame."""

from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 5

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализирует объект с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране."""


class Apple(GameObject):
    """Класс яблока, которое собирает змейка."""

    def __init__(self, body_color=APPLE_COLOR):
        """Создаёт яблоко в случайной позиции."""
        super().__init__(position=(0, 0), body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает яблоко в случайную позицию на поле."""
        x = randint(0, GRID_WIDTH - 1)
        y = randint(0, GRID_HEIGHT - 1)
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко."""
        pixel_x = self.position[0] * GRID_SIZE
        pixel_y = self.position[1] * GRID_SIZE
        rect = pygame.Rect((pixel_x, pixel_y), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(
        self,
        positions=None,
        body_color=SNAKE_COLOR,
        length=1,
        direction=(1, 0),
        next_direction=None,
        last=None,
    ):
        """Инициализирует змейку с заданными позициями сегментов."""
        if positions is None:
            center_x = GRID_WIDTH // 2
            center_y = GRID_HEIGHT // 2
            positions = [
                (center_x, center_y),
                (center_x - 1, center_y),
                (center_x - 2, center_y),
            ]
        super().__init__(position=positions[0], body_color=body_color)
        self.body = list(positions)
        self.positions = self.body
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.body[0]

    def move(self, ate_apple=False):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        d_x, d_y = self.direction
        new_h_x = (head_x + d_x) % GRID_WIDTH
        new_h_y = (head_y + d_y) % GRID_HEIGHT
        new_head = (new_h_x, new_h_y)
        self.body.insert(0, new_head)
        if not ate_apple:
            self.last = self.body[-1]
            del self.body[-1]
        else:
            self.last = None

    def update_direction(self):
        """Применяет отложенное направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def cell_to_pixels(self, positions):
        """Преобразует координаты клетки в пиксели."""
        return positions[0] * GRID_SIZE, positions[1] * GRID_SIZE

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        for position in self.body:
            rect = pygame.Rect(
                self.cell_to_pixels(position),
                (GRID_SIZE, GRID_SIZE),
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.positions = self.body
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.position = self.body[0]


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш игроком."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Запускает основной игровой цикл."""
    pygame.init()
    start_positions = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
    ]
    snake = Snake(positions=start_positions, body_color=SNAKE_COLOR)
    apple = Apple(body_color=APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)
        snake.update_direction()

        ate_apple = False
        if snake.get_head_position() == apple.position:
            ate_apple = True
            apple.randomize_position()

        snake.move(ate_apple=ate_apple)

        head = snake.get_head_position()
        if head in snake.body[1:]:
            snake.reset()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
