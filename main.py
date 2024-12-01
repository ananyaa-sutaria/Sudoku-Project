from sudoku_generator import Board
import pygame

def main():
    running = True
    screen = pygame.display.set_mode( (576, 576) )
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = event.pos
                b.select(row,col)


        screen.fill((0,0,0))
        b = Board(576, 576, screen, "easy")
        b.draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()