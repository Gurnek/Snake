import pygame as pg
import random, math
pg.init()

class SceneBase:
	def __init__(self):
		self.next = self

	def ProcessInput(self, events):
		print('This has not been overridden')

	def Update(self):
		print('This has not been overridden')

	def Render(self, screen):
		print('This has not been overridden')

	def SwitchToScene(self, next_scene):
		self.next = next_scene

	def Terminate(self):
		self.SwitchToScene(None)

def drawNiceRect(screen, color, x, y, width, height, thickness):
		pg.draw.rect(screen, color, pg.Rect(x, y, thickness, height))
		pg.draw.rect(screen, color, pg.Rect(x, y, width, thickness))
		pg.draw.rect(screen, color, pg.Rect(x + width - thickness, y, thickness, height))
		pg.draw.rect(screen, color, pg.Rect(x, y + height - thickness, width, thickness))

class Drop():
	def __init__(self, r = False):
		self.z = (random.randrange(0, 8000)) ** (1/3)
		self.y = random.randrange(-500, -50)
		self.x = random.randrange(0, 800)
		self.yspeed = (-9 / 20) * self.z + 10
		self.length = (-3 / 4) * self.z + 20
		self.width = (-1 / 5) * self.z + 5
		self.r = r

	def check(self):
		if self.y > 600:
			self.y = random.randrange(-500, -50)

	def draw(self, screen):
		if self.r:
			color = (0, 0, 0)
		else:
			color = (255, 0, 0)

		pg.draw.rect(screen, color, pg.Rect(self.x, self.y, self.width, self.length))

	def update(self):
		self.y += self.yspeed

class TitleScene(SceneBase):
	def __init__(self):
		SceneBase.__init__(self)
		self.d = [Drop() for x in range(500)]
		self.position = (0, 0)
		self.highlight_1 = False
		self.highlight_2 = False
		self.background = (0, 0, 0)
		self.title = 'Super Intense Snake X'
		self.textColor = (255, 0, 0)
		self.fps = 120

		pg.mixer.music.load('songs/firepower.mp3')
		pg.mixer.music.play(-1)

	def ProcessInput(self, events, pressed):
		for event in events:
			if event.type == pg.QUIT:
				self.Terminate()
			if event.type == pg.MOUSEMOTION:
				self.position = event.pos
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_r:
					self.SwitchToScene(RatedRTitle())

			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1 and self.position[0] > 200 and self.position[0] < 600 and self.position[1] < 350 and self.position[1] > 250:
					pg.mixer.music.stop()
					self.SwitchToScene(NormalSnake())

				if event.button == 1 and self.position[0] > 200 and self.position[0] < 600 and self.position[1] < 500 and self.position[1] > 400:
					self.Terminate()

	def Update(self):
		if self.position[0] > 200 and self.position[0] < 600 and self.position[1] < 350 and self.position[1] > 250:
			self.highlight_1 = True
		if self.position[0] > 200 and self.position[0] < 600 and self.position[1] < 500 and self.position[1] > 400:
			self.highlight_2 = True

		if self.position[0] < 200 or self.position[0] > 600:
			self.highlight_1 = False
			self.highlight_2 = False
		if self.position[1] < 250 or self.position[1] > 350:
			self.highlight_1 = False
		if self.position[1] < 400 or self.position[1] > 500:
			self.highlight_2 = False

		for drop in self.d:
			drop.update()
			drop.check()

	def Render(self, screen):
		font = pg.font.Font('fonts/moonhouse.ttf', 56)
		title = font.render(self.title, True, self.textColor)
		play = font.render('Play Snake', True, self.textColor)
		quit = font.render('Quit', True, self.textColor)

		screen.fill(self.background)
		for drop in self.d:
			drop.draw(screen)
		if self.highlight_1:
			pg.draw.rect(screen, (255, 255, 255), pg.Rect(200, 250, 400, 100))
		if self.highlight_2:
			pg.draw.rect(screen, (255, 255, 255), pg.Rect(200, 400, 400, 100))

		drawNiceRect(screen, (255, 255, 255), 200, 250, 400, 100, 7)
		drawNiceRect(screen, (255, 255, 255), 200, 400, 400, 100, 7)

		screen.blit(title, (400 - title.get_width() // 2, 150 - title.get_height() // 2))
		screen.blit(play, (400 - play.get_width() // 2, 300 - play.get_height() // 2))
		screen.blit(quit, (400 - quit.get_width() // 2, 450 - quit.get_height() // 2))

class RatedRTitle(TitleScene):
	def __init__(self):
		TitleScene.__init__(self)
		self.background = (255, 0, 0)
		self.title = 'X Rated Snake'
		self.d = [Drop(True) for x in range(500)]
		self.textColor = (255, 255, 255)

	def ProcessInput(self, events, pressed):
		TitleScene.ProcessInput(self, events, pressed)
		for event in events:
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_r:
					self.SwitchToScene(TitleScene())

			if event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1 and self.position[0] > 200 and self.position[0] < 600 and self.position[1] < 350 and self.position[1] > 250:
					self.SwitchToScene(RRatedSnake())

	def Update(self):
		TitleScene.Update(self)

	def Render(self, screen):
		TitleScene.Render(self, screen)

class ScoreScene(SceneBase):
	def __init__(self, score, r = False):
		SceneBase.__init__(self)
		self.score = score
		self.r = r
		self.fps = 120
		self.highlight_1 = False
		self.highlight_2 = False
		self.position = (0, 0)
	def ProcessInput(self, events, pressed):
		for event in events:
			if event.type == pg.QUIT:
				self.Terminate()

			if event.type == pg.MOUSEMOTION:
				self.position = event.pos

			if event.type == pg.MOUSEBUTTONDOWN:
				if self.highlight_1:
					self.SwitchToScene(TitleScene())
				if self.highlight_2:
					self.Terminate()

	def Update(self):
		if self.position[0] > 200 and self.position[0] < 600:
			if self.position[1] > 300 and self.position[1] < 400:
				self.highlight_1 = True
			if self.position[1] > 420 and self.position[1] < 520:
				self.highlight_2 = True

		if self.position[0] < 200 or self.position[0] > 600:
			self.highlight_1 = False
			self.highlight_2 = False
		if self.position[1] < 300 or self.position[1] > 400:
			self.highlight_1 = False
		if self.position[1] < 420 or self.position[1] > 520:
			self.highlight_2 = False

	def Render(self, screen):
		screen.fill((0, 0, 0))
		font = pg.font.Font('fonts/moonhouse.ttf', 56)
		death = font.render('YOU DIED!', True, (255, 0, 0))
		score = font.render('Your score is %s' % (self.score), True, (255, 0, 0))
		retry = font.render('Retry', True, (255, 0, 0))
		quit = font.render('Quit', True, (255, 0, 0))

		if self.highlight_1:
			pg.draw.rect(screen, (255, 255, 255), pg.Rect(200, 300, 400, 100))
		elif self.highlight_2:
			pg.draw.rect(screen, (255, 255, 255), pg.Rect(200, 420, 400, 100))

		screen.blit(death, (400 - death.get_width() // 2, 50 - death.get_height() // 2))
		screen.blit(score, (400 - score.get_width() // 2, 120 - score.get_height() // 2))
		screen.blit(retry, (400 - retry.get_width() //2, 350 - retry.get_height() // 2))
		screen.blit(quit, (400 - quit.get_width() // 2, 470 - quit.get_height() // 2))

		drawNiceRect(screen, (255, 255, 255), 200, 300, 400, 100, 10)
		drawNiceRect(screen, (255, 255, 255), 200, 420, 400, 100, 10)

class Snake:
	def __init__(self):
		self.x = 10
		self.y = 10
		self.speed = [1, 0]
		self.length = 1
		self.tail = []

	def dir(self, speed):
		self.speed = speed

class NormalSnake(SceneBase):
	def __init__(self):
		SceneBase.__init__(self)
		self.song_end = pg.USEREVENT + 1
		pg.mixer.music.set_endevent(self.song_end)
		self.s = Snake()
		self.scl = 10
		self.food_present = False
		self.foodx = None
		self.foody = None
		self.fps = 20

		self.songs = ['astronaut 13', 'catharsis', 'colorblind', 'firepower', 'karma', 'nirmiti', 'robot language',
				 'supernova', 'the one who flies', 'universal expression', 'hidden dangers']
		self.already_played_songs = []

		self.pick_new_song()

	def pick_new_song(self):
		if len(self.songs) == self.already_played_songs:
			self.already_played_songs = []
		next_song = random.choice(self.songs)
		while next_song in self.already_played_songs:
			next_song = random.choice(self.songs)
		self.already_played_songs.append(next_song)
		pg.mixer.music.load('songs/' + next_song + '.mp3')
		pg.mixer.music.play()

	def food(self):
		if not self.food_present:
			self.foodx = self.scl * random.randrange(80)
			self.foody = self.scl * random.randrange(60)

			for coord in self.s.tail:
				while self.foodx == coord[0] and self.foody == coord[1]:
					self.foodx = self.scl * random.randrange(80)
					self.foody = self.scl * random.randrange(60)
			self.food_present = True

	def didIEatMyself(self):
		for coord in self.s.tail[1:]:
			if self.s.x == coord[0] and self.s.y == coord[1]:
				self.SwitchToScene(ScoreScene(self.s.length))

	def eat(self):
		if self.s.x == self.foodx and self.s.y == self.foody:
			self.food_present = False
			self.s.length += 1

	def ProcessInput(self, events, pressed):
		self.pressed = pressed
		for event in events:
			if event.type == pg.QUIT:
				self.Terminate()
			if event.type == self.song_end:
				self.pick_new_song()

		if pressed[pg.K_UP] : self.s.dir([0, -1])
		if pressed[pg.K_DOWN] : self.s.dir([0, 1])
		if pressed[pg.K_LEFT] : self.s.dir([-1, 0])
		if pressed[pg.K_RIGHT] : self.s.dir([1, 0])
		if pressed[pg.K_n] : self.pick_new_song()

	def Update(self):
		if self.s.x == 790 and self.s.speed[0] == 1:
			self.s.speed[0] = 0
		if self.s.x == 0 and self.s.speed[0] == -1:
			self.s.speed[0] = 0
		if self.s.y == 0 and self.s.speed[1] == -1:
			self.s.speed[1] = 0
		if self.s.y == 590 and self.s.speed[1] == 1:
			self.s.speed[1] = 0
		if len(self.s.tail) == self.s.length:
			self.s.tail.insert(0, (self.s.x + self.s.speed[0] * self.scl, self.s.y + self.s.speed[1] * self.scl))
			del self.s.tail[-1]
		if len(self.s.tail) < self.s.length:
			self.s.tail.insert(0, (self.s.x + self.s.speed[0] * self.scl, self.s.y + self.s.speed[1] * self.scl))
		self.s.x += self.s.speed[0] * self.scl
		self.s.y += self.s.speed[1] * self.scl

		self.didIEatMyself()
		self.eat()

	def Render(self, screen):
		screen.fill((0, 0, 0))

		for coord in self.s.tail:
			r = math.floor(((255 * coord[0])/800))
			g = math.floor((255 * coord[1])/600)
			b = 255 - math.floor(((255 * math.sqrt(r ** 2 + g ** 2))/1000))
			color = (r, g, b)

			pg.draw.rect(screen, color, pg.Rect(coord[0], coord[1], self.scl, self.scl))

		self.food()
		if self.food_present:
			pg.draw.rect(screen, (255, 0, 0), pg.Rect(self.foodx, self.foody, self.scl, self.scl))

class RRatedSnake(NormalSnake):
	def __init__(self):
		NormalSnake.__init__(self)
		self.s.x = 20
		self.s.y = 20
		self.fps = 10
		self.scl = 20
		self.createSurfaces()

	def createSurfaces(self):
		image = pg.image.load('pics/sprite.png')

		self.head = pg.Surface((20, 20))
		self.head.set_colorkey((0, 0, 0))
		self.head.blit(image, (0, 0), (0, 0, 20, 20))

		self.shaft = pg.Surface((20, 20))
		self.shaft.set_colorkey((0, 0, 0))
		self.shaft.blit(image, (0, 0), (21, 0, 20, 20))

		self.halfshaft = pg.Surface((20, 10))
		self.halfshaft.set_colorkey((0, 0, 0))
		self.halfshaft.blit(image, (0, 0), (21, 0, 20, 10))

		self.ball = pg.Surface((20, 20))
		self.ball.set_colorkey((0, 0, 0))
		self.ball.blit(image, (0, 0), (0, 21, 20, 20))

		self.pill = pg.Surface((20, 20))
		self.pill.set_colorkey((0, 0, 0))
		self.pill.blit(image, (0, 0), (21, 21, 20, 20))

	def food(self):
		if not self.food_present:
			self.foodx = self.scl * random.randrange(40)
			self.foody = self.scl * random.randrange(30)

			for coord in self.s.tail:
				while self.foodx == coord[0] and self.foody == coord[1]:
					self.foodx = self.scl * random.randrange(40)
					self.foody = self.scl * random.randrange(30)
			self.food_present = True

	def ProcessInput(self, events, pressed):
		for event in events:
			if event.type == pg.QUIT:
				self.Terminate()
		if pressed[pg.K_UP] : self.s.dir([0, -1])
		elif pressed[pg.K_DOWN] : self.s.dir([0, 1])
		elif pressed[pg.K_LEFT] : self.s.dir([-1, 0])
		elif pressed[pg.K_RIGHT] : self.s.dir([1, 0])

	def Update(self):
		if self.s.x == 780 and self.s.speed[0] == 1:
			self.s.speed[0] = 0
		if self.s.x == 0 and self.s.speed[0] == -1:
			self.s.speed[0] = 0
		if self.s.y == 580 and self.s.speed[1] == 1:
			self.s.speed[1] = 0
		if self.s.y == 0 and self.s.speed[1] == -1:
			self.s.speed[1] = 0

		if len(self.s.tail) == self.s.length:
			self.s.tail.insert(0, (self.s.x + self.s.speed[0] * self.scl, self.s.y + self.s.speed[1] * self.scl, self.s.speed[0], self.s.speed[1]))
			del self.s.tail[-1]
		if len(self.s.tail) < self.s.length:
			self.s.tail.insert(0, (self.s.x + self.s.speed[0] * self.scl, self.s.y + self.s.speed[1] * self.scl, self.s.speed[0], self.s.speed[1]))

		self.s.x += self.s.speed[0] * self.scl
		self.s.y += self.s.speed[1] * self.scl

		self.didIEatMyself()
		self.eat()

	def Render(self, screen):
		screen.fill((255, 0, 0))

		for piece in self.s.tail:
			if piece == self.s.tail[0]:
				if piece[2] == 1:
					currenthead = pg.transform.rotate(self.head, -90)
				elif piece[2] == -1:
					currenthead = pg.transform.rotate(self.head, 90)
				elif piece[3] == 1:
					currenthead = pg.transform.rotate(self.head, 180)
				else:
					currenthead = self.head

				screen.blit(currenthead, (piece[0], piece[1]))

			elif piece == self.s.tail[-1]:
				if piece[2] != 0:
					screen.blit(self.ball, (piece[0], piece[1] + 10))
					screen.blit(self.ball, (piece[0], piece[1] - 10))
					if piece[2] > 0:
						screen.blit(pg.transform.rotate(self.halfshaft, -90), (piece[0], piece[1]))
					else:
						screen.blit(pg.transform.rotate(self.halfshaft, 90), (piece[0], piece[1]))

				else:
					screen.blit(self.ball, (piece[0] + 10, piece[1]))
					screen.blit(self.ball, (piece[0] - 10, piece[1]))
					if piece[3] > 0:
						screen.blit(pg.transform.rotate(self.halfshaft, 180), (piece[0], piece[1]))
					else:
						screen.blit(self.halfshaft, (piece[0], piece[1]))

			else:
				if piece[2] == 1:
					currentshaft = pg.transform.rotate(self.shaft, -90)
				elif piece[2] == -1:
					currentshaft = pg.transform.rotate(self.shaft, 90)
				elif piece[3] == 1:
					currentshaft = pg.transform.rotate(self.shaft, 180)
				else:
					currentshaft = self.shaft

				screen.blit(currentshaft, (piece[0], piece[1]))

		self.food()
		if self.food_present:
			screen.blit(self.pill, (self.foodx, self.foody))


def runGame(width, height, fps, starting_scene):

	screen = pg.display.set_mode((width, height))
	pg.display.set_caption('Super Intense Snake X')

	clock = pg.time.Clock()

	active_scene = starting_scene

	while active_scene != None:
		pressed = pg.key.get_pressed()

		filtered_events = []
		for event in pg.event.get():
			quit = False
			if event.type == pg.QUIT:
				quit = True
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					quit = True
			if quit:
				active_scene.Terminate()
			else:
				filtered_events.append(event)

		active_scene.ProcessInput(filtered_events, pressed)
		active_scene.Update()
		active_scene.Render(screen)

		active_scene = active_scene.next

		pg.display.flip()

		if active_scene != None:
			clock.tick(active_scene.fps)

runGame(800, 600, 15, TitleScene())
