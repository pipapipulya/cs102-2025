import random
import typing as tp

import pygame
from pygame.locals import QUIT

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        width: int = 640,
        height: int = 480,
        cell_size: int = 10,
        speed: int = 10,
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen = pygame.display.set_mode((width, height))

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed

        self.grid: Grid = self.create_grid(randomize=True)
        self.prev_grid: Grid = self.create_grid(randomize=False)
        self.generations: int = 1

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)
        self.prev_grid = self.create_grid(randomize=False)
        self.generations = 1

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.fill(pygame.Color("white"))
            self.draw_lines()
            self.draw_grid()
            self.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid: Grid = []

        for _ in range(self.cell_height):
            if randomize:
                row = [random.randint(0, 1) for _ in range(self.cell_width)]
            else:
                row = [0 for _ in range(self.cell_width)]
            grid.append(row)

        return grid

    def draw_grid(self) -> None:
        for r in range(self.cell_height):
            for c in range(self.cell_width):
                color = pygame.Color("green") if self.grid[r][c] == 1 else pygame.Color("white")
                rect = pygame.Rect(
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        r, c = cell
        out: Cells = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.cell_height and 0 <= nc < self.cell_width:
                    out.append(self.grid[nr][nc])

        return out

    def get_next_generation(self) -> Grid:
        new_grid: Grid = self.create_grid(randomize=False)

        for r in range(self.cell_height):
            for c in range(self.cell_width):
                alive = self.grid[r][c] == 1
                alive_cnt = sum(self.get_neighbours((r, c)))

                if alive:
                    new_grid[r][c] = 1 if alive_cnt in (2, 3) else 0
                else:
                    new_grid[r][c] = 1 if alive_cnt == 3 else 0

        return new_grid

    def step(self) -> None:
        self.prev_grid = [row[:] for row in self.grid]
        self.grid = self.get_next_generation()
        self.generations += 1
