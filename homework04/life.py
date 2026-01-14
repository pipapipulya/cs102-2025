import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: float = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        r, c = cell
        neighbours = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbours.append(self.curr_generation[nr][nc])

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(False)

        for r in range(self.rows):
            for c in range(self.cols):
                alive = self.curr_generation[r][c]
                neighbours = sum(self.get_neighbours((r, c)))

                if alive:
                    new_grid[r][c] = 1 if neighbours in (2, 3) else 0
                else:
                    new_grid[r][c] = 1 if neighbours == 3 else 0

        return new_grid

    def step(self) -> None:
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename) as f:
            lines = [list(map(int, line.strip())) for line in f if line.strip()]

        rows = len(lines)
        cols = len(lines[0])

        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = lines
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join(map(str, row)) + "\n")
