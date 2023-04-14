from typing import List
import pygame
from colours import Colour


class Block:

    _template = []

    def __init__(self, x: int) -> None:
        self.size: int = len(self._template)
        self.depth: float = -self.size
        self.depth_target: int = self.depth
        self.x: float = x
        self.x_target: int = self.x
        self.colour: Colour = Colour.randomise()
        self.state: List[List[int]] = []
        self.previous_state: List[List[int]] = []

        self.load_state()

    def load_state(self) -> None:
        self.state = []
        for i in range(self.size):
            self.state.append([])
            for j in range(self.size):
                self.state[i].append(self._template[i][j])

    def save_previous_state(self) -> None:
        self.previous_state = []
        for i in range(self.size):
            self.previous_state.append([])
            for j in range(self.size):
                self.previous_state[i].append(self.state[i][j])

    def undo_rotation(self) -> None:
        self.state = self.previous_state

    def move_left(self) -> None:
        self.x_target -= 1

    def move_right(self) -> None:
        self.x_target += 1

    def move_down(self) -> None:
        self.depth_target += 1

    def animate_pos(self) -> None :
        p = 1/8.
        self.x += p * (self.x_target - self.x)
        self.depth += p * (self.depth_target - self.depth)

    def build_empty_block(self) -> List[List[int]]:
        block = []
        for r in range(self.size):
            row = []
            for c in range(self.size):
                row.append(0)
            block.append(row)
        return block

    def cw_rotation(self) -> None:
        self.save_previous_state()
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.state[self.size - c - 1][r]

        self.state = state

    def ccw_rotation(self) -> None:
        self.save_previous_state()
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.state[c][self.size - r - 1]

        self.state = state

    def double_rotation(self) -> None:
        self.save_previous_state()
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.state[self.size - r - 1][self.size - c - 1]

        self.state = state

    def print_pixel(self, row: int, col: int) -> bool:
        return bool(self.state[row][col])

    def draw_block(self, surface: pygame.Surface, size: float, padding: float) -> None:
            for row in range(self.size):
                for col in range(self.size):
                    if (row + self.depth_target) >= 0 and self.print_pixel(row, col):
                        pygame.draw.rect(
                            surface, self.colour.colour,
                            pygame.Rect(
                                padding * (col + self.x),
                                padding * (row + self.depth),
                                size, size
                            ), 0, 3)


class SquareBlock(Block):

    _template = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]


class LineBlock(Block):

    _template = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


class RightSBlock(Block):

    _template = [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ]


class LeftSBlock(Block):

    _template = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]


class RightLBlock(Block):

    _template = [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0],
    ]


class LeftLBlock(Block):

    _template = [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0],
    ]


class TBlock(Block):

    _template = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]


BLOCKS = [
    SquareBlock,
    LineBlock,
    LeftLBlock,
    RightLBlock,
    LeftSBlock,
    RightSBlock,
    TBlock
]