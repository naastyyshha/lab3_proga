import pygame
from pygame.locals import *
import random
import os

class Cell:
    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state


    def is_alive(self):
        return self.state



class CellList:
    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.grid = [[Cell(i, j, random.choice([True, False]) if randomize else False)
             for j in range(ncols)] for i in range(nrows)]

        # Для итератора
        self._current_row = 0
        self._current_col = 0


    def update(self):
        """Обновляет состояние всех клеток по правилам игры Жизнь"""
        # Создаём новую сетку с мёртвыми клетками
        new_grid = [[Cell(i, j, False) for j in range(self.ncols)]
            for i in range(self.nrows)]

        for i in range(self.nrows):
            for j in range(self.ncols):
                cell = self.grid[i][j]
                neighbours = self.get_neighbours(cell)
                live_count = sum(1 for n in neighbours if n.is_alive())

                if cell.is_alive():
                    if live_count in (2, 3):
                        new_grid[i][j].state = True
                else:
                    if live_count == 3:
                        new_grid[i][j].state = True

        self.grid = new_grid


    def get_neighbours(self, cell):
        """Возвращает список соседних клеток"""
        neighbours = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                ni, nj = cell.row + di, cell.col + dj
                if 0 <= ni < self.nrows and 0 <= nj < self.ncols:
                    neighbours.append(self.grid[ni][nj])
        return neighbours


    @classmethod
    def from_file(cls, filename):
        """Создаёт CellList из текстового файла с 0 и 1"""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл '{filename}' не найден")

        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        if not lines:
            raise ValueError("Файл пуст.")

        nrows = len(lines)
        ncols = len(lines[0])

        # Проверка, что все строки одинаковой длины
        for line in lines:
            if len(line) != ncols:
                raise ValueError("Все строки в файле должны иметь одинаковую длину")
            if not all(ch in '01' for ch in line):
                raise ValueError("Файл должен содержать только символы '0' и '1'")

        cell_list = cls(nrows, ncols, randomize=False)
        for i in range(nrows):
            for j in range(ncols):
                cell_list.grid[i][j].state = (lines[i][j] == '1')
        return cell_list


    def __iter__(self):
        self._current_row = 0
        self._current_col = 0
        return self


    def __next__(self):
        if self._current_row >= self.nrows:
            raise StopIteration
        cell = self.grid[self._current_row][self._current_col]
        self._current_col += 1
        if self._current_col >= self.ncols:
            self._current_row += 1
            self._current_col = 0
        return cell

    def __str__(self):
        return '\n'.join(
            '[' + ', '.join('1' if cell.is_alive() else '0' for cell in row) + ']'
            for row in self.grid)


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

        # Инициализируем список клеток
        self.cell_list = CellList(self.cell_height, self.cell_width, randomize=True)


    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                (0, y), (self.width, y))


    def draw_cell_list(self, cell_list):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        """
        for row in cell_list.grid:
            for cell in row:
                color = pygame.Color('green') if cell.is_alive() else pygame.Color('white')
                rect = (cell.col * self.cell_size, cell.row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.screen.fill(pygame.Color('white'))
        pygame.display.set_caption('Game of Life')
        paused = False
        running = True

        # Обновлен running
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused  # Пауза по нажатию пробела

            self.draw_cell_list(self.cell_list)
            self.draw_grid()

            if not paused:
                self.cell_list.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == '__main__':
    game = GameOfLife(width=640, height=480, cell_size=20, speed=5)
    game.run()
