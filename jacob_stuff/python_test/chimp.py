#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((640, 480))
player = pygame.image.load('player.bmp').convert()
background = pygame.image.load('background.bmp').convert()
screen.blit(background, (0, 0))
objects = []

