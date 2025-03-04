import pygame
from pygame.locals import *
import os
import worlds
from menu import menu_page

pygame.init()

class Font_types():
	fonts = {
	"40" : pygame.font.Font(None, 40),
	"50" : pygame.font.Font(None, 50),
	"80" : pygame.font.Font(None, 80)
	}

"""
infos = pygame.display.Info()

screen_width, screen_height = infos.current_w, infos.current_h

resolutions = [(1920, 1080), (1760, 990), (1680, 1050), (1600, 900), (1440, 900), (1366, 768), (1280, 1024), (1280, 800), (1280, 720), (1152, 870), (1152, 864), (1128, 634), (1024, 768), (832, 624), (800, 600)]
print(len(resolutions))

index = -1
for i in range(len(resolutions)):
	if resolutions[i][0] == screen_width and resolutions[i][1] == screen_height:
		print("Megvan!")
		index = i

d = -1.42857142857143
tile_size = 50
if i == 0:
	tile_size = 50
else:
	tile_size += i*(d)

tile_size = int(tile_size)
"""


BLACK = (0, 0, 0)


infos = pygame.display.Info()
screen_width, screen_height = infos.current_w, infos.current_h
resolutions = [(1920, 1080), (1760, 990), (1680, 1050), (1600, 900), (1440, 900), (1366, 768), (1280, 1024), 
			   (1280, 800), (1280, 720), (1152, 870), (1152, 864), (1128, 634), (1024, 768), (832, 624), (800, 600)]

action = menu_page(screen_width, screen_height, Font_types.fonts, resolutions)

if action == 1:
	run = 1
else:
	run = 0

tile_size = 50

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN|pygame.SCALED)
pygame.display.set_caption('For The Potato')


bg_img = pygame.image.load(os.path.join("kepek", "hatter.png")).convert()
bg2_img = pygame.image.load(os.path.join("kepek", "hatter2.png")).convert()


bg_img = pygame.transform.scale(bg_img, (1000, 1000))
bg2_img = pygame.transform.scale(bg2_img, (1000, 1000))


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, level):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(os.path.join("kepek", "enemy.png"))
		self.image = pygame.transform.scale(img, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.speed = 1
		self.level = level

	def update(self):
		next_x = self.rect.x + self.move_direction * self.speed
		next_bottom = self.rect.bottom + 1
		ground_beneath_next = False
		self.rect.x += self.move_direction * self.speed

		for tile in worlds_list[self.level].tile_list:
				if tile[1].collidepoint(self.rect.right, self.rect.midright[1]) and tile[2] > 0:
					self.move_direction *= -1
				if tile[1].collidepoint(self.rect.left, self.rect.midleft[1]) and tile[2] > 0:
					self.move_direction *= -1
				if tile[1].colliderect(next_x + self.rect.width // 2, next_bottom, 1, 1):
					ground_beneath_next = True

		if not ground_beneath_next:
			self.move_direction *= -1

		


class Player():
	def __init__(self, level, completed, x, y):
		img = pygame.image.load(os.path.join("kepek", "trollface.jpg"))
		self.image = pygame.transform.scale(img, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.level = level - 1
		self.vel_y = 0
		self.jumped = False
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.checkpoint_x = self.rect.x
		self.checkpoint_y = self.rect.y
		self.died = False
		self.completed = completed

	def update(self):
		dx = 0
		dy = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			dx -= 5
		if key[pygame.K_RIGHT]:
			dx += 5
		if key[pygame.K_UP] and self.jumped == False:
			self.vel_y = -15
			self.jumped = True

		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y

		for tile in worlds_list[self.level].tile_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if key[pygame.K_UP] == False:
					self.jumped = False
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
				if tile[2] == 4:
					self.died = True
				if tile[2] == 3:
					self.checkpoint_x = tile[3]
					self.checkpoint_y = tile[4]
				if tile[2] == 5:
					return True
		
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0

		for enemy in worlds_list[self.level].world_enemy_group:
			if self.rect.colliderect(enemy.rect):
				if self.rect.bottom <= enemy.rect.top + 10:
					enemy.kill()  
					self.vel_y = -10 
				else: 
					self.died = True

		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0
			
		if self.died == False:
			self.rect.x += dx
			self.rect.y += dy
		
		else:
			self.rect.x = self.checkpoint_x
			self.rect.y = self.checkpoint_y
			self.died = False

		screen.blit(self.image, self.rect)


class World():
	def __init__(self, data, level, level_name):
		self.level = level - 1
		self.level_name = level_name
		self.tile_list = []
		self.world_enemy_group = pygame.sprite.Group()
		self.player_place = None
		

		dirt_img = pygame.image.load(os.path.join("kepek", "dirt.png"))
		grass_img = pygame.image.load(os.path.join("kepek","grass.png"))
		goal_img = pygame.image.load(os.path.join("kepek", "goal.png"))
		water_img = pygame.image.load(os.path.join("kepek", "water.png"))
		goal2_img = pygame.image.load(os.path.join("kepek", "goal2.png"))
		rock_img = pygame.image.load(os.path.join("kepek", "rock.png"))
		lava_img = pygame.image.load(os.path.join("kepek", "lava.png"))

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 1)
					self.tile_list.append(tile)

				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 2)
					self.tile_list.append(tile)
					
				if tile == 3:
					img = pygame.transform.scale(goal_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 3, img_rect.x, img_rect.y)
					self.tile_list.append(tile)

				if tile == 4:
					img = pygame.transform.scale(water_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 4)
					self.tile_list.append(tile)

				if tile == 5:
					img = pygame.transform.scale(goal2_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 5)
					self.tile_list.append(tile)

				if tile == 6:
					enemy = Enemy(col_count * tile_size, row_count * tile_size + 15, self.level)
					self.world_enemy_group.add(enemy)
				
				if tile == 7:
					img = pygame.transform.scale(rock_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 7)
					self.tile_list.append(tile)
				
				if tile == 8:
					img = pygame.transform.scale(lava_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, 4)
					self.tile_list.append(tile)
				
				if tile == "p":
					self.player_place = Player(level, False, col_count * tile_size, row_count * tile_size)

				col_count += 1
			row_count += 1

	def draw(self, pause, run):
		for tile in self.tile_list:
			if pause and not run:
				megallitva = Font_types.fonts["80"].render("Paused", False, BLACK)
				megallitva_place = (screen_width // 2 - 80, screen_height // 2)
				screen.blit(megallitva, megallitva_place)
				pygame.display.update()

			text = Font_types.fonts["50"].render(self.level_name, False, BLACK)
			text_place = text.get_rect()
			screen.blit(text, text_place)
			screen.blit(tile[0], tile[1])
	
	def get_player(self):
		return self.player_place



level = 5
world = World(worlds.world_data, 1, "Level: 1 - Tutorial")
world2 = World(worlds.world2_data, 2, "Level: 2")
world3 = World(worlds.world3_data, 3, "Level: 3")
world4 = World(worlds.world4_data, 4, "Level: 4")
world5 = World(worlds.world5_data, 5, "Level: 5")
worlds_list = [world, world2, world3, world4, world5]


completed = False
clock = pygame.time.Clock()
FPS = 60

pause = 0

while run and not pause:
	clock.tick(FPS)
	if level < 4:
		screen.blit(bg_img, (0, 0))
	elif level >= 4:
		screen.blit(bg2_img, (0, 0))

	worlds_list[level - 1].draw(pause, run)
	player = worlds_list[level - 1].get_player()
	completed = player.update()
	worlds_list[level - 1].world_enemy_group.update()
	worlds_list[level - 1].world_enemy_group.draw(screen)


	if completed == True:
		level += 1
		completed = False
		player = Player(level, completed, player.checkpoint_x, player.checkpoint_y)
		continue

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = 0

		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pause = 1
			run = 0

	while not run and pause:
		worlds_list[level - 1].draw(pause, run)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				pause = 0
				run = 1
			elif event.type == pygame.QUIT:
				pause = 0
				run = 0


	pygame.display.flip()

pygame.quit()
