import time
import pygame
from pygame.event import Event
from random import choice
from tetris_blocks import Block, BLOCKS

REMOVE_COMPLETED_EVENT = pygame.USEREVENT + 1


class TetrisBoard:

    def __init__(self, n_cols: int, n_rows: int) -> None:
        self.score: int = 0
        self.level: int = 1
        self._n_cols: int = n_cols
        self._n_rows: int = n_rows
        self._board = None
        self.reset_board()
        self.block_size: int = 30
        self.padding: int = 1
        self.padded_block: int = (self.block_size + 2 * self.padding)
        self.surface: pygame.Surface = pygame.display.set_mode((self._n_cols * self.padded_block, self._n_rows * self.padded_block))

        self.last_block_step: float = time.time()
        self.step_interval: float = 0.5

        self.add_new_block()
        self.valid_game: bool = True

        self.completed_rows: list = []

        self.print_score()

    def print_score(self):
        title = 'Tetris' if self.valid_game else 'Game Over'
        level = 'lv-%02d' % self.level

        pygame.display.set_caption('%s - %04d - %s' % (title, self.score, level))

    def add_new_block(self) -> None:
        self.block: Block = choice(BLOCKS)(3)
        for n in range(choice([1, 2, 3])):
            self.block.cw_rotation()

    def block_is_inside_the_board(self) -> bool:
        for row in range(self.block.size):
            for col in range(self.block.size):
                if self.block and self.block.print_pixel(row, col) and (row + self.block.depth_target) < 0:
                    return False
        return True

    def detect_collision(self, side_step: int = 0, vertical_step: int = 0) -> bool:
        for row in range(self.block.size):
            for col in range(self.block.size):
                if self.block and self.block.print_pixel(row, col):
                    row_pos = row + vertical_step + self.block.depth_target
                    col_pos = col + side_step + self.block.x_target
                    side_collision = col_pos < 0 or col_pos >= self._n_cols
                    bottom_collision = row_pos >= self._n_rows
                    if side_collision or bottom_collision or (row_pos >= 0 and self._board[row_pos][col_pos]):
                        return True
        return False

    def move_left(self) -> None:
        if not self.detect_collision(-1):
            self.block.move_left()

    def move_right(self) -> None:
        if not self.detect_collision(+1):
            self.block.move_right()

    def move_down(self) -> bool:
        if self.detect_collision(vertical_step=1):
            if not self.block_is_inside_the_board():
                self.game_over()
            return False
        else:
            self.block.move_down()
            return True

    def reset_board(self) -> None:
        self._board = []
        for row in range(self._n_rows):
            row = []
            for col in range(self._n_cols):
                row.append(None)
            self._board.append(row)

    def draw_grid(self) -> None:
        for row in range(self._n_rows):
            for col in range(self._n_cols):
                if self._board[row][col]:
                    if row in self.completed_rows:
                        pygame.draw.rect(
                            self.surface, self._board[row][col].colour,
                            pygame.Rect(
                                self.padded_block * col,
                                self.padded_block * row,
                                self.block_size,
                                self.block_size
                            ), 2, 3)
                    else:
                        pygame.draw.rect(self.surface, self._board[row][col].colour, pygame.Rect(self.padded_block * col, self.padded_block * row, self.block_size, self.block_size), 0, 3)

    def draw_block(self) -> None:
        if self.valid_game and self.block:
            self.block.draw_block(self.surface, self.block_size, self.padded_block)

    def incorporate_block_to_pile(self) -> None:
        for row in range(self.block.size):
            for col in range(self.block.size):
                if self.block and self.block.print_pixel(row, col) and (row + self.block.depth + 1) >= 0:
                    self._board[row + self.block.depth_target][col + self.block.x_target] = self.block.colour

    def increment_level(self) -> None:
        self.level += 1
        self.step_interval *= 0.9

    def update_score(self) -> None:
        self.score += 1
        if self.score % 10 == 0:
            self.increment_level()

        self.print_score()

    def process_completed_rows(self) -> None:
        self.completed_rows = []
        for ri, row in enumerate(self._board):
            if ri not in self.completed_rows and all(row):
                self.completed_rows.append(ri)
                self.update_score()

        if len(self.completed_rows):
            pygame.time.set_timer(REMOVE_COMPLETED_EVENT, 200, True)

    def remove_completed_rows(self) -> None:
        if len(self.completed_rows):
            for ri in self.completed_rows:
                self._board.pop(ri)
                self._board.insert(0,[None] * self._n_cols)

            self.completed_rows = []
        self.process_completed_rows()

    def process_frame(self) -> None:
        t = time.time()
        if t - self.last_block_step >= self.step_interval and self.valid_game:
            if not self.move_down():
                self.incorporate_block_to_pile()
                self.process_completed_rows()
                self.add_new_block()
            self.last_block_step = t

        self.animate()
        self.draw_scene()

    def game_over(self) -> None:
        self.incorporate_block_to_pile()
        print("Game Over")
        self.valid_game = False
        self.print_score()

    def draw_scene(self) -> None:
        self.surface.fill((0, 0, 0))
        self.draw_grid()
        self.draw_block()

    def rotate_block(self) -> None:
        self.block.cw_rotation()
        if self.detect_collision():
            self.block.undo_rotation()

    def event(self, event: Event) -> None:
        if self.valid_game:
            match event.key:
                case pygame.K_UP:
                    self.rotate_block()
                case pygame.K_LEFT:
                    self.move_left()
                case pygame.K_RIGHT:
                    self.move_right()
                case pygame.K_DOWN:
                    self.move_down()

    def animate(self) -> None:
        self.block.animate_pos()