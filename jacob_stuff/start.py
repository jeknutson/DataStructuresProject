#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import sys, pygame, os, math, time
from time import sleep

pygame.init()
pygame.display.list_modes()
screen = pygame.display.set_mode((1200, 600))
#arrow = pygame.image.load("arrow.png")
arrow_angle = math.radians(90)
#arrow_width = int (180 / 5)
#arrow_length = int (130 / 5)
#arrow = pygame.transform.scale(arrow, (arrow_width, arrow_length))
clock = pygame.time.Clock()
#arrow = pygame.transform.rotate(arrow, arrow_angle)
done = False

p_color = (255, 0, 0)
p_xcord = 30
arrow_x = 30
arrow_y = 100
arrow_r = 20

ball_r = 5
ball_c = (0, 0, 0)
white = (255, 255, 255)
ball_t = 0
ball_x = 30
ball_y = 500
vel_x = 30
vel_y = 0

# Power bar
def progress(direction, p_xcord):
	if direction > 1 and p_xcord < 100:
		p_xcord = p_xcord+4
	elif direction < 1 and p_xcord > 0:
		p_xcord = p_xcord-4
	pygame.draw.rect(screen, p_color, pygame.Rect(30, 550, 30+p_xcord, 30))
	return p_xcord

def rotatearrow(direction):
	global arrow_x,arrow_y,arrow_angle
	if direction > 0:
		arrow_angle = arrow_angle + math.radians(-5)
	elif direction < 0:
		arrow_angle = arrow_angle + math.radians(5)
	x = arrow_x + arrow_r*math.cos(arrow_angle)
	y = arrow_y - arrow_r*math.sin(arrow_angle)
	pygame.draw.aaline(screen, (255,0,0),(arrow_x,arrow_y), (x,y))
	
# Ball movement
def moveball(color, new_x, new_y):
	#screen.blit(ball, (new_x, new_y))
	screen.fill((255, 255, 255))
	time.sleep(.04)
	#global ball_color, ball_radius, ball_thickness
	pygame.display.update(pygame.draw.circle(screen, color, (int(new_x), int(new_y)), ball_r, ball_t))

def hitball(angle, velocity):
	vel_y = velocity * math.sin(angle)
	vel_x = velocity * math.cos(angle)
	t = (vel_y / 9.8)* 2
	global ball_x, ball_y
	pos_x = ball_x
	pos_y = ball_y
	dt = t / 50
	while dt < t:
		vel_x = velocity * math.cos(angle)
		vel_y = velocity * math.sin(angle) * -1
		moveball(white, pos_x, pos_y)
		pos_x = ball_x + vel_x*dt
		pos_y = ball_y + vel_y*dt + 4.9*dt*dt
		print(pos_y)
		dt = dt + dt
		screen.fill((255, 255, 255))
		moveball(ball_c, pos_x, pos_y)
	moveball(white, pos_x, pos_y)
	pos_x = ball_x + vel_x*t
	pos_y = ball_y + vel_y*t + 4.9*t*t
	moveball(ball_c, pos_x, pos_y)
	ball_x = pos_x
	ball_y = pos_y

# Main loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_m:
				p_xcord = progress(2, p_xcord)
			if event.key == pygame.K_n:
				p_xcord = progress(0, p_xcord)
			if event.key == pygame.K_SPACE:
				hitball(arrow_angle, p_xcord) 
			if event.key == pygame.K_RIGHT:
				rotatearrow(1)
			if event.key == pygame.K_LEFT:
				rotatearrow(-1)

		
	screen.fill((255, 255, 255))
	moveball(ball_c, ball_x, ball_y)

	arrow_x = ball_x 
	arrow_y = ball_y
	x = arrow_x + arrow_r*math.cos(arrow_angle)
	y = arrow_y - arrow_r*math.sin(arrow_angle)
	pygame.draw.aaline(screen, (255,0,0),(arrow_x,arrow_y), (x,y))
	
	
	#Draw power bar
	pygame.draw.rect(screen, (0,0,0), pygame.Rect(30,550,132,30))
	pygame.draw.rect(screen, p_color, pygame.Rect(30,550,30+p_xcord,30))
	
	pygame.display.flip()
	clock.tick(60)
