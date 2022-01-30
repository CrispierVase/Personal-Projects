import pyglet
import neat
import random
ball_speed_increment = 0.5
paddel_width = 15
paddel_height = 126
paddel_speed = 10
width = 400
height = 400
starting_left_position = (10, height / 2 - paddel_height / 2)
starting_right_position = (width - 10 - paddel_width, height / 2 - paddel_height / 2)
ball_radius = 8
fps = 30
ball_bounce_variation = 2
pop_size = 2
if not pop_size % 2 == 0:
	pop_size += 1


class Ball:
	def __init__(self, win):
		self.x = width / 2 - ball_radius
		self.y = height /2 - ball_radius
		self.x_dir = -5
		self.y_dir = 0
		self.win = win

	def show(self):
		self.circle = pyglet.shapes.Circle(x=self.x, y=self.y, radius=ball_radius, color=(255, 255, 255))
		self.circle.draw()

	def move(self):
		self.y += self.y_dir
		self.x += self.x_dir

	def collide(self, paddel, idx):
		if idx == 0:
			if self.x < paddel.x + paddel_width and self.y < paddel.y and self.y > paddel.y - paddel_height:
				paddel.score += 1
				self.x_dir = -self.x_dir
				self.y_dir = -self.y_dir
				if self.x_dir < 0:
					self.x_dir -= ball_speed_increment
				else:
					self.x_dir += ball_speed_increment
				if self.y_dir > 0:
					self.y_dir += ball_speed_increment
				else:
					self.y_dir -= ball_speed_increment

		else:
			if self.x > paddel.x and self.y < paddel.y and self.y > paddel.y - paddel_height:
				paddel.score += 1f
				self.x_dir = -self.x_dir + random.randrange(-ball_bounce_variation, ball_bounce_variation)
				self.y_dir = -self.y_dir + random.randrange(-ball_bounce_variation, ball_bounce_variation)
				if self.x_dir < 0:
					self.x_dir -= ball_speed_increment
				else:
					self.x_dir += ball_speed_increment
				if self.y_dir > 0:
					self.y_dir += ball_speed_increment
				else:
					self.y_dir -= ball_speed_increment

		if self.y < 0:
			self.y = 0
			self.y_dir = -self.y_dir
		elif self.y > height:
			self.y = height
			self.y_dir = - self.y_dir

	def lose(self, paddels):
		if self.x < 0:
			paddels[0].score += 1
			return True
		elif self.x > width:
			paddels[1].score += 1
			return True
		return False



class Paddel:
	def __init__(self, x, y, win):
		self.x = x
		self.y = y
		self.y_dir = 0
		self.score = 0
		self.win = win
		self.rect = pyglet.shapes.Rectangle(x=self.x, y=self.y, width=paddel_width, height=paddel_height, color=(255, 255, 255))

	def show(self):
		self.rect = pyglet.shapes.Rectangle(x=self.x, y=self.y, width=paddel_width, height=paddel_height, color=(255, 255, 255))
		self.rect.anchor_x = 0
		self.rect.anchor_y = paddel_height 
		self.rect.draw()

	def move(self, new_y_dir):
		# if not new_y_dir == 0:
		self.y_dir = new_y_dir
		if self.y > height:
			self.y = height
		elif self.y - paddel_height < 0:
			self.y = paddel_height
		self.y -= self.y_dir * paddel_speed





class Game:
	def __init__(self):
		self.win = pyglet.window.Window(width, height)
		self.clock = pyglet.clock.get_default()
		self.ball = Ball(self.win)
		self.paddel1 = Paddel(starting_left_position[0], starting_left_position[1], self.win)
		self.paddel2 = Paddel(starting_right_position[0], starting_right_position[1], self.win)
		self.paddels = [self.paddel1, self.paddel2]
		self.good_y = height / 2

	def game_loop(self):
		@self.win.event
		def on_mouse_motion(x, y, dx, dy):
			self.good_y = y + paddel_height // 2


		def on_draw(*args, **kwargs):
			self.win.clear()
			for idx, paddel in enumerate(self.paddels):
				if paddel.y < self.good_y:
					paddel.move(-1)
				elif paddel.y > self.good_y:
					paddel.move(1)
				# else:
					# paddel.move(0)
				paddel.show()
				if self.ball.lose(self.paddels):
				 	quit('You Lost lol')
				self.ball.collide(paddel, idx)
			self.ball.move()
			self.ball.show()
		self.clock.tick(fps)
		self.clock.schedule(on_draw, 1/fps)
		self.win.flip()
		pyglet.app.run()



games = [Game() for _ in range(int(pop_size / 2))]
for game in games:
 	game.game_loop()


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
