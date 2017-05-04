#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import sys
import pygame
import os
import math
import time
import random
import bisect

pygame.init()
pygame.display.list_modes()
myfont = pygame.font.SysFont("monospace", 13)
myfont2 = pygame.font.SysFont("monospace", 13)

screen = pygame.display.set_mode((1200, 600))
arrow_angle = math.radians(90)
clock = pygame.time.Clock()
done = False

# Define global variables
size = width, height = 1200, 600
running = 1
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0
gameplay = 0
hits = 0

p_color = (255, 0, 0)
p_xcord = 30
arrow_x = 30
arrow_y = 100
arrow_r = 20

# Holds ball info
ball_r = 3
ball_c = white
ball_t = 0
ball_x = 25
ball_y = height/2
vel_x = 30
vel_y = 0

flag_topx = width-33
flag_topy = height/2-4
flag_w = 16
flag_h = 8
score = []
score_x = 200

# Power bar
def progress(direction, p_xcord):
	if direction > 1 and p_xcord < 100:
		p_xcord = p_xcord+8
	elif direction < 1 and p_xcord > 0:
		p_xcord = p_xcord-8
	pygame.draw.rect(screen, p_color, pygame.Rect(30, 550, 30+p_xcord, 30))
	return p_xcord

def rotatearrow(direction):
	# Update arrow direction, depending on user's key press
	global arrow_x,arrow_y,arrow_angle
	if direction > 0:
		arrow_angle = arrow_angle + math.radians(-10)
	elif direction < 0:
		arrow_angle = arrow_angle + math.radians(10)
	x = arrow_x + arrow_r*math.cos(arrow_angle)
	y = arrow_y - arrow_r*math.sin(arrow_angle)
	pygame.draw.aaline(screen, (250, 250, 15),(arrow_x,arrow_y), (x,y))

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

def update_lines():
	
	# Calculates new line position for green and background lines
	global line, line2, line3, line4
	line = midpt_disp([0+50, height/2], [width-50, height/2], 1.8, 50, 12)
	line2 = midpt_disp([0, height/2], [width, height/2], 1.0, 325, 12)
	line3 = midpt_disp([0, height/2], [width, height/2], 1.0, 150, 12)
	line4 = midpt_disp([0, height/2], [width, height/2], 0.8, 225, 12)

def line_data():
	# Creates data list that holds the y position of the green
	global line
	data = []
	data.append(height/2)
	for i in range(50):
		data.append(height/2)
	x = 0
	for i in range(width-100):
		while (i+50) != int(line[x][0]):
			x = x + 1
		data.append(int(line[x][1]))
	for i in range(50):
		data.append(height/2)
	return data


# Ball movement
def moveball(color, new_x, new_y):
	time.sleep(.005)
	pygame.display.update(pygame.draw.circle(screen, color, (int(new_x), int(new_y)), ball_r, ball_t))

def hitball(angle, velocity):
	
	# Calculate physics of ball movement
	vel_y = velocity * math.sin(angle)
#	print (vel_y)
	vel_x = velocity * math.cos(angle)
	t = (vel_y / 9.8)* 2
	global ball_x, ball_y, data
	pos_x = ball_x
	pos_y = ball_y
	dt = t / 100
	dt_total = dt
	vel_y = vel_y * -1
	# Ball is moving fast enough to move
	while math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)) > 1:

		# Run until the ball hits the ground
		while pos_y <= data[int(pos_x)]:
			vel_y = vel_y + (4.9)*dt
			moveball(black, pos_x, pos_y)
			pos_x = pos_x + vel_x*dt
			pos_y = pos_y + vel_y*dt

			# Hit a wall
			if pos_x > width:
				vel_x = -vel_x
				pos_x = width - 1

			if pos_x < 1:
				vel_x = -vel_x
				pos_x = 1	

			dt_total += dt
			if pos_y > data[int(pos_x)]:
				break
			
			# Draw ball in new position
			moveball(ball_c, pos_x, pos_y)	

			#ball hits flag
			if pos_x > flag_topx and pos_x < flag_topx + flag_w:
				if pos_y > flag_topy and pos_y < flag_topy + flag_h:
					return 1;
					break

		# Bouncing
		dt_total = dt_total - 2*dt
		if pos_x >= 1 and pos_x <= width:
			pos_x = pos_x - (vel_x*dt)
		pos_y = data[int(pos_x)] #data is ground data

		# Calculate the bounce angle
		inco_x = pos_x - (vel_x*dt)
		inco_y = pos_y - (vel_y*dt)
		gd_x = pos_x - 2
		gd_y = data[int(gd_x)]
		a = math.sqrt(math.pow(inco_x - pos_x, 2) + math.pow(inco_y - pos_y, 2))
		b = math.sqrt(math.pow(gd_x - pos_x, 2) + math.pow(gd_y - pos_y, 2))
		c = math.sqrt(math.pow(inco_x - gd_x, 2) + math.pow(inco_y - gd_y, 2))
		theta = math.acos((a*a + b*b - c*c)/(2*a*b))
#		angle = -1*theta + math.pi

		phi = math.acos(math.fabs(gd_x - pos_x)/b)
#		angle = theta + phi
		if (inco_x <= pos_x):
			angle = theta + phi
		elif (inco_x > pos_x):
			angle = theta - phi
		
		velocity = velocity * 0.6
		vel_y = velocity * math.sin(angle)
		vel_x = velocity * math.cos(angle)
		t = (vel_y / 9.8) * 2

		dt_total = dt
		vel_y = vel_y * -1
		ball_x = pos_x
		ball_y = pos_y

	# update ball's x and y to final position
	ball_x = pos_x
	ball_y = data[int(pos_x)]

	# ball has not made it into the hole
	return 0;

def draw_fill(line, color):
	i = 1
	while i < (len(line)):
		pygame.draw.aaline(screen, color, (line[i-1][0],line[i-1][1]), (line[i-1][0],height))
		i = i + 1

def draw_background(line2, line3, lin4):
	draw_fill(line2,(76,3,3))
	draw_fill(line4,(3,3,76))
	draw_fill(line3,(3,76,3))

def draw_green(line):
	draw_fill(line, green)
	for val in range(50):
		pygame.draw.aaline(screen, green, (val, height/2), (val, height))
		pygame.draw.aaline(screen, green, (width-val-1, height/2), (width-val-1, height))



def restart():
	p = sys.executable
	os.execl(p, p, *sys.argv)

# Main loop
it = 0
playing = True

# Set up initial line variables
line = midpt_disp([0+50, height/2], [width-50, height/2], 1.8, 50, 12)
line2 = midpt_disp([0, height/2], [width, height/2], 1.0, 325, 12)
line3 = midpt_disp([0, height/2], [width, height/2], 1.0, 150, 12)
line4 = midpt_disp([0, height/2], [width, height/2], 0.8, 225, 12)
data = line_data()

for holenumber in range(1):
	while(playing == True):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				playing = false
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					p_xcord = progress(2, p_xcord)
				if event.key == pygame.K_DOWN:
					p_xcord = progress(0, p_xcord)
				if event.key == pygame.K_SPACE:
					gameplay = hitball(arrow_angle, p_xcord) 
					hits += 1
				if event.key == pygame.K_RIGHT:
					rotatearrow(1)
				if event.key == pygame.K_LEFT:
					rotatearrow(-1)

		# Draw hole elements
		screen.fill((27,128,186))
		draw_background(line2, line3, line4)
		draw_green(line)

		# Flag
		pygame.draw.ellipse(screen, (50,50,50), [flag_topx, flag_topy, flag_w, flag_h])
		pygame.draw.line(screen, white, (width-25, height/2), (width-25, height/2-20))
		pygame.draw.polygon(screen, red, [[width-25, height/2-20],[width-25, height/2-15],[width-35, height/2-18+(it%3)]])
		
		moveball(ball_c, ball_x, ball_y)
	
		# Update and draw arrow
		arrow_x = ball_x 
		arrow_y = ball_y
		x = arrow_x + arrow_r*math.cos(arrow_angle)
		y = arrow_y - arrow_r*math.sin(arrow_angle)
		pygame.draw.aaline(screen, (250,250,15),(arrow_x,arrow_y), (x,y))
		
		#Create string with current scores
		output = str("")
		tota = 0
		for g in range(holenumber):
			output += "{:>2} ".format(str(score[g]))
			output += " "
			tota += score[g]
		if hits > 99:
			output += str(99)
			tota += 99
		else:
			output += str(hits)
			tota += hits
		if tota > 999:
			tota = 999

		#Draw scoreboard
		pygame.draw.rect(screen, white, pygame.Rect(0, height-65, 550, 65));
		label = myfont.render("1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | T",1, black)
		scor = myfont2.render(output, 1, black)
		tot = myfont2.render("| " + str(tota), 1, black)
		screen.blit(label, (score_x,height-50))
		screen.blit(scor, (score_x-5,height-30))
		screen.blit(tot, (score_x+272, height-30))
		
		#Draw power bar
		pygame.draw.rect(screen, black, pygame.Rect(28,548,136,34))
		pygame.draw.rect(screen, blue, pygame.Rect(30,550,132,30))
		pygame.draw.rect(screen, p_color, pygame.Rect(30,550,30+p_xcord,30))
		
		it = it + 1
		pygame.display.flip()
		
		# Ball in hole
		if gameplay != 0:
			if hits <= 99:
				score.append(hits)
			else:
				score.append(99)
			playing = False

	# Update proper variables for next hole
	screen.fill((27,128,186))
	update_lines()
	data = line_data()
	playing = True
	gameplay = 0
	hits = 0
	ball_x = 25
	ball_y = height/2

## Game is over ##
pygame.display.update(screen.fill((27,128,186)))
myendfont = pygame.font.SysFont("monospace", 26)
myendfont2 = pygame.font.SysFont("monospace", 18)

# Update green and background
update_lines()
data = line_data()
draw_background(line2, line3, line4)
draw_green(line)

pygame.display.flip()
while (1):
	screen.fill((27,128,186))
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit(0)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					restart()
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit(0)
	# Set up end game page text
	end = myendfont.render("~GAME OVER~", 1, white)
	end2 = myendfont.render("FINAL SCORE: " + str(tota), 1, white)
	mess = myendfont2.render("Press q to quit, r to restart!", 1, white)

	# Ball randomly moves on final screen
	draw_background(line2, line3, line4)
	draw_green(line)
	gameplay = hitball(math.radians(random.randint(0,180)), random.randint(30,100))

	# Display end game text
	screen.blit(mess, (100, height - 100))
	screen.blit(end, (width/2-100, height/4))
	screen.blit(end2, (width/2-120, height/4 + 50))

	pygame.display.flip()


