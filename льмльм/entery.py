import pygame

class Entery:
	def __init__(self, x, y, font, onlycounts=False, smooting=False, w=10, colorW=(0, 255, 0), colorS=(0, 122, 0), colorAS=(0, 255, 122), border=1, writing='', space=10, spacey=5):
		self.x = x # позиция
		self.y = y # позиция
		
		self.colorM = None # фон
		self.colorS = colorS # граница
		self.colorAS = colorAS # граница в активе
		self.colorW = colorW # надпись

		self.border = border # тощина границы

		self.font = font # сам шрифт

		self.writing = writing # надпись
		self.printing = font.render(writing, smooting, colorW) #отрендереная надпись
		self.helper = (font.render('I', smooting, colorW).get_width(), font.render('I', False, colorW).get_height())

		self.w = w # размер
		self.h = self.helper[1] + spacey# размер
		self.unscalable = False #рамка не масштабируется

		self.space = space #отступ от границы по х
		self.spacey = spacey #отступ от границы по у
		
		self.hitbox = pygame.Rect(x, y, self.w + space * 2, self.h + spacey) #хитбокс

		self.input = False #активно/нет

		self.inputer = len(writing)

		self.smooting = smooting
		self.onlycounts = onlycounts

	def edit(self, unscalable=False, colorM=None):
		self.unscalable = unscalable

		if colorM:
			self.colorM = colorM

	def draw(self, screen, colorBG=(0, 0, 0)):
		if not self.unscalable: # отображение масштабируемого вводного поля...
			if self.colorM:
				pygame.draw.rect(screen, self.colorM, self.hitbox) # рисуем фон
			
			if self.border > 0: # рисуем границы
				color = self.colorAS if self.input else self.colorS
				pygame.draw.rect(screen, color, self.hitbox, self.border)
			
			screen.blit(self.printing, (self.x + self.space, self.y + self.spacey)) # прикрепляем надпись
			
			printing2 = self.font.render(self.writing[:self.inputer], True, self.colorW) # вспомогательная надпись
			dd = printing2.get_width() + self.space # дельта	
			if self.input:
				pygame.draw.line(screen, (255, 255, 255), (self.x + dd, self.y + self.spacey), (self.x + dd, self.y + self.h - self.spacey)) # отрисовка инпутера
		
		else:
			entery = pygame.Surface((self.w + self.space * 2, self.h + self.spacey * 2)) # создаём поверхность (весёлая вещь)
			entery.fill(colorBG)
			if self.colorM:
				pygame.draw.rect(entery, self.colorM, (0, 0, self.w + self.space * 2, self.printing.get_height() + self.spacey*2)) 

			if self.border > 0:
				color = self.colorAS if self.input else self.colorS
				pygame.draw.rect(entery, color, (0, 0, self.w + self.space * 2, self.printing.get_height() + self.spacey*2), self.border)

			delta = self.printing.get_width() - self.w if self.printing.get_width() > self.w else 0 # создаём дельту относительно левого края
			
			printing2 = self.font.render(self.writing[self.inputer:], True, self.colorW) # вспомогательная надпись
			inputerPos = self.printing.get_width() + self.space - delta - printing2.get_width() # определяем конечную позицию
			if self.input:
				pygame.draw.line(entery, (255, 255, 255), (inputerPos, 0 + self.spacey), (inputerPos, 0 - self.spacey + self.h)) # рисуем наконец инпутер
			
			entery.blit(self.printing, (0 + self.space - delta, 0 + self.spacey)) # окончательная отрисовка
			screen.blit(entery, (self.x, self.y))

	def activate(self, mousepos):
		if self.hitbox.collidepoint(mousepos):
			self.input = True

		else:
			self.input = False

	def inputWord(self, code, key):
		if self.input:
			if key == pygame.K_BACKSPACE: # стираем назад
				if self.inputer > 0:
					self.writing = self.writing[:self.inputer-1] + self.writing[self.inputer:]
					self.inputer -= 1

			elif key == pygame.K_DELETE: # стираем вперёд...
				self.writing = self.writing[:self.inputer] + self.writing[self.inputer+1:]
				
			elif key == pygame.K_RIGHT: # перемещение инпутера
				if self.inputer < len(self.writing):
					self.inputer += 1

			elif key == pygame.K_LEFT: # перемещение инпутера
				if self.inputer > 0:
					self.inputer -= 1

			elif key == pygame.K_LCTRL or key == pygame.K_RCTRL:
				self.writing = ''
				self.inputer = 0

			# блокаем ненужные клавиши...
			elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
				pass

			elif key == pygame.K_LALT or key == pygame.K_RALT:
				pass

			elif key == pygame.K_RETURN:
				pass

			else:
				# self.writing = self.writing[0:-1]
				try:
					if str(code) != '-' and str(code) != '.':
						int(float(str(code)))
					self.writing = self.writing[:self.inputer] + code + self.writing[self.inputer:]
					self.inputer += 1
				
				except ValueError:
					if not self.onlycounts:
						self.writing = self.writing[:self.inputer] + code + self.writing[self.inputer:]
						self.inputer += 1

			self.printing = self.font.render(self.writing, self.smooting, self.colorW)

			if not self.unscalable:
				delta = self.printing.get_width() if self.printing.get_width() >= self.w else self.w
				self.hitbox = pygame.Rect(self.x, self.y,delta + self.space*2, self.h + self.spacey)
				# меняем размер хитбокса после ввода...

	def update(self):
		self.hitbox = pygame.Rect(self.x, self.y, self.w + self.space * 2, self.printing.get_height() + self.spacey*2) #хитбокс
