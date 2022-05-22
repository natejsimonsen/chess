import pygame
from Grid import Grid

# config variables
WIDTH = 1080
HEIGHT = 720
FPS = 20
HOST = '137.184.86.45'
#HOST = '127.0.0.1'
PORT = 9000

# pygame setup
pygame.init()
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# custom class setup
grid = Grid(screen, WIDTH, HEIGHT, HOST, PORT)
grid.generate_board("")

# game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            grid.stop()
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEMOTION:
            grid.on_hover(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid.on_click(event)

    grid.draw_board()
    pygame.display.update()
