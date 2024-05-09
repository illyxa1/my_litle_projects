import pygame
pygame.init()

def test():
	print('pass')

def drawMenu(screen, size):
	ots = 3
	w = 3
	buttons = 55
	pygame.draw.rect(screen, (0, 0, 0), (ots, ots + buttons, size[0] - ots * 2, size[1] - buttons -ots * 2), w)
	pygame.draw.rect(screen, (0, 0, 0), (ots, ots, size[0] - ots * 2, ots + buttons - ots * 2), w)

	return (ots, ots + buttons, size[0] - ots * 2, size[1] - buttons -ots * 2)

class Button:
	def __init__(self, x, y, w, h, font, onlyOneClick=False, funk=test, args=None, smooting=False, bw=2, colorU=(42, 42, 42), colorD=(12, 12, 12), colorM=(32, 32, 32), colorB=(0, 0, 0), colorP=(64, 64, 64), printing='Button'):
		self.x = x if type(x)==int else (x[0] - w) // 2 
		self.y = y if type(y)==int else (y[0] - h) // 2 
		self.w = w
		self.h = h

		self.hitbox = pygame.Rect(self.x, self.y, w, h)

		self.font = font

		self.bw = bw

		self.colorM = colorM
		self.colorB = colorB
		self.colorP = colorP
		self.colorU = colorU
		self.colorD = colorD

		self.printing = printing
		self.font = font

		self.funk = funk
		self.args = args

		self.smooting = smooting

		self.onlyOneClick = onlyOneClick
		self.used = False

	def draw(self, screen, mousePos):
		pygame.draw.rect(screen, self.colorM, (self.x, self.y, self.w, self.h))
		if not self.used:
			if self.hitbox.collidepoint(mousePos):
				pygame.draw.rect(screen, self.colorU, (self.x, self.y, self.w, self.h))

			if self.bw:
				pygame.draw.rect(screen, self.colorB, (self.x, self.y, self.w, self.h), self.bw)
		
		else:
			pygame.draw.rect(screen, self.colorD, (self.x, self.y, self.w, self.h))

		writing = self.font.render(self.printing, self.smooting, self.colorP)
		x = self.x + (self.w - writing.get_width()) / 2
		y = self.y + (self.h - writing.get_height()) / 2
		screen.blit(writing, (x, y))

	def click(self, mousePos):
		if not self.used:
			if self.hitbox.collidepoint(mousePos):
				if self.args:
					self.funk(self.args)

				else:
					self.funk()

				if self.onlyOneClick:
					self.used = True
				return True

class BList:
	def __init__(self, x, y , w, h, font, smooting=False, buttons={}, bw=2, colorU=(42, 42, 42), colorM=(32, 32, 32), colorB=(0, 0, 0), colorP=(64, 64, 64), printing='Buttons'):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.hitbox = pygame.Rect(x, y, w + 14, h)

		self.colorM = colorM
		self.colorU = colorU
		self.colorB = colorB

		self.bw = bw

		self.writing = font.render(printing, smooting, colorP) 

		self.active = False

		self.arrow = pygame.image.load('arrow.bmp')
		self.arrow.set_colorkey((255, 255, 255))

		self.smooting = smooting

		self.buttons = []
		y1 = 1
		for key in buttons.keys():
			self.buttons.append(Button(x, y + y1 * h, w, h, font, funk=buttons[key] if type(buttons[key])!=list else buttons[key][0], args=None if type(buttons[key])!=list else buttons[key][1]
				, smooting=self.smooting, printing=key))
			y1 += 1

	def draw(self, screen, mousePos):
		pygame.draw.rect(screen, self.colorM, (self.x, self.y, self.w + 14, self.h))

		if self.hitbox.collidepoint(mousePos):
			pygame.draw.rect(screen, self.colorU, (self.x, self.y, self.w + 14, self.h))

		if self.bw:
			pygame.draw.rect(screen, self.colorB, (self.x, self.y, self.w + 14, self.h), self.bw)

		x = self.x + (self.w - self.writing.get_width()) / 2
		y = self.y + (self.h - self.writing.get_height()) / 2
		screen.blit(self.writing, (x, y))

		if self.active:
			screen.blit(self.arrow, (self.x + (self.w + 12 - self.arrow.get_width()), self.y + (self.h - self.arrow.get_height())//2))
			for button in self.buttons:
				button.draw(screen, mousePos)

		else:
			screen.blit(pygame.transform.rotate(self.arrow, 90), (self.x + (self.w + 12 - self.arrow.get_height()), self.y + (self.h - self.arrow.get_width())//2))

	def click(self, mousePos):
		if self.hitbox.collidepoint(mousePos):
			self.active = True if not self.active else False

		else:
			if self.active:
				for button in self.buttons:
					if button.click(mousePos):
						return True
			self.active = False