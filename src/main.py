import pygame
from tetris_board import TetrisBoard, REMOVE_COMPLETED_EVENT


def main() -> None:
    # Initializing Pygame
    pygame.init()
    clock = pygame.time.Clock()

    running = True

    board_size = (8, 16)

    tetris_board = TetrisBoard(*board_size)

    while running:
        clock.tick(240)
        for event in pygame.event.get():
            # Did the user hit a key?

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tetris_board = TetrisBoard(*board_size)
                else:
                    tetris_board.event(event)

            elif event.type == REMOVE_COMPLETED_EVENT:
                tetris_board.remove_completed_rows()

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

        tetris_board.process_frame()
        pygame.display.flip()


if __name__ == '__main__':
    main()