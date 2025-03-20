import pygame
from pygame.locals import *
import os
import worlds
import asyncio
import time
from menu import menu_page
from styles import BLACK
from styles import RED
from styles import BLUE
from styles import set_language
from styles import languages
from styles import Selected_fonts

class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y, level):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load(os.path.join("kepek", "enemy.png")).convert()
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
		self.level = level - 1
		self.rect.x = x
		self.rect.y = y
		self.vel_y = 0
		self.jumped = False
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.checkpoint_x = self.rect.x
		self.checkpoint_y = self.rect.y
		self.died = False
		self.completed = completed
		self.player_place = None

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
					self.checkpoint_x = tile[1].x
					self.checkpoint_y = tile[1].y
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

		for block in worlds_list[self.level].blocks:
			if block.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if key[pygame.K_UP] == False:
					self.jumped = False
				if self.vel_y < 0 and block.visible:
					dy = block.rect.bottom - self.rect.top
					self.vel_y = 0					
				elif self.vel_y >= 0 and block.visible:
					dy = block.rect.top - self.rect.bottom
					self.vel_y = 0

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
		self.world_map = data
		self.level = level - 1
		self.level_name = level_name
		self.tile_list = []
		self.world_enemy_group = pygame.sprite.Group()
		self.player_place = None
		self.blocks = []
		

		dirt_img = pygame.image.load(os.path.join("kepek", "dirt.png"))
		grass_img = pygame.image.load(os.path.join("kepek","grass.png"))
		goal_img = pygame.image.load(os.path.join("kepek", "goal.png"))
		water_img = pygame.image.load(os.path.join("kepek", "water.png"))
		goal2_img = pygame.image.load(os.path.join("kepek", "goal2.png"))
		rock_img = pygame.image.load(os.path.join("kepek", "rock.png"))
		lava_img = pygame.image.load(os.path.join("kepek", "lava.png"))

		row_count = 0
		for row in self.world_map:
			col_count = 0
			for tile in row:
				if tile == 1:
					tile = make_tile(dirt_img, tile_size, col_count, row_count, 1)
					self.tile_list.append(tile)

				if tile == 2:
					tile = make_tile(grass_img, tile_size, col_count, row_count, 2)
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

				if tile == "b1":
					image = pygame.transform.scale(rock_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					block = Block(img_rect.x, img_rect.y, image, 2)
					self.blocks.append(block)

				if tile == "b2":
					image = pygame.transform.scale(rock_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					block = Block(img_rect.x, img_rect.y, image, 3)
					self.blocks.append(block)

				if tile == "p":
					self.player_place = Player(level, False, col_count * tile_size, row_count * tile_size)

				col_count += 1
			row_count += 1


	def draw(self, pause, run, lang, ch_lang, mouse = None, ):
		for tile in self.tile_list:
			if pause and not run:
				megallitva = fonts.font_size80.render(lang[ch_lang]["in game"][1], False, BLACK)
				if ch_lang == "en":
					megallitva_place = (screen_width // 2 - 80, screen_height // 2 - 200)
					quit_game_text_place = ((in_game_menu_rects[0].center[0])-(in_game_menu_rects[0].center[0]*0.17), in_game_menu_rects[0].center[1]-15)
				else:
					megallitva_place = (screen_width // 2 - 130, screen_height // 2 - 200)
					quit_game_text_place = ((in_game_menu_rects[0].center[0])-(in_game_menu_rects[0].center[0]*0.27), in_game_menu_rects[0].center[1]-15)
				for rect in in_game_menu_rects:
					square = pygame.draw.rect(screen, BLACK, rect)
					if square.collidepoint(float(mouse[0]), float(mouse[1])) and mouse is not None:
						square = pygame.draw.rect(screen, BLUE, rect)
				quit_game_text = fonts.font_size50.render(lang[ch_lang][4], 0, RED)
				screen.blit(megallitva, megallitva_place)
				screen.blit(quit_game_text, quit_game_text_place)
				pygame.display.update()

			text = fonts.font_size50.render(self.level_name, False, BLACK)
			text_place = text.get_rect()
			screen.blit(text, text_place)
			screen.blit(tile[0], tile[1])
			
	def draw_broken_blocks(self):
		for bloc in self.blocks:
			bloc.update()
			bloc.draw(screen)

	def get_player(self):
		return self.player_place


def make_tile(image, tile_size, column, row, number):
	img = pygame.transform.scale(image, (tile_size, tile_size))
	img_rect = img.get_rect()
	img_rect.x = column * tile_size
	img_rect.y = row * tile_size
	tile = (img, img_rect, number)
	return tile


def saving_game(points, level, choosen_lang):
	with open("saves.csv", "w") as file:
		file.write(f"{str(points)} {str(level)} {choosen_lang}")
		file.close()


class Block(pygame.sprite.Sprite):
	def __init__(self, x, y, image, second):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.visible = True
		self.last_toggle_time = time.time()
		self.sec = second

	def update(self):
		current_time = time.time()
		if current_time - self.last_toggle_time > self.sec:
			self.visible = not self.visible
			self.last_toggle_time = current_time

	def draw(self, surface):
		if self.visible:
			surface.blit(self.image, self.rect)




pygame.init()

fonts = Selected_fonts()

screen_width = 1000
screen_height = 1000

choosen_language = set_language()

datas = menu_page(screen_height, screen_height, fonts, choosen_language, languages)

points = datas[0]
level = datas[1]
choosen_language = datas[2]
music_is_on = datas[3]

if music_is_on:
	background_music = pygame.mixer.Sound("Jazz In Paris  Media Right Productions (No Copyright Music).mp3")
	background_music.set_volume(0.6)
	background_music.play(-1)



run = 1
		
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(languages[choosen_language][0])
tile_size = 50
bg_img = pygame.image.load(os.path.join("kepek", "hatter.png")).convert()
bg2_img = pygame.image.load(os.path.join("kepek", "hatter2.png")).convert()
bg2_img = pygame.transform.scale(bg2_img, (1000, 1000))
bg3_img = pygame.image.load(os.path.join("kepek", "hatter3.png")).convert()
bg3_img = pygame.transform.scale(bg3_img, (1000, 1000))

level_name = languages[choosen_language]["in game"][0]

world = World(worlds.world_data, 1, f"{level_name}: 1")
world2 = World(worlds.world2_data, 2, f"{level_name}: 2")
world3 = World(worlds.world3_data, 3, f"{level_name}: 3")
world4 = World(worlds.world4_data, 4, f"{level_name}: 4")
world5 = World(worlds.world5_data, 5, f"{level_name}: 5")
world6 = World(worlds.world6_data, 6, f"{level_name}: 6")
world7 = World(worlds.world7_data, 7, f"{level_name}: 7")
worlds_list = [world, world2, world3, world4, world5, world6, world7]

in_game_menu_rects = [
	pygame.rect.Rect(screen_width*0.27, screen_height/2, screen_width*0.5, screen_width*0.1)
]

completed = False
clock = pygame.time.Clock()
FPS = 60
pause = 0

current_world = worlds_list[level - 1]


async def main(run, pause, completed, clock, level):
	while run and not pause:
		clock.tick(FPS)
		if level < 4:
			screen.blit(bg_img, (0, 0))
		elif level >= 4 and level <= 5:
			screen.blit(bg2_img, (0, 0))
		elif level >= 6:
			screen.blit(bg3_img, (0, 0))


		current_world.draw(pause, run, languages, choosen_language)
		current_world.draw_broken_blocks()
		player = current_world.get_player()
		current_world.world_enemy_group.update()
		current_world.world_enemy_group.draw(screen)
		completed = player.update()


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
			mouse = pygame.mouse.get_pos()
			current_world.draw(pause, run, languages, choosen_language, mouse)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					pause = 0
					run = 1
				elif event.type == pygame.QUIT:
					pause = 0
					run = 0
				elif event.type == pygame.MOUSEBUTTONDOWN:
					for rect in in_game_menu_rects:
						if rect.collidepoint(float(mouse[0]), float(mouse[1])):
							if in_game_menu_rects.index(rect) == 0:
								pause, run = 0, 0
								saving_game(points, level, choosen_language)



		pygame.display.flip()
		await asyncio.sleep(0)

	pygame.quit()

asyncio.run(main(run, pause, completed, clock, level))
