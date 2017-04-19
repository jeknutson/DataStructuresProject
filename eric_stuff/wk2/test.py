#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	pygame.display.flip()
