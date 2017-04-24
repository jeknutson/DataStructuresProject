#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import sys
import pygame
import os
import random
import bisect

#pygame.init()

size = width, height = 1200, 600

screen = pygame.display.set_mode(size)
running = 1
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0

#def draw_lines(line, width, height, color_dict=None):
#	sampled_line = []
#	for i in range(len(line)-1):
#		sampled_line = sampled_line + [line[i]]
#		if line[i+1][0]-line[i][0] > 1:
#			m = float(line[i+1][1]-line[i][1])/(line[i+1][0]-line[i][0])
#			n = line[i][1]-m*line[i][0]
#			r = lambda x: m*x+n
#			for j in range(line[i][0]+1, line[i+1][0]):
#				sampled_line = sampled_line + [[j, r(j)]]
#	for x in range(len(sampled_line[i])-1):
#		pygame.draw.aaline(screen, green, (sampled_line[1][x][0],height-sampled_line[1][x][1]), (sample_line[1][x][0],height))
		

def midpt_disp(start, end, roughness, v_d = None, num_i = 16):
	if v_d is None:
		v_d = (start[1]+end[1])/2
	points = [start, end]
	iteration = 1
	while iteration <= num_i:
		points_tup = tuple(points)
		for i in range(len(points_tup)-1):
			midpt = list(map(lambda x: (points_tup[i][x]+points_tup[i+1][x])/2, [0, 1]))
			midpt[1] = midpt[1] + random.choice([-v_d, v_d])
			bisect.insort(points, midpt)
		v_d *= 2 ** (-roughness)
		iteration = iteration + 1
	return points

line = midpt_disp([0+50, height/2], [width-50, height/2], 1.4, 20, 12)
line2 = midpt_disp([0+50, height/2], [width-50, height/2], 2.0, 250, 12)
for i in range(len(line)):
	print((line[i-1][0],line[i-1][1]),(line[i][0], line[i][1]))

it = 0
while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0

	screen.fill(black)

#	pygame.draw.line(screen, white, (0,height/2), (width, height/2))
	pygame.draw.line(screen, green, (0, height/2), (50, height/2))
	pygame.draw.line(screen, green, (width-50, height/2), (width, height/2))
	pygame.draw.ellipse(screen, (20,70,15), [width-33, height/2-4, 16, 8])
	pygame.draw.line(screen, (200,200,200), (width-25, height/2), (width-25, height/2-20))
	pygame.draw.polygon(screen, red, [[width-25, height/2-20],[width-25, height/2-15],[width-35, height/2-18+(it%3)]])

	i = 1
	while i < (len(line)):
		pygame.draw.aaline(screen, green, (line[i-1][0],line[i-1][1]),(line[i][0], line[i][1]))
		pygame.draw.aaline(screen, blue, (line2[i-1][0],line2[i-1][1]),(line2[i][0], line2[i][1]))	
		i = i + 1

	it = it + 1
	pygame.display.flip()
