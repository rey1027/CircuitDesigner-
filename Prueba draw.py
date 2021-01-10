import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60
WIDTH = 600
HEIGHT = 500
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ballx = WIDTH / 2
bally = HEIGHT / 2
ball_vel = [1, 1]
ball_pos =(ballx, bally)
RADIUS = 20

# Game Loop:
while True:
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Erase the screen (I have tried with and without this step)
    DISPLAYSURF.fill(BLACK)

    # Update circle position
    ballx += ball_vel[0]
    bally += ball_vel[1]
    ball_pos =(ballx, bally)

    # Draw Circle (I have tried with and without locks/unlocks)
    pygame.draw.circle(DISPLAYSURF, WHITE, ball_pos, RADIUS, 2)

    # Update the screen
    pygame.display.flip()
    fpsClock.tick(FPS)