import pygame
import neat
paddel_width = 15
paddel_height = 125
paddel_speed = 3
win = pygame.display.set_mode((400, 400))
starting_left_position = (0 + 10, win.get_height() / 2 - paddel_height / 2)
starting_right_position = (win.get_width() - 10 - paddel_width, win.get_height() / 2 - paddel_height / 2)
ball_radius = 8
ball_bounce_variation = 2
pop_size = 2
if not pop_size % 2 == 0:
	pop_size += 1


class Ball:
	def __init__(self):
		self.x = win.get_width() / 2 - ball_radius
		self.y = win.get_height() / 2 - ball_radius
		self.x_dir = 1
		self.y_dir = 0

	def show(self):
		pygame.draw.circle(win, (255, 255, 255), (self.x + self.x_dir, self.y + self.y_dir), ball_radius)	

	def move(self):
		self.y += self.y_dir
		self.x += self.x_dir

	def collide(self, paddel):
		collision = paddel.rect.collidepoint((self.x, self.y))
		if collision:
			self.x_dir = -self.x_dir
			self.y_dir = -self.y_dir + paddel.y_dir

		if  self.y < 0 or self.y > win.get_height():
			if self.y < 0:
				self.y = 0
			elif self.y > win.get_height():
				self.y = win.get_height()
			self.y_dir = -self.y_dir



class Paddel:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.y_dir = 0
		self.rect = pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, paddel_width, paddel_height))

	def show(self, win=win):
		self.rect = pygame.draw.rect(win, (255, 255, 255), pygame.Rect(self.x, self.y, paddel_width, paddel_height))

	def move(self, new_y_dir):
		if not new_y_dir == 0:
			self.y_dir = new_y_dir
		if self.y - (self.y_dir * paddel_speed) + paddel_height > win.get_height():
			self.y = win.get_height() - paddel_height
		elif self.y - (self.y_dir * paddel_speed) < 0:
			self.y = 0
		self.y -= self.y_dir * paddel_speed
		





class Game:
	def __init__(self):
		self.win = pygame.display.set_mode((400, 400))
		self.ball = Ball()
		self.paddel1 = Paddel(starting_left_position[0], starting_left_position[1])
		self.paddel2 = Paddel(starting_right_position[0], starting_right_position[1])
		self.paddels = [self.paddel1, self.paddel2]

	def game_loop(self):
		for paddel in self.paddels:
			ball.collide(paddel)
			paddel.show()

		self.ball.move()
		self.ball.show()


game = Game()
while True:
	game.game_loop


def run(conifig_file):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
	# Create the population, which is the top-level object for a NEAT run.
	p = neat.Population(config)
	# Add a stdout reporter to show progress in the terminal.
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.Checkpointer(5))
	# Run for up to 300 generations.
	winner = p.run(Game, 10)


def played_game():
	paddels = [Paddel(starting_left_position[0], starting_left_position[1]) if i % 2 == 0 else Paddel(starting_right_position[0], starting_right_position[1]) for i in range(int(pop_size))]
	balls = [Ball() for _ in range(int(pop_size / 2))]
	clock = pygame.time.Clock()
	run = True
	win.fill(51)
	for paddel in paddels:
		for ball in balls:
			ball.collide(paddel)
		paddel.show()
	for ball in balls:
		ball.move()
		ball.show()
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	mouse_pos = pygame.mouse.get_pos()[1]
	if round(paddels[0].y + paddel_height / 2) > mouse_pos:
		paddels[0].move(1)
	if round(paddels[0].y + paddel_height / 2) < mouse_pos:
		paddels[0].move(-1)
	clock.tick(100)
