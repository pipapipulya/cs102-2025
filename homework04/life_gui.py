import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed

        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        self.screen.fill((0, 0, 0))  # background

        for r in range(self.life.rows):
            for c in range(self.life.cols):
                if self.life.curr_generation[r][c] == 1:
                    pygame.draw.rect(
                        self.screen,
                        (0, 200, 0),
                        (
                            c * self.cell_size,
                            r * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

        self.draw_lines()
        pygame.display.flip()

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(self.speed)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            if self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()

            self.draw_grid()

        pygame.quit()
