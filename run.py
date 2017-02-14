import pygame
import sys
import random
import math

# CONSTANTS

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 728
GAME_COLOR = (255, 255, 255)
PAD_WIDTH = 16
PAD_HEIGHT = 64
PAD_SPEED = 6
BALL_SIZE = 16
BALL_SPEED = 8
FIRST_PLAYER = 0
SECOND_PLAYER = 1

NORTHWEST = 0
NORTHEAST = 1
SOUTHWEST = 2
SOUTHEAST = 3

pygame.init()

monospace = pygame.font.SysFont("monospace", 22)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

def check_collision(a, b):
	h_overlaps = True
	v_overlaps = True
	if (a.x > (b.x + b.w)) or ((a.x + a.w) < b.x):
		h_overlaps = False
	if (a.y > (b.y + b.h)) or ((a.y + a.h) < b.y):
		v_overlaps = False
	return h_overlaps and v_overlaps

class Pad:

	def __init__(self, x, y, player):
		self.x = x
		self.y = y
		self.w = PAD_WIDTH
		self.h = PAD_HEIGHT
		self.up = False
		self.down = False
		self.player = player
		self.surface = pygame.Surface((16, 64))

	def draw(self):
		pygame.draw.rect(screen, GAME_COLOR, pygame.Rect(self.x, self.y, self.w, self.h))

class Ball:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.direction = 180
		self.speed = BALL_SPEED
		self.w = BALL_SIZE
		self.h = BALL_SIZE
	
	def reset(self):
		self.x = (WINDOW_WIDTH / 2) - (BALL_SIZE / 2)
		self.y = (WINDOW_HEIGHT / 2) - (BALL_SIZE / 2)
		self.direction = 180
		self.speed = BALL_SPEED
	
	def bounce(self, diff):
		self.direction = (180 + self.direction) % 360
		self.direction -= diff
		self.speed *= 1.1
	
	def draw(self):
		direction_radians = math.radians(self.direction)
		
		self.x += self.speed * math.cos(direction_radians)
		self.y -= self.speed * math.sin(direction_radians)
		
		if self.x < 0:
			self.reset()
		elif self.x > WINDOW_WIDTH:
			self.reset()
		if self.y <= 0:
			self.direction = (360 - self.direction) % 360
		elif self.y > WINDOW_HEIGHT - self.w:
			self.direction = (360 - self.direction) % 360
			
		pygame.draw.rect(screen, GAME_COLOR, pygame.Rect(self.x, self.y, self.w, self.h))
	
class Score:
	pass

clock = pygame.time.Clock()
FPS = 60
player1 = Pad(PAD_WIDTH, (WINDOW_HEIGHT / 2) - (PAD_HEIGHT / 2), FIRST_PLAYER)
player2 = Pad(WINDOW_WIDTH - (PAD_WIDTH * 2), (WINDOW_HEIGHT / 2) - (PAD_HEIGHT / 2), SECOND_PLAYER)
ball = Ball((WINDOW_WIDTH / 2) - (BALL_SIZE / 2), (WINDOW_HEIGHT / 2) - (BALL_SIZE / 2))

def handle_events():
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			sys.exit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				sys.exit()
			elif e.key == pygame.K_w:
				player1.up = True
				player1.down = False
			elif e.key == pygame.K_s:
				player1.up = False
				player1.down = True
			elif e.key == pygame.K_UP:
				player2.up = True
				player2.down = False
			elif e.key == pygame.K_DOWN:
				player2.up = False
				player2.down = True

def redraw():
	pygame.display.flip()
	screen.fill((0, 0, 0))
	player1.draw()
	player2.draw()
	ball.draw()
	
	# Delimit boundaries for the paddles.
	
	if player1.up and player1.y > 0:
		player1.y -= PAD_SPEED
	elif player1.down and (player1.y + player1.h) < WINDOW_HEIGHT:
		player1.y += PAD_SPEED
	if player2.up and player2.y > 0:
		player2.y -= PAD_SPEED
	elif player2.down and (player2.y + player2.h) < WINDOW_HEIGHT:
		player2.y += PAD_SPEED
		
	# Handles the ball.
	
	if check_collision(player1, ball):
		diff = (player1.y + player1.h / 2) - (ball.y + ball.h / 2)
		ball.bounce(diff)
	elif check_collision(player2, ball):
		diff = (player2.y + player2.h / 2) - (ball.y + ball.h / 2)
		ball.bounce(diff)
	
	# screen.blit(monospace.render("Bla", 1, (255, 255, 0)), (16, 16))

while (running):
	clock.tick(FPS)
	redraw()
	#  screen.blit(monospace.render(str(clock.get_fps()), 1, (255, 255, 0)), (16, 32 + LINE_SPACE))
	handle_events()
