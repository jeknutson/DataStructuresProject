#!/afs/nd.edu/user14/csesoft/cse20312/bin/python3.6

import sys, pygame, os, math, time, random, bisect

pygame.init()
pygame.display.list_modes()
screen = pygame.display.set_mode((1200, 600))
arrow_angle = math.radians(90)
clock = pygame.time.Clock()
done = False

size = width, height = 1200, 600
running = 1
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
blue = 0, 0, 255
green = 0, 255, 0

p_color = (255, 0, 0)
p_xcord = 30
arrow_x = 30
arrow_y = 100
arrow_r = 20

ball_r = 3
ball_c = white
ball_t = 0
ball_x = 25
ball_y = height/2
vel_x = 30
vel_y = 0

# Power bar
def progress(direction, p_xcord):
	if direction > 1 and p_xcord < 100:
		p_xcord = p_xcord+8
	elif direction < 1 and p_xcord > 0:
		p_xcord = p_xcord-8
	pygame.draw.rect(screen, p_color, pygame.Rect(30, 550, 30+p_xcord, 30))
	return p_xcord

def rotatearrow(direction):
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

line = midpt_disp([0+50, height/2], [width-50, height/2], 1.8, 200, 12)
#line2 = midpt_disp([0+50, height/2], [width-50, height/2], 2.0, 250, 12)
#for i in range(len(line)):
#	print((line[i-1][0],line[i-1][1]),(line[i][0], line[i][1]))	

def line_data():
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


#Ball movement
def moveball(color, new_x, new_y):
	time.sleep(.1)
	pygame.display.update(pygame.draw.circle(screen, color, (int(new_x), int(new_y)), ball_r, ball_t))

def hitball(angle, velocity):
	vel_y = velocity * math.sin(angle)
	print (vel_y)
	vel_x = velocity * math.cos(angle)
	t = (vel_y / 9.8)* 2
	global ball_x, ball_y, data
	pos_x = ball_x
	pos_y = ball_y
	dt = t / 30
	dt_total = dt
	vel_y = vel_y * -1
#	while dt_total < t:
	while vel_y < -7:
		while pos_y <= data[int(pos_x)]:
			#vel_x = velocity * math.cos(angle)
			vel_y = vel_y + (4.9)*dt
			#moveball(black, pos_x, pos_y)
			pos_x = pos_x + vel_x*dt
			#pos_y = ball_y + vel_y*dt_total + 4.9*dt_total*dt_total
			pos_y = pos_y + vel_y*dt

			# Hit a wall
			if pos_x > width:
				vel_x = -vel_x
				pos_x = width - 1
			#if pos_y <= 0:
			#	vel_y = -vel_y
			#	pos_y = 1
			if pos_x < 1:
				vel_x = -vel_x
				pos_x = 1	

			#print(pos_x)

			dt_total += dt
			moveball(ball_c, pos_x, pos_y)	

		pos_y = data[int(pos_x)]
		velocity = velocity * .5
		vel_y = velocity * math.sin(angle)
		t = (vel_y / 9.8) * 2
		dt = t / 30
		dt_total = dt
		vel_y = vel_y * -1
	
#	moveball(black, pos_x, pos_y)
#	pos_x = ball_x + vel_x*t
#	pos_y = ball_y + vel_y*t + 4.9*t*t
#	moveball(ball_c, pos_x, pos_y)
	ball_x = pos_x
	ball_y = data[int(pos_x)]
#	moveball(ball_c, ball_x, ball_y)
	print(ball_x, ball_y)

# Main loop
it = 0
data = line_data()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			running = 0
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				p_xcord = progress(2, p_xcord)
			if event.key == pygame.K_DOWN:
				p_xcord = progress(0, p_xcord)
			if event.key == pygame.K_SPACE:
				hitball(arrow_angle, p_xcord) 
			if event.key == pygame.K_RIGHT:
				rotatearrow(1)
			if event.key == pygame.K_LEFT:
				rotatearrow(-1)

	#screen.fill(black)

	pygame.draw.line(screen, green, (0, height/2), (50, height/2))
	pygame.draw.line(screen, green, (width-50, height/2), (width, height/2))
	pygame.draw.ellipse(screen, (20,70,15), [width-33, height/2-4, 16, 8])
	pygame.draw.line(screen, (200,200,200), (width-25, height/2), (width-25, height/2-20))
	pygame.draw.polygon(screen, red, [[width-25, height/2-20],[width-25, height/2-15],[width-35, height/2-18+(it%3)]])

	i = 1
	while i < (len(line)):
		pygame.draw.aaline(screen, green, (line[i-1][0],line[i-1][1]),(line[i][0], line[i][1]))
#		print((line[i-1][0],line[i-1][1]),(line[i][0],line[i][1]))	
#		pygame.draw.aaline(screen, blue, (line2[i-1][0],line2[i-1][1]),(line2[i][0], line2[i][1]))	
		i = i + 1
		
	moveball(ball_c, ball_x, ball_y)

	arrow_x = ball_x 
	arrow_y = ball_y
	x = arrow_x + arrow_r*math.cos(arrow_angle)
	y = arrow_y - arrow_r*math.sin(arrow_angle)
	pygame.draw.aaline(screen, (250,250,15),(arrow_x,arrow_y), (x,y))
	
	#Draw power bar
	pygame.draw.rect(screen, white, pygame.Rect(30,550,132,30))
	pygame.draw.rect(screen, p_color, pygame.Rect(30,550,30+p_xcord,30))
	
	it = it + 1
	pygame.display.flip()
