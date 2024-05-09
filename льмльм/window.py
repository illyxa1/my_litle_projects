import pygame
from menu_draw import *

pygame.init()

font = pygame.font.Font('main.ttf', 15)

class Window:
	def __init__(self, screen, x, y, w, h, buttons=[], printings=[], bLists=[], enterys=[], caption=' ', font=font):
		self.x = x if type(x) != list else (x[0] - w)//2
		self.y = y if type(y) != list else (y[0] - h)//2

		self.w = w
		self.h = h

		self.screen = screen
		self.hat = pygame.Surface((w, 22))
		self.surf = pygame.Surface((w, h))

		self.font = font

		self.setCaption(caption)

		self.runs = True

		self.Bexit = Button(w-42, 1, 40, 18, funk=self.close, font=font, smooting=True, printing='X', colorM=(255, 255, 255), colorU=(255, 0, 0))
		
		self.buttons = buttons
		self.bLists = bLists
		self.printings = printings
		self.enterys = enterys

	def setCaption(self, caption):
		self.printing = self.font.render(caption, True, (0, 0, 0))

	def draw(self):
		self.surf.fill((0, 122, 122))
		pygame.draw.rect(self.surf, (0, 0, 0), (2, 2, self.w - 4, self.h - 4), 4)		

		pygame.draw.rect(self.hat, (255, 255, 255), (0, 0, self.w, 20))
		
		self.hat.blit(self.printing, (2, 2))
		self.Bexit.draw(self.hat, self.mousePos2)

		for button in self.buttons:
			button.draw(self.surf, self.mousePos)

		for bList in self.bLists:
			bList.draw(self.surf, self.mousePos)

		for printing in self.printings:
			self.surf.blit(printing[0], printing[1])

		for entery in self.enterys:
			entery.draw(self.surf)

		self.screen.blit(self.hat, (self.x, self.y))
		self.screen.blit(self.surf, (self.x, self.y+20))

	def run(self):
		self.runs = True
		while self.runs:
			x, y = pygame.mouse.get_pos()
			self.mousePos = x - self.x, y - self.y - 20
			self.mousePos2 = (x-self.x, y-self.y)
			for event in pygame.event.get():
				if event.type == 256:
					quit()

				if event.type == pygame.KEYDOWN:
					for entery in self.enterys:
						entery.inputWord(event.unicode, event.key)

				if event.type == pygame.MOUSEBUTTONDOWN:
					self.Bexit.click(self.mousePos2)

					for button in self.buttons:
						button.click(self.mousePos)

					for bList in self.bLists:
						bList.click(self.mousePos)

					for entery in self.enterys:
						entery.activate(self.mousePos)

			self.draw()
			pygame.display.update()

	def close(self):
		self.runs = False