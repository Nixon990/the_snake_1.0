"""the_snake.py"""
from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Направление движения змейки:
DIRECTIONS = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс."""

    def __init__(self) -> None:
        """Инициализация двух атрибутов."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def _draw_cell(self, position=None, color=None):
        if position is None:
            position = self.position

        if color is None:
            color = self.body_color

        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка объекта."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, snake_positions, color=APPLE_COLOR):
        """Инициализация яблока."""
        super().__init__()
        self.randomize_position(snake_positions)
        self.body_color = color

    def randomize_position(self, snake_positions):
        """Возврат случайной позиции."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in snake_positions:
                return position

    def spawn(self, snake_positions):
        """Рандомное перемещение яблока в свободную клетку."""
        self.position = self.randomize_position(snake_positions)

    def draw(self):
        """Отрисовка яблока."""
        self._draw_cell()


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.length = 1
        self.reset()

    def get_head_position(self):
        """Возврат позиции головы."""
        return self.positions[0]

    def move(self):
        """Логика движения змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_box = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_box)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def grow(self):
        """Увеличение в длину."""
        if self.last:
            self.positions.append(self.last)

    def update_direction(self, next_direction):
        """Обновление направления движения змейки."""
        if next_direction:
            self.direction = next_direction

    def draw(self):
        """Отрисовка змейки."""
        if self.last:
            self._draw_cell(self.last, BOARD_BACKGROUND_COLOR)

        for position in self.positions[:-1]:
            self._draw_cell(position)

        self._draw_cell(self.positions[0])

    def reset(self):
        """Сброс змейки."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None
        self.length = 1


def handle_keys(game_object):
    """Обработка нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit

            return DIRECTIONS.get(
                (event.key, game_object.direction),
                game_object.direction
            )

    return None


def main():
    """Игровой цикл."""
    pg.init()
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        next_direction = handle_keys(snake)
        snake.update_direction(next_direction)
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.spawn(snake.positions)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
