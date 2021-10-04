# Importing the library
import time
import pygame

from random import choice
from typing import List
from pygame import time as pg_time
from pygame.event import Event


COLOURS = [
    (254, 67, 101),
    (252, 157, 154),
    (249, 205, 173),
    (200, 200, 169),
    (131, 175, 155),
]


class Colour:

    def __init__(self, r: int=0, g: int=0, b: int=0):
        self.r = r
        self.g = g
        self.b = b

    @property
    def colour(self):
        return (self.r, self.g, self.b)

    @classmethod
    def randomise(cls) -> 'Colour':
        instance = Colour()
        colour = choice(COLOURS)
        instance.r = colour[0]
        instance.g = colour[1]
        instance.b = colour[2]
        return instance


class Block:

    def __init__(self, size: int) -> None:
        self.size = size

    def build_empty_block(self) -> List[List[int]]:
        block = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(0)
            block.append(row)
        return block

    def cw_rotation(self):
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.template[self.size - c - 1][r]

        self.template = state

    def ccw_rotation(self):
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.template[c][self.size - r - 1]

        self.template = state

    def double_rotation(self):
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.template[self.size - r - 1][self.size - c - 1]

        self.template = state

    def print_pixel(self, row: int, col: int) -> bool:
        return bool(self.template[row][col])


class SquareBlock(Block):

    def __init__(self) -> None:
        self.template = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ]
        super().__init__(len(self.template))

class LineBlock(Block):

    def __init__(self) -> None:
        self.template = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        super().__init__(len(self.template))


class RightSBlock(Block):

    def __init__(self) -> None:
        self.template = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ]
        super().__init__(len(self.template))


class LeftSBlock(Block):

    def __init__(self) -> None:
        self.template = [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ]
        super().__init__(len(self.template))


class RightLBlock(Block):

    def __init__(self) -> None:
        self.template = [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
        ]
        super().__init__(len(self.template))

class LeftLBlock(Block):

    def __init__(self) -> None:
        self.template = [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
        ]
        super().__init__(len(self.template))


BLOCKS = [
    SquareBlock,
    LineBlock,
    LeftLBlock,
    RightLBlock,
    LeftSBlock,
    RightSBlock
]


class TetrisBoard:

    def __init__(self, n_cols: int, n_rows: int) -> None:
        self._n_cols = n_cols
        self._n_rows = n_rows
        self._board = None
        self.reset_board()
        self.block_size = 60
        self.padding = 1
        self.padded_block = (self.block_size + 2 * self.padding)
        self.surface = pygame.display.set_mode((self._n_cols * self.padded_block, self._n_rows * self.padded_block))

        self.last_block_step = time.time()
        self.step_iterval = 0.5

        self.add_new_block()
        self.valid_game = True

    def add_new_block(self):
        self.block = choice(BLOCKS)()
        self.block_colour = Colour.randomise()
        self.block_depth = 0
        self.block_pos = 3


    def detect_collision(self, side_step: int = 0, vertical_step: int = 0):
        for row in range(self.block.size):
            for col in range(self.block.size):
                if self.block and self.block.print_pixel(row, col):
                    col_pos = col + side_step + self.block_pos
                    row_pos = row + vertical_step + self.block_depth
                    side_collision = col_pos < 0 or col_pos >= self._n_cols
                    bottom_collision = row_pos >= self._n_rows
                    if side_collision or bottom_collision or self._board[row_pos][col_pos]:
                        return True
        return False

    def move_left(self):
        if not self.detect_collision(-1):
            self.block_pos -= 1

    def move_right(self):
        if not self.detect_collision(+1):
            self.block_pos += 1

    def move_down(self) -> bool:
        if not self.detect_collision(vertical_step=1):
            self.block_depth += 1
            return True
        else:
            return False

    def reset_board(self):
        self._board = []
        for row in range(self._n_rows):
            row = []
            for col in range(self._n_cols):
                row.append(None)
            self._board.append(row)

    def draw_grid(self):
        for row in range(self._n_rows):
            for col in range(self._n_cols):
                if self._board[row][col]:
                    pygame.draw.rect(self.surface, self._board[row][col].colour, pygame.Rect(self.padded_block * col, self.padded_block * row, self.block_size, self.block_size), 2, 3)

    def draw_block(self):
        if self.valid_game:
            for row in range(self.block.size):
                for col in range(self.block.size):
                    if self.block and self.block.print_pixel(row, col):
                        pygame.draw.rect(self.surface, self.block_colour.colour, pygame.Rect(self.padded_block * (col + self.block_pos), self.padded_block * (row + self.block_depth), self.block_size, self.block_size), 0, 3)

    def incorporate_block_to_pile(self):
        for row in range(self.block.size):
            for col in range(self.block.size):
                if self.block and self.block.print_pixel(row, col):
                    self._board[row + self.block_depth][col + self.block_pos] = self.block_colour

    def process_completed_row(self):
        completed_rows = []
        for ri, row in enumerate(self._board):
            if all(row):
                completed_rows.append(ri)

        if len(completed_rows):
            for ri in reversed(completed_rows):
                self._board.pop(ri)
            len(self._board)

            self._board = [[None] * self._n_cols] * len(completed_rows) + self._board

    def process_frame(self):
        t = time.time()
        if t - self.last_block_step >= self.step_iterval and self.valid_game:
            if not self.move_down():
                self.incorporate_block_to_pile()
                self.process_completed_row()
                self.add_new_block()
                if self.detect_collision():
                    self.game_over()
            self.last_block_step = t

        self.draw_scene()

    def game_over(self):
        print("Game Over")
        self.valid_game = False

    def draw_scene(self):
        self.surface.fill((0, 0, 0))
        self.draw_grid()
        self.draw_block()

    def event(self, event: Event) -> None:
        try:
            {
                pygame.K_UP: self.block.cw_rotation,
                pygame.K_LEFT: self.move_left,
                pygame.K_RIGHT: self.move_right,
                pygame.K_DOWN: self.move_down,
            }[event.key]()
        except KeyError:
            pass


def main():
    # Initializing Pygame
    pygame.init()
    clock = pg_time.Clock()

    running = True

    tetris_board = TetrisBoard(8, 16)

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                tetris_board.event(event)

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

        tetris_board.process_frame()
        pygame.display.flip()
if __name__ == '__main__':
    main()