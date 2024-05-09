import pymunk
import pymunk.pygame_util
import pygame
from random import randint

pygame.init()

def ball_particles():
	size = (500, 700)
	screen = pygame.display.set_mode(size)

	draw_options = pymunk.pygame_util.DrawOptions(screen)

	space = pymunk.Space()
	space.gravity = 0, 0

	clock = pygame.time.Clock()
	FPS = 60

	pts = [(10, 10), (size[0] - 10, 10), (size[0] - 10, size[1] - 10), (10, size[1] - 10)]
	for i in range(4):
		segment = pymunk.Segment(space.static_body, pts[i], pts[(i+1)%4], 2)
		segment.elasticity = 1
		segment.friction = 0
		space.add(segment)

	j = 1000
	for i in range(j):
		ball_mass, ball_radius = 1, 5000 / j 
		ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
		ball_body = pymunk.Body(ball_mass, ball_moment)
		ball_body.position = 40 +  i * (size[0] - 80) / j, 40 +  i * (size[1] - 80) / j
		ball_shape = pymunk.Circle(ball_body, ball_radius)
		ball_shape.color = (i * 255 / j, i * 255 / j, 0, 0)
		impulse = randint(-1000, 1000), randint(-1000, 1000)
		ball_body.apply_impulse_at_local_point(impulse)
		ball_shape.elasticity = 1
		ball_shape.friction = 0

		space.add(ball_body, ball_shape)

	while True:
		for event in pygame.event.get():
			if event.type == 256:
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					FPS += 10

				elif event.key == pygame.K_DOWN:
					if FPS > 10:
						FPS -= 10

		pygame.display.update()
		pygame.display.set_caption(str(FPS))
		
		screen.fill((0, 122, 255))
		space.debug_draw(draw_options)

		space.step(1 / FPS)
		clock.tick(FPS)