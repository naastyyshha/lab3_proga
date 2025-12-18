import pygame
from pygame.locals import *
import random


class Cell:

    def __init__(self, row, col, state=False):
        pass

    def is_alive(self):
        pass


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        pass

    def update(self):
        pass

    def get_neighbours(self, cell):
        pass



class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создаём начальное состояние поля
        self.grid = self.cell_list(randomize=True)


    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (0, y), (self.width, y))

    def cell_list(self, randomize=False):
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1.
        В противном случае клетка считается мертвой, то
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(0, self.cell_width)]
            for _ in range(self.cell_height)]
        return [[0 for _ in range(0, self.cell_width)]
                for _ in range(self.cell_height)]

    def draw_cell_list(self, rects):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        for i in range(len(rects)):
            for j in range(len(rects[i])):
                color = pygame.Color('green') if rects[i][j] == 1 else pygame.Color('white')
                rect = (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell):
        """
        Вернуть список соседних клеток для клетки cell.

        Соседними считаются клетки по горизонтали,
        вертикали и диагоналям, то есть во всех
        направлениях.
        """
        row, col = cell
        neighbours = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                ni, nj = row + di, col + dj
                if 0 <= ni < self.cell_height and 0 <= nj < self.cell_width:
                    neighbours.append(self.grid[ni][nj])
        return neighbours

    def update_cell_list(self, cell_list):
        """
        Обновление состояния клеток
        """
        new_grid = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = self.get_neighbours((i, j))
                live_neighbours = sum(neighbours)

                if cell_list[i][j] == 1:
                    # Живая клетка
                    if live_neighbours in (2, 3):
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    # Мёртвая клетка
                    if live_neighbours == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0

        return new_grid

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_cell_list(self.grid)
            self.draw_grid()
            pygame.display.flip()

            # Обновляем состояние
            self.grid = self.update_cell_list(self.grid)

            clock.tick(self.speed)
        pygame.quit()


game = GameOfLife(320, 240, 20)
game.run()


