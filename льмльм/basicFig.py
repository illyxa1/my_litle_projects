import pygame
from menu_draw import *
from window import *
from entery import Entery
import pymunk
import pymunk.pygame_util

class Circle:
	def __init__(self, screen, pos, r, num):
		self.pos = pos
		self.r = r if r > 0 else 1

		self.color = (0, 0, 255)

		self.mass = 10
		self.elasticity = 1
		self.friction = 1

		self.typ = 'Circle'
		self.num = num

		self.screen = screen
		self.moving = False

	def startMove(self, mousePos):
		if (mousePos[0] - self.pos[0])**2 + (mousePos[1] - self.pos[1])**2 <= self.r ** 2:
			self.moving = True
			self.delta = mousePos[0] - self.pos[0], mousePos[1] - self.pos[1]

			return True

	def move(self, mousePos):
		if self.moving:
			self.pos = mousePos[0] - self.delta[0], mousePos[1] - self.delta[1]

	def endMove(self):
		self.moving = False

	def add(self, space):
		body = pymunk.Body(self.mass, pymunk.moment_for_circle(self.mass, 0, self.r))
		body.position = self.pos
		shape = pymunk.Circle(body, self.r)
		shape.elasticity = self.elasticity
		shape.friction = self.friction

		space.add(body, shape)
		
	def draw(self):
		pygame.draw.circle(self.screen, self.color, self.pos, self.r)
		pygame.draw.circle(self.screen, (0, 0, 0), self.pos, self.r, 2)
		pygame.draw.circle(self.screen, (0, 0, 0), self.pos, 2)

		font = pygame.font.Font('main.ttf', 15)
		self.screen.blit(font.render(str(self.num), True, (0, 0, 0)), self.pos)

	def changeR(self, delta):
		self.r += delta
		self.draw()

	def click(self, mousePos, button, num=0, dubl=False):
		if (mousePos[0] - self.pos[0])**2 + (mousePos[1] - self.pos[1])**2 <= self.r ** 2:
			if button == 3:
				font = pygame.font.Font('main.ttf', 20)
				printings=[]


				self.enterys = []
				pr = {
					'x'    : self.pos[0],
					'y'    : self.pos[1],
					'radius'    : self.r,

					'color': self.color,
					'mass' : self.mass,
					'elasticity' : self.elasticity,
					'friction' : self.friction
				}

				h = font.render('0', True, (0, 0, 0)).get_height()
				i = 0
				for key in pr.keys():
					printings.append([font.render(key, True, (0, 0, 0)),     (5, 5 + (h + 3) * i)])
					if i == 3:
						printings.append([font.render(str(pr[key]), True, (0, 0, 0)), (105, 5 + (h + 3) * i)])
					
					else:
						self.enterys.append(					
							Entery(105, (5 + (h + 3) * i), font, onlycounts=True, smooting=True, writing=str(pr[key]),
						space=5, spacey=1, w=20, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
					)
					i += 1

				# self.enterys = [
				# 	Entery(105, (5 + (h + 3) * (i-1)), font, onlycounts=True, smooting=True, writing=str(self.mass),
				# 		space=5, spacey=1, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
				# ]
				buttons = [
					Button([200], (10 + (h + 3) * i), 80, h+5, font, funk=self.aply, printing='Aply')
				]

				size = self.screen.get_width(), self.screen.get_height()
				posY = size[1] - (30 + (h + 3) * (i + 1)) if mousePos[1] + (30 + (h + 3) * (i + 1)) > size[1] else mousePos[1]
				posX = size[0] - 200 if mousePos[0] + 200 > size[0] else mousePos[0]

				win = Window(self.screen, posX, posY, 200, (20 + (h + 3) * (i + 1)), 
					printings=printings, enterys=self.enterys, buttons=buttons)
				win.run()
				return True

			if button == 2:
				return True

			if button == 1 and dubl:
				copy = Circle(self.screen, self.pos,self.r, num+1)
				copy.color = self.color

				copy.mass = self.mass
				copy.elasticity = self.elasticity
				copy.friction = self.friction

				return copy

			else:
				return False
				
	def changeSetting(self, pos):
		font = pygame.font.Font('main.ttf', 20)
		
		printings=[]
		self.enterys = []
		
		pr = {
			'x'    : self.pos[0],
			'y'    : self.pos[1],
			'radius'    : self.r,

			'color': self.color,
			'mass' : self.mass,
			'elasticity' : self.elasticity,
			'friction' : self.friction
		}

		h = font.render('0', True, (0, 0, 0)).get_height()
		i = 0

		for key in pr.keys():
			printings.append([font.render(key, True, (0, 0, 0)),     (5, 5 + (h + 3) * i)])
			if i == 3:
				printings.append([font.render(str(pr[key]), True, (0, 0, 0)), (105, 5 + (h + 3) * i)])
					
			else:
				self.enterys.append(					
					Entery(105, (5 + (h + 3) * i), font, onlycounts=True, smooting=True, writing=str(pr[key]),
				space=5, spacey=1, w=20, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
			)
			i += 1

		# self.enterys = [
		# 	Entery(105, (5 + (h + 3) * (i-1)), font, onlycounts=True, smooting=True, writing=str(self.mass),
		# 		space=5, spacey=1, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
		# ]
		buttons = [
			Button([200], (10 + (h + 3) * i), 80, h+5, font, funk=self.aply, printing='Aply')
		]

		# size = self.screen.get_width(), self.screen.get_height()
		# posY = size[1] - (30 + (h + 3) * (i + 1)) if mousePos[1] + (30 + (h + 3) * (i + 1)) > size[1] else mousePos[1]
		# posX = size[0] - 200 if mousePos[0] + 200 > size[0] else mousePos[0]

		win = Window(self.screen, pos[0], pos[1], 200, (20 + (h + 3) * (i + 1)), 
			printings=printings, enterys=self.enterys, buttons=buttons)
		win.run()
		return True

	def aply(self):
		self.pos = int(self.enterys[0].writing), int(self.enterys[1].writing)
		self.r = int(self.enterys[2].writing) if int(self.enterys[2].writing) > 0 else 1

		self.mass = int(self.enterys[3].writing) if int(self.enterys[3].writing) > 0 else 1
		self.elasticity = float(self.enterys[4].writing)
		self.friction = float(self.enterys[5].writing)

	def parametrate(self):
		return {
			'pos': self.pos,
			'r': self.r,

			'mass': self.mass,
			'elasticity': self.elasticity,
			'friction': self.friction,

			'typ': self.typ,
			'num': self.num
		}

class Box:
	def __init__(self, screen, x, y, w, h, num):
		self.x = x 
		self.y = y
		self.w = w
		self.h = h

		self.color = (0, 255, 0)

		self.rect = pygame.Rect(x, y, w, h)

		self.mass = 10
		self.friction = 1
		self.elasticity = 1

		self.typ = 'Box'
		self.num = num

		self.screen = screen
		self.moving = False

	def parametrate(self):
		return {
			'x':self.x,
			'y':self.y,
			'w':self.w,
			'h':self.h,

			'typ':self.typ,
			'num':self.num,

			'mass':self.mass,
			'friction':self.friction,
			'elasticity':self.elasticity			
		}

	def startMove(self, mousePos):
		if self.rect.collidepoint(mousePos):
			self.moving = True
			self.delta = mousePos[0] - self.x, mousePos[1] - self.y

			return True

	def move(self, mousePos):
		if self.moving:
			self.x = mousePos[0] - self.delta[0]
			self.y = mousePos[1] - self.delta[1]
			self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


	def endMove(self):
		self.moving = False
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		

	def add(self, space):
		body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, (self.w, self.h)))
		body.position = (self.x + self.w/2, self.y + self.h/ 2)
		shape = pymunk.Poly.create_box(body, (self.w, self.h))
		shape.elasticity = self.elasticity
		shape.friction = self.friction

		space.add(body, shape)

	def draw(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
		pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 2)
		pygame.draw.circle(self.screen, (0, 0, 0), (self.x + self.w/2, self.y + self.h/2), 2)

		font = pygame.font.Font('main.ttf', 15)
		self.screen.blit(font.render(str(self.num), True, (0, 0, 0)), (self.x + self.w/2, self.y + self.h/2))

	def click(self, mousePos, button, dubl=False, num=0):
		if self.rect.collidepoint(mousePos):
			if button == 3:
				font = pygame.font.Font('main.ttf', 20)
				printings=[]
				self.enterys = []
				pr = {
					'x'    : self.x,
					'y'    : self.y,
					'w'    : self.w,
					'h'    : self.h,

					'color': self.color,
					'mass' : self.mass,
					'elasticity' : self.elasticity,
					'friction' : self.friction
				}

				h = font.render('0', True, (0, 0, 0)).get_height()
				i = 0
				for key in pr.keys():
					printings.append([font.render(key, True, (0, 0, 0)),     (5, 5 + (h + 3) * i)])
					if i == 4:
						printings.append([font.render(str(pr[key]), True, (0, 0, 0)), (105, 5 + (h + 3) * i)])
					
					else:
						self.enterys.append(					
							Entery(105, (5 + (h + 3) * i), font, onlycounts=True, smooting=True, writing=str(pr[key]),
						space=5, spacey=1, w=20, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
					)
					i += 1

				# self.enterys = [
				# 	Entery(105, (5 + (h + 3) * (i-1)), font, onlycounts=True, smooting=True, writing=str(self.mass),
				# 		space=5, spacey=1, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
				# ]
				buttons = [
					Button([200], (10 + (h + 3) * i), 80, h+5, font, funk=self.aply, printing='Aply')
				]

				size = self.screen.get_width(), self.screen.get_height()
				posY = size[1] - (30 + (h + 3) * (i + 1)) if mousePos[1] + (30 + (h + 3) * (i + 1)) > size[1] else mousePos[1]
				posX = size[0] - 200 if mousePos[0] + 200 > size[0] else mousePos[0]

				win = Window(self.screen, posX, posY, 200, (20 + (h + 3) * (i + 1)), 
					printings=printings, enterys=self.enterys, buttons=buttons)
				win.run()
				return True

			if button == 2:
				return True

			if button == 1 and dubl:
				copy = Box(self.screen, self.x, self.y, self.w, self.h, num+1)
				copy.color = self.color

				copy.mass = self.mass
				copy.elasticity = self.elasticity
				copy.friction = self.friction

				return copy

			else:
				return False
	def changeSetting(self, pos):
		font = pygame.font.Font('main.ttf', 20)
		
		printings=[]
		self.enterys = []
		
		pr = {
			'x'    : self.x,
			'y'    : self.y,
			'w'    : self.w,
			'h'    : self.h,

			'color': self.color,
			'mass' : self.mass,
			'elasticity' : self.elasticity,
			'friction' : self.friction
		}

		h = font.render('0', True, (0, 0, 0)).get_height()
		i = 0

		for key in pr.keys():
			printings.append([font.render(key, True, (0, 0, 0)),     (5, 5 + (h + 3) * i)])
			if i == 4:
				printings.append([font.render(str(pr[key]), True, (0, 0, 0)), (105, 5 + (h + 3) * i)])
					
			else:
				self.enterys.append(					
					Entery(105, (5 + (h + 3) * i), font, onlycounts=True, smooting=True, writing=str(pr[key]),
				space=5, spacey=1, w=20, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
			)
			i += 1

		# self.enterys = [
		# 	Entery(105, (5 + (h + 3) * (i-1)), font, onlycounts=True, smooting=True, writing=str(self.mass),
		# 		space=5, spacey=1, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
		# ]
		buttons = [
			Button([200], (10 + (h + 3) * i), 80, h+5, font, funk=self.aply, printing='Aply')
		]

		# size = self.screen.get_width(), self.screen.get_height()
		# posY = size[1] - (30 + (h + 3) * (i + 1)) if mousePos[1] + (30 + (h + 3) * (i + 1)) > size[1] else mousePos[1]
		# posX = size[0] - 200 if mousePos[0] + 200 > size[0] else mousePos[0]

		win = Window(self.screen, pos[0], pos[1], 200, (20 + (h + 3) * (i + 1)), 
			printings=printings, enterys=self.enterys, buttons=buttons)
		win.run()
		return True

	def aply(self):
		self.x = int(self.enterys[0].writing)
		self.y = int(self.enterys[1].writing)
		self.w = int(self.enterys[2].writing) if int(self.enterys[2].writing) > 0 else 1
		self.h = int(self.enterys[3].writing) if int(self.enterys[3].writing) > 0 else 1

		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

		self.mass = int(self.enterys[4].writing) if int(self.enterys[4].writing) > 0 else 1
		self.elasticity = float(self.enterys[5].writing)
		self.friction = float(self.enterys[6].writing)

class Paddle:
	def __init__(self, screen, pos, pos2, w, num):
		self.pos = pos
		self.pos2 = pos2
		self.w = w

		self.color = (122, 122, 122)

		self.friction = 1
		self.elasticity = 1

		self.typ = 'Paddle'
		self.num = num

		self.screen = screen

		self.moving = False
		self.part = 1 # 1/2

	def parametrate(self):
		return {
			'pos':self.pos,
			'pos2':self.pos2,
			'w':self.w,

			'typ':self.typ,
			'num':self.num,

			'friction':self.friction,
			'elasticity':self.elasticity			
		}
	
	def startMove(self, mousePos):
		if (mousePos[0] - self.pos[0])**2 + (mousePos[1] - self.pos[1])**2 <= 16:
			self.part = 1
			self.moving = True
			self.delta = mousePos[0] - self.pos[0], mousePos[1] - self.pos[1]


			return True

		elif (mousePos[0] - self.pos2[0])**2 + (mousePos[1] - self.pos2[1])**2 <= 16:
			self.part = 2
			self.moving = True
			self.delta = mousePos[0] - self.pos2[0], mousePos[1] - self.pos2[1]


			return True

	def move(self, mousePos):
		if self.moving:
			if self.part == 1:
				self.pos = mousePos[0] - self.delta[0], mousePos[1] - self.delta[1]

			else:
				self.pos2 = mousePos[0] - self.delta[0], mousePos[1] - self.delta[1]


	def endMove(self):
		self.moving = False

	def add(self, space):
		segment = pymunk.Segment(space.static_body, self.pos, self.pos2, self.w)
		segment.elasticity = self.elasticity
		segment.friction = self.friction

		space.add(segment)

	def draw(self):
		pygame.draw.line(self.screen, self.color, self.pos, self.pos2, self.w)
		pygame.draw.circle(self.screen, (0, 0, 0),
			self.pos, 4)

		pygame.draw.circle(self.screen, (0, 0, 0),
			self.pos2, 4)

		font = pygame.font.Font('main.ttf', 15)
		self.screen.blit(font.render(str(self.num), True, (0, 0, 0)), 
			self.pos)

	def click(self, mousePos, button, dubl=False, num=0):
		pass

	def changeSetting(self, pos):
		font = pygame.font.Font('main.ttf', 20)
		
		printings=[]
		self.enterys = []
		
		pr = {
			'x1'    : self.pos[0],
			'y1'    : self.pos[1],
			'x2'    : self.pos2[0],
			'y2'    : self.pos2[1],
			'w'     : self.w,

			'color': self.color,
			'elasticity' : self.elasticity,
			'friction' : self.friction
		}

		h = font.render('0', True, (0, 0, 0)).get_height()
		i = 0

		for key in pr.keys():
			printings.append([font.render(key, True, (0, 0, 0)),     (5, 5 + (h + 3) * i)])
			if i == 5:
				printings.append([font.render(str(pr[key]), True, (0, 0, 0)), (105, 5 + (h + 3) * i)])
					
			else:
				self.enterys.append(					
					Entery(105, (5 + (h + 3) * i), font, onlycounts=True, smooting=True, writing=str(pr[key]),
				space=5, spacey=1, w=20, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
			)
			i += 1

		# self.enterys = [
		# 	Entery(105, (5 + (h + 3) * (i-1)), font, onlycounts=True, smooting=True, writing=str(self.mass),
		# 		space=5, spacey=1, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
		# ]
		buttons = [
			Button([200], (10 + (h + 3) * i), 80, h+5, font, funk=self.aply, printing='Aply')
		]

		# size = self.screen.get_width(), self.screen.get_height()
		# posY = size[1] - (30 + (h + 3) * (i + 1)) if mousePos[1] + (30 + (h + 3) * (i + 1)) > size[1] else mousePos[1]
		# posX = size[0] - 200 if mousePos[0] + 200 > size[0] else mousePos[0]

		win = Window(self.screen, pos[0], pos[1], 200, (20 + (h + 3) * (i + 1)), 
			printings=printings, enterys=self.enterys, buttons=buttons)
		win.run()
		return True

	def aply(self):
		x1 = int(self.enterys[0].writing)
		y1 = int(self.enterys[1].writing)
		x2 = int(self.enterys[2].writing)
		y2 = int(self.enterys[3].writing)

		self.pos = (x1, y1)
		self.pos2 = (x2, y2)

		self.w = int(self.enterys[4].writing)

		self.elasticity = float(self.enterys[5].writing)
		self.friction = float(self.enterys[6].writing)

class Link:
	def __init__(self, screen, pos, pos2, w, num):
		self.pos = pos
		self.pos2 = pos2
		self.w = w

		self.color = (122, 122, 122)

		self.friction = 1
		self.elasticity = 1

		self.typ = 'Paddle'
		self.num = num

		self.screen = screen

	def add(self, space):
		segment = pymunk.Segment(space.static_body, self.pos, self.pos2, self.w)
		segment.elasticity = self.elasticity
		segment.friction = self.friction

		space.add(segment)

	def draw(self):
		pygame.draw.line(self.screen, self.color, self.pos, self.pos2, self.w)
		pygame.draw.circle(self.screen, (0, 0, 0),
			self.pos, 2)

		font = pygame.font.Font('main.ttf', 15)
		self.screen.blit(font.render(str(self.num), True, (0, 0, 0)), 
			self.pos)

	def click(self, mousePos, button):
		pass

	def changeSetting(self, pos):
		font = pygame.font.Font('main.ttf', 20)
		
		printings=[]
		self.enterys = []
		
		pr = {
			'x1'    : self.pos[0],
			'y1'    : self.pos[1],
			'x2'    : self.pos2[0],
			'y2'    : self.pos2[1],
			'w'     : self.w,

			'color': self.color,
			'elasticity' : self.elasticity,
			'friction' : self.friction
		}

		h = font.render('0', True, (0, 0, 0)).get_height()
		i = 0

		for key in pr.keys():
			printings.append([font.render(key, True, (0, 0, 0)),     (5, 5 + (h + 3) * i)])
			if i == 5:
				printings.append([font.render(str(pr[key]), True, (0, 0, 0)), (105, 5 + (h + 3) * i)])
					
			else:
				self.enterys.append(					
					Entery(105, (5 + (h + 3) * i), font, onlycounts=True, smooting=True, writing=str(pr[key]),
				space=5, spacey=1, w=20, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
			)
			i += 1

		# self.enterys = [
		# 	Entery(105, (5 + (h + 3) * (i-1)), font, onlycounts=True, smooting=True, writing=str(self.mass),
		# 		space=5, spacey=1, colorS=(122, 122, 122), colorAS=(0, 255, 0), border=2, colorW=(0, 0, 0))
		# ]
		buttons = [
			Button([200], (10 + (h + 3) * i), 80, h+5, font, funk=self.aply, printing='Aply')
		]

		# size = self.screen.get_width(), self.screen.get_height()
		# posY = size[1] - (30 + (h + 3) * (i + 1)) if mousePos[1] + (30 + (h + 3) * (i + 1)) > size[1] else mousePos[1]
		# posX = size[0] - 200 if mousePos[0] + 200 > size[0] else mousePos[0]

		win = Window(self.screen, pos[0], pos[1], 200, (20 + (h + 3) * (i + 1)), 
			printings=printings, enterys=self.enterys, buttons=buttons)
		win.run()
		return True

	def aply(self):
		x1 = int(self.enterys[0].writing)
		y1 = int(self.enterys[1].writing)
		x2 = int(self.enterys[2].writing)
		y2 = int(self.enterys[3].writing)

		self.pos = (x1, y1)
		self.pos2 = (x2, y2)

		self.w = int(self.enterys[4].writing)

		self.elasticity = float(self.enterys[5].writing)
		self.friction = float(self.enterys[6].writing)