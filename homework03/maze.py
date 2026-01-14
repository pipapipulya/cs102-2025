from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

Cell = Union[str, int]
Coord = Tuple[int, int]
Path = List[Coord]

WALL = "■"
EMPTY = " "
EXIT = "X"


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Cell]]:
    return [[WALL] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Cell]], coord: Coord) -> List[List[Cell]]:
    x, y = coord
    cols = len(grid[0])

    dirs = []
    if x - 2 >= 1:
        dirs.append("U")
    if y + 2 <= cols - 2:
        dirs.append("R")

    if not dirs:
        return grid

    direction = choice(dirs)
    if direction == "U":
        grid[x - 1][y] = EMPTY
    else:
        grid[x][y + 1] = EMPTY

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Cell]]:
    grid = create_grid(rows, cols)
    empty_cells = []

    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = EMPTY
                empty_cells.append((x, y))

    for x, y in empty_cells:
        direction = choice(["up", "right"])
        can_up = x > 1
        can_right = y < cols - 2

        if direction == "up":
            if can_up:
                grid[x - 1][y] = EMPTY
            elif can_right:
                grid[x][y + 1] = EMPTY
        else:
            if can_right:
                grid[x][y + 1] = EMPTY
            elif can_up:
                grid[x - 1][y] = EMPTY

    if random_exit:
        x1, x2 = randint(0, rows - 1), randint(0, rows - 1)
        y1 = randint(0, cols - 1) if x1 in (0, rows - 1) else choice((0, cols - 1))
        y2 = randint(0, cols - 1) if x2 in (0, rows - 1) else choice((0, cols - 1))
    else:
        x1, y1 = 0, cols - 2
        x2, y2 = rows - 1, 1

    grid[x1][y1] = EXIT
    grid[x2][y2] = EXIT

    return grid


def get_exits(grid: List[List[Cell]]) -> List[Coord]:
    rows, cols = len(grid), len(grid[0])
    exits = []

    for i in range(rows):
        if grid[i][0] == EXIT:
            exits.append((i, 0))
        if grid[i][cols - 1] == EXIT:
            exits.append((i, cols - 1))

    for j in range(cols):
        if grid[0][j] == EXIT:
            exits.append((0, j))
        if grid[rows - 1][j] == EXIT:
            exits.append((rows - 1, j))

    return sorted(dict.fromkeys(exits))


def make_step(grid: List[List[Cell]], k: int) -> List[List[Cell]]:
    rows, cols = len(grid), len(grid[0])
    nk = k + 1

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                for ni, nj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0:
                        grid[ni][nj] = nk

    return grid


def shortest_path(grid: List[List[Cell]], exit_coord: Coord) -> Optional[Path]:
    x, y = exit_coord
    value = grid[x][y]

    if not isinstance(value, int) or value <= 0:
        return None

    path = [(x, y)]
    k = value

    while k != 1:
        cx, cy = path[-1]
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == k - 1:
                path.append((nx, ny))
                k -= 1
                break
        else:
            return None

    return path


def encircled_exit(grid: List[List[Cell]], coord: Coord) -> bool:
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    checks = []
    if x == 0:
        checks.append((1, y))
    if x == rows - 1:
        checks.append((rows - 2, y))
    if y == 0:
        checks.append((x, 1))
    if y == cols - 1:
        checks.append((x, cols - 2))

    for cx, cy in checks:
        if 0 <= cx < rows and 0 <= cy < cols and grid[cx][cy] == EMPTY:
            return False

    return True


def solve_maze(grid: List[List[Cell]]) -> Tuple[List[List[Cell]], Optional[Path]]:
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, [exits[0]] if exits else None

    entrance, exit_ = exits[0], exits[1]

    if encircled_exit(grid, entrance) or encircled_exit(grid, exit_):
        return grid, None

    work = deepcopy(grid)

    for i in range(len(work)):
        for j in range(len(work[0])):
            if work[i][j] == EMPTY:
                work[i][j] = 0

    work[entrance[0]][entrance[1]] = 1
    work[exit_[0]][exit_[1]] = 0

    k = 0
    while work[exit_[0]][exit_[1]] == 0:
        k += 1
        prev = deepcopy(work)
        make_step(work, k)
        if work == prev:
            return grid, None

    path = shortest_path(work, exit_)
    return grid, path


def add_path_to_grid(grid: List[List[Cell]], path: Optional[Path]) -> List[List[Cell]]:
    if path is None:
        return grid
    for x, y in path:
        grid[x][y] = EXIT
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    for row in MAZE:
        print(row)
