import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        rows = self.life.rows
        cols = self.life.cols

        for x in range(cols + 2):
            screen.addstr(0, x, "#")
            screen.addstr(rows + 1, x, "#")

        for y in range(rows + 2):
            screen.addstr(y, 0, "#")
            screen.addstr(y, cols + 1, "#")

    def draw_grid(self, screen) -> None:
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                char = "█" if cell == 1 else " "
                screen.addstr(i + 1, j + 1, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)

        try:
            while not self.life.is_max_generations_exceeded and self.life.is_changing:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                self.life.step()
                curses.napms(200)

        finally:
            curses.endwin()
