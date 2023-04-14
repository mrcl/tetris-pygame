from typing import List
import pygame

from colours import Colour


class Block:

    def __init__(self, size: int, x: int) -> None:
        self.size: int = size
        self.depth: float = -size
        self.depth_target: int = self.depth
        self.x: float = x
        self.x_target: int = self.x
        self.colour: Colour = Colour.randomise()

    def move_left(self) -> None:
        self.x_target -= 1

    def move_right(self) -> None:
        self.x_target += 1

    def move_down(self) -> None:
        self.depth_target += 1

    def animate_pos(self):
        p = 1/5.
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
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.template[self.size - c - 1][r]

        self.template = state

    def ccw_rotation(self) -> None:
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.template[c][self.size - r - 1]

        self.template = state

    def double_rotation(self) -> None:
        state = self.build_empty_block()
        for r in range(self.size):
            for c in range(self.size):
                state[r][c] = self.template[self.size - r - 1][self.size - c - 1]

        self.template = state

    def print_pixel(self, row: int, col: int) -> bool:
        return bool(self.template[row][col])

    def draw_block(self, surface: pygame.Surface, size: float, padding: float) -> None:
            for row in range(self.size):
                for col in range(self.size):
                    if self.print_pixel(row, col):
                        pygame.draw.rect(
                            surface, self.colour.colour,
                            pygame.Rect(
                                padding * (col + self.x),
                                padding * (row + self.depth),
                                size, size
                            ), 0, 3)


class SquareBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ]
        super().__init__(len(self.template), x)

class LineBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        super().__init__(len(self.template), x)


class RightSBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ]
        super().__init__(len(self.template), x)


class LeftSBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ]
        super().__init__(len(self.template), x)


class RightLBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
        ]
        super().__init__(len(self.template), x)

class LeftLBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
        ]
        super().__init__(len(self.template), x)


class TBlock(Block):

    def __init__(self, x: int) -> None:
        self.template = [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ]
        super().__init__(len(self.template), x)


BLOCKS = [
    SquareBlock,
    LineBlock,
    LeftLBlock,
    RightLBlock,
    LeftSBlock,
    RightSBlock,
    TBlock
]