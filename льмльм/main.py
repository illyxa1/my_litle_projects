import pymunk
import pymunk.pygame_util
import pygame
from menu_draw import *
from window import *
from entery import Entery
from random import randint
from basicFig import *
import numpy as np

pygame.init()

class App:
	def __init__(self):
		self.size = (800, 700)
		self.screen = pygame.display.set_mode(self.size)

		self.font = pygame.font.Font('main.ttf', 40)
		self.LFont = pygame.font.Font('main.ttf', 20)

		self.clock = pygame.time.Clock()
		self.FPS = 60

		self.objects = []
		self.start_pos = None

		self.workSpace = pygame.Rect(drawMenu(self.screen, self.size))
		self.startClick = False
		self.instrument = 'None'
		self.pastInstr = self.instrument
		self.num = 0

		self.settings = {
			'Gravity Y': 900,
			'Gravity X': 0,
			'FPS':60
		}

		FileButtons = {
			'New':self.createNew,
			'Save':self.save,
			'Load':self.load
		}

		AddButtons = {
			'Circle':[self.changeInstOn, 'Circle'],
			'Box':[self.changeInstOn, 'Box'],
			'Paddle':[self.changeInstOn, 'Paddle'],
			'Move':[self.changeInstOn, 'Move'],
			'Dublicate':[self.changeInstOn, 'Dublicate'],
			'None':[self.changeInstOn, 'None']
		}

		self.bLists = [
			BList(6, 6, 100, 45, self.font, smooting=True, printing='File', buttons=FileButtons),
			BList(130, 6, 100, 45, self.font, smooting=True, printing='Add', buttons=AddButtons)
		]

		self.buttons = [
			Button(254, 6, 100, 45, self.font, smooting=True, printing='Objects', funk=self.objSets),
			Button(364, 6, 100, 45, self.font, smooting=True, printing='Render', funk=self.simRun)
		]

	def save(self):
		objects = [obj.parametrate() for obj in self.objects]
		save_list = np.array(objects)
		np.save('saves/save_file', save_list, allow_pickle=True)

	def load(self):
		enterys = [
			Entery(75, 50, self.LFont, w=150, colorS=(122, 122, 122), border=2, smooting=True)
		]

		buttons = [
			Button(100, 150, 100, 30, font=self.LFont, printing='Load file', smooting=True, funk=self.loadFile, args=[enterys[0], self.screen])
		]

		window = Window(self.screen, [800], [700], 300, 200, caption='Load file',
			buttons=buttons, enterys=enterys)
		window.run()

	def loadFile(self, args):
		name = args[0].writing
		screen = args[1]
		for block in np.load(name, allow_pickle=True):
			if block['typ'] == 'Circle':
				circle = Circle(screen, block['pos'], block['r'], block['num'])
				circle.mass = block['mass']
				circle.elasticity = block['elasticity']
				circle.friction = block['friction']
				self.objects.append(circle)

			elif block['typ'] == 'Box':
				box = Box(screen, block['x'], block['y'], block['w'], block['h'], block['num'])
				box.mass = block['mass']
				box.elasticity = block['elasticity']
				box.friction = block['friction']
				self.objects.append(box)

			elif block['typ'] == 'Paddle':
				paddle = Paddle(screen, block['pos'], block['pos2'], block['w'], block['num'])
				paddle.elasticity = block['elasticity']
				paddle.friction = block['friction']
				self.objects.append(paddle)

	def objSets(self):
		h = len(self.objects) * 30 + 60

		printings = [
			[self.LFont.render(self.objects[i].typ + ' ' +str(self.objects[i].num), True, (0, 0, 0)), (20, 30 + i * 30)] for i in range(len(self.objects))
		]
		
		buttons = []
		for i in range(len(self.objects)):

			buttons.append(Button(100, 30 + i * 30 - 2, 100, printings[0][0].get_height() + 4, font=self.LFont, printing='Change', 
				funk=self.objects[i].changeSetting, args=([self.size[0]], [self.size[1]])))

			buttons.append(Button(230, 30 + i * 30 - 2, 100, printings[0][0].get_height() + 4, onlyOneClick=True, font=self.LFont, printing='Delete', 
				funk=self.objects.remove, args=self.objects[i]))
		

		window = Window(self.screen, [self.size[0]], [self.size[1]], 350, h, caption='Objects settings', 
			printings=printings, buttons=buttons)
		window.run()

	def changeInstOn(self, instrument):
		self.instrument = instrument
		pass

	def draw(self):
		self.screen.fill((0, 122, 122))
		drawMenu(self.screen, self.size)
		
		# drawing objects
		for obj in self.objects:
			obj.draw()
		self.drawObjects()

		# drawing interface objects
		[bl.draw(self.screen, self.mousePos) for bl in self.bLists]
		[b.draw(self.screen, self.mousePos) for b in self.buttons]

		# taling about instrument
		instrument = self.LFont.render(self.instrument, True, (0, 0, 0))
		self.screen.blit(instrument, (6, 60))

		# end of drawing
		pygame.display.update()

	def run(self):
		while True:
			self.mousePos = pygame.mouse.get_pos()
			self.keys = pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == 256:
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						print(self.objects, len(self.objects))

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 3:
						for obj in self.objects:
							if obj.click(self.mousePos, event.button):
								break

					if event.button == 2:
						for obj in self.objects:
							if obj.click(self.mousePos, event.button):
								self.objects.remove(obj)
								break

					if event.button == 1:
						[bl.click(self.mousePos)for bl in self.bLists]
						[b.click(self.mousePos)for b in self.buttons]

						if self.workSpace.collidepoint(self.mousePos):
							self.startClick = True
							for i in self.bLists:
								if i.active == True:
									self.startClick = False

						if self.startClick:
							print('down')
							if self.instrument == 'Dublicate':
								for obj in self.objects:
									rs = obj.click(self.mousePos, 1, dubl=True, num=self.num)
									if rs:
										self.objects.append(rs)
										self.num += 1
										break

							if self.instrument != 'Move':
								self.startCreating()

							else:
								for obj in self.objects:
									if obj.moving:
										break

									else:
										if obj.startMove(self.mousePos):
											break

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						if self.startClick == True:
							print('up')
							self.startClick = False
							if self.instrument != 'Move':
								self.create()

							else:
								[obj.endMove() for obj in self.objects]

			if self.keys[pygame.K_RSHIFT] or self.keys[pygame.K_LSHIFT]:
				self.instrument = 'Move'

			if self.keys[pygame.K_RCTRL] or self.keys[pygame.K_LCTRL]:
				self.instrument = 'Dublicate'

			if self.keys[pygame.K_c]:
				self.instrument = 'Circle'

			if self.keys[pygame.K_b]:
				self.instrument = 'Box'

			if self.keys[pygame.K_p]:
				self.instrument = 'Paddle'

			self.draw()
			[obj.move(self.mousePos) for obj in self.objects]
			self.clock.tick(self.FPS)

	def startCreating(self):
		self.start_pos = self.mousePos

	def create(self):
		if self.instrument == 'Circle':
			r = int((((self.start_pos[0] - self.mousePos[0])**2 + (self.start_pos[1] - self.mousePos[1])**2))**0.5)
			self.objects.append(Circle(self.screen, self.start_pos, r, self.num))

		if self.instrument == 'Box':
			x = self.mousePos[0] if self.start_pos[0] > self.mousePos[0] else self.start_pos[0]
			y = self.mousePos[1] if self.start_pos[1] > self.mousePos[1] else self.start_pos[1]

			w = abs(self.start_pos[0] - self.mousePos[0])
			h = abs(self.start_pos[1] - self.mousePos[1])

			self.objects.append(Box(self.screen, x, y, w, h, self.num))

		if self.instrument == 'Paddle':
			self.objects.append(Paddle(self.screen, self.start_pos, self.mousePos, 4, self.num))
		self.start_pos = None
		self.num += 1

	def new(self):
		self.objects = []
		self.num = 0
		self.creationWindow.close()

	def createNew(self):
		font = pygame.font.Font('main.ttf', 20)
		fontButt = pygame.font.Font('main.ttf', 15)
		h = font.render('0', True, (0, 0, 0)).get_height()
				
		printings = []
		buttons = [Button([400], 300, 100, 50, font=font, smooting=True, printing='Create', funk=self.new)]

		i = 0
		for key in self.settings.keys():
			printings.append([font.render(key, True, (0, 0, 0)), (20, 20 + i * (h + 10))])
			printings.append([font.render(str(self.settings[key]), True, (0, 0, 0)),
			 (270 + (50 - font.render(str(self.settings[key]), True, (0, 0, 0)).get_width()) // 2, 20 + i * (h + 10))])
			

			buttons.append(Button(320, 20 + i * (h + 10), 20, 20, font=font, printing='+', smooting=True, funk=self.changeSetting, args=(key, 1)))
			buttons.append(Button(250, 20 + i * (h + 10), 20, 20, font=font, printing='-', smooting=True, funk=self.changeSetting, args=(key, -1)))
			
			i += 1

		self.creationWindow = Window(self.screen, [self.size[0]], [self.size[1]], 400, 400, buttons=buttons, printings=printings, caption='Creating new simulation')
		self.creationWindow.run()

	def changeSetting(self, keyChange):
		key    = keyChange[0]
		change = keyChange[1]

		if key == 'FPS':
			if change < 0:
				if self.settings[key] > 1:
					self.settings[key] += change

			else:
				self.settings[key] += change
		else:
			self.settings[key] += change * 10

		font = pygame.font.Font('main.ttf', 20)
		h = font.render('0', True, (0, 0, 0)).get_height()
		
		printings = []
		
		i = 0
		for key in self.settings.keys():
			printings.append([font.render(key, True, (0, 0, 0)), (20, 20 + i * (h + 10))])
			printings.append([font.render(str(self.settings[key]), True, (0, 0, 0)),
			 (270 + (50 - font.render(str(self.settings[key]), True, (0, 0, 0)).get_width()) // 2, 20 + i * (h + 10))])

			i += 1
		self.creationWindow.printings = printings

	def drawObjects(self):
		if self.start_pos != None:
			if self.instrument == 'Circle':
				r = int((((self.start_pos[0] - self.mousePos[0])**2 + (self.start_pos[1] - self.mousePos[1])**2))**0.5)
				pygame.draw.circle(self.screen, (0, 0, 255), self.start_pos, r)
				pygame.draw.circle(self.screen, (0, 0, 0), self.start_pos, r, 2)

			elif self.instrument == 'Box':
				x = self.mousePos[0] if self.start_pos[0] > self.mousePos[0] else self.start_pos[0]
				y = self.mousePos[1] if self.start_pos[1] > self.mousePos[1] else self.start_pos[1]

				w = abs(self.start_pos[0] - self.mousePos[0])
				h = abs(self.start_pos[1] - self.mousePos[1])
				pygame.draw.rect(self.screen, (0, 255, 0), (x, y, w, h))
				pygame.draw.rect(self.screen, (0, 0, 0), (x, y, w, h), 2)

			elif self.instrument == 'Paddle':
				pygame.draw.line(self.screen, (122, 122, 122), self.start_pos, self.mousePos, 5)

	def render(self):
		for obj in self.objects:
			obj.add(self.space)

	def simRun(self):
		self.space = pymunk.Space()
		self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
		self.space.gravity = self.settings['Gravity X'], self.settings['Gravity Y']
		self.render()

		runing = True
		while runing:
			for event in pygame.event.get():
				if event.type == 256:
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						runing = False

			self.simDraw()
			
			pygame.display.update()

			self.clock.tick(self.FPS)
			self.space.step(1/self.FPS)

	def simDraw(self):
		self.screen.fill((0, 122, 122))
		p = self.font.render('To escape from simulation press space', True, (0, 0, 0))
		self.screen.blit(p, ((self.screen.get_width() - p.get_width())//2, 0))

		self.space.debug_draw(self.draw_options)

engine = App()
engine.run()