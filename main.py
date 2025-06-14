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
from styles import WHITE
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
		ground_beneath_next = 0
		self.rect.x += self.move_direction * self.speed

		for tile in worlds_list[self.level].tile_list:
				if tile[1].collidepoint(self.rect.right, self.rect.midright[1]) and tile[2] > 0:
					self.move_direction *= -1
				if tile[1].collidepoint(self.rect.left, self.rect.midleft[1]) and tile[2] > 0:
					self.move_direction *= -1
				if tile[1].colliderect(next_x + self.rect.width // 2, next_bottom, 1, 1):
					ground_beneath_next = 1

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
		self.jumped = 0
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.checkpoint_x = self.rect.x
		self.checkpoint_y = self.rect.y
		self.died = 0
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
		if key[pygame.K_UP] and self.jumped == 0:
			self.vel_y = -15
			self.jumped = 1

		self.vel_y += 1
		if self.vel_y > 10:
			self.vel_y = 10
		dy += self.vel_y

		for tile in worlds_list[self.level].tile_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if key[pygame.K_UP] == 0:
					self.jumped = 0
				if self.vel_y < 0:
					dy = tile[1].bottom - self.rect.top
					self.vel_y = 0
				elif self.vel_y >= 0:
					dy = tile[1].top - self.rect.bottom
					self.vel_y = 0
				if tile[2] == 4:
					self.died = 1
				if tile[2] == 3:
					self.checkpoint_x = tile[1].x
					self.checkpoint_y = tile[1].y
				if tile[2] == 5:
					return 1
		
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0

		for enemy in worlds_list[self.level].world_enemy_group:
			if self.rect.colliderect(enemy.rect):
				if self.rect.bottom <= enemy.rect.top + 10:
					enemy.kill()  
					self.vel_y = -10 
				else: 
					self.died = 1

		for block in worlds_list[self.level].blocks:
			if block.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				if key[pygame.K_UP] == 0:
					self.jumped = 0
				if self.vel_y < 0 and block.visible:
					dy = block.rect.bottom - self.rect.top
					self.vel_y = 0					
				elif self.vel_y >= 0 and block.visible:
					dy = block.rect.top - self.rect.bottom
					self.vel_y = 0


		for fireball in worlds_list[self.level].fireballs_group:
			if self.rect.colliderect(fireball.rect):
				self.died = 1

		if self.rect.bottom > screen_height:
			self.rect.bottom = screen_height
			dy = 0
			
		if self.died == 0:
			self.rect.x += dx
			self.rect.y += dy
		
		else:
			self.rect.x = self.checkpoint_x
			self.rect.y = self.checkpoint_y
			self.died = 0

		screen.blit(self.image, self.rect)




class World():
	def __init__(self, data, level, level_name):
		self.world_map = data
		self.level = level - 1
		self.level_name = level_name
		self.tile_list = []
		self.world_enemy_group = pygame.sprite.Group()
		self.fireballs_group = pygame.sprite.Group()
		self.stalactite_group = pygame.sprite.Group()
		self.player_place = None
		self.blocks = []
		

		dirt_img = pygame.image.load(os.path.join("kepek", "dirt.png"))
		grass_img = pygame.image.load(os.path.join("kepek","grass.png"))
		goal_img = pygame.image.load(os.path.join("kepek", "goal.png"))
		water_img = pygame.image.load(os.path.join("kepek", "water.png"))
		water2_img = pygame.image.load(os.path.join("kepek", "water2.png"))
		goal2_img = pygame.image.load(os.path.join("kepek", "goal2.png"))
		rock_img = pygame.image.load(os.path.join("kepek", "rock.png"))
		lava_img = pygame.image.load(os.path.join("kepek", "lava.png"))
		snow_img = pygame.image.load(os.path.join("kepek", "snow.png"))
		snow2_img = pygame.image.load(os.path.join("kepek", "snow2.png"))
		ice_img = pygame.image.load(os.path.join("kepek", "ice.png"))

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
					tile = make_tile(goal_img, tile_size, col_count, row_count, 3)
					self.tile_list.append(tile)

				if tile == 4:
					tile = make_tile(water_img, tile_size, col_count, row_count, 4)
					self.tile_list.append(tile)

				if tile == 5:
					tile = make_tile(goal2_img, tile_size, col_count, row_count, 5)
					self.tile_list.append(tile)

				if tile == 6:
					enemy = Enemy(col_count * tile_size, row_count * tile_size + 15, self.level)
					self.world_enemy_group.add(enemy)
				
				if tile == 7:
					tile = make_tile(rock_img, tile_size, col_count, row_count, 7)
					self.tile_list.append(tile)
				
				if tile == 8:
					tile = make_tile(lava_img, tile_size, col_count, row_count, 4)
					self.tile_list.append(tile)

				if tile == 9:
					tile = make_tile(snow2_img, tile_size, col_count, row_count, 9)
					self.tile_list.append(tile)
				
				if tile == 10:
					tile = make_tile(snow_img, tile_size, col_count, row_count, 10)
					self.tile_list.append(tile)

				if tile == 11:
					tile = make_tile(water2_img, tile_size, col_count, row_count, 4)
					self.tile_list.append(tile)

				if tile == 12:
					tile = make_tile(ice_img, tile_size, col_count, row_count, 12)
					self.tile_list.append(tile)

				if tile == "b1":
					block = make_block(rock_img, col_count, row_count, 2)
					self.blocks.append(block)

				if tile == "b2":
					block = make_block(grass_img, col_count, row_count, 3)
					self.blocks.append(block)

				if tile == "b3":
					block = make_block(snow_img, col_count, row_count, 2)
					self.blocks.append(block)

				if tile == "b4":
					block = make_block(snow_img, col_count, row_count, 2)
					self.blocks.append(block)

				if tile == "p":
					self.player_place = Player(level, 0, col_count * tile_size, row_count * tile_size)

				if tile == "fb":
					fireball = Fireball(col_count * tile_size, row_count * tile_size)
					tile = make_tile(lava_img, tile_size, col_count, row_count, 4)
					self.fireballs_group.add(fireball)
					self.tile_list.append(tile)
				
				if tile == "st":
					
					tile = make_tile(rock_img, tile_size, col_count, row_count, 7)
					stalactite = Stalactite(col_count * tile_size, row_count * tile_size, tile)
					self.stalactite_group.add(stalactite)
					self.tile_list.append(tile)

				col_count += 1
			row_count += 1



	def draw(self, pause, run, lang, ch_lang, mouse = None):

		def draw_left_top_texts():
			if self.level < 5:
				chosen_color = BLACK
			else:
				chosen_color = WHITE

			level_text = fonts.font_size50.render(self.level_name, 0, chosen_color)
			escape_text = fonts.font_size30.render(lang[ch_lang]["in game"][2], 0, chosen_color)
			level_text_place = level_text.get_rect()
			escape_text_place = (0, 35)
			screen.blit(level_text, level_text_place)
			screen.blit(escape_text, escape_text_place)

		for tile in self.tile_list:
			if pause and not run:
				explainer_text = fonts.font_size50.render(lang[ch_lang]["in game"][3], 0, BLACK)
				explainer_text_place = (screen_width*0.4 - 10, screen_height/2 + 100)	

				if ch_lang == "en":
					quit_game_text_place = ((in_game_menu_rects[0].center[0])-(in_game_menu_rects[0].center[0]*0.30), in_game_menu_rects[0].center[1]-15)
					explainer_text_place = (screen_width*0.4 - 60, screen_height/2 + 100)
				else:
					quit_game_text_place = ((in_game_menu_rects[0].center[0])-(in_game_menu_rects[0].center[0]*0.45), in_game_menu_rects[0].center[1]-15)
					explainer_text_place = (screen_width*0.4 - 60, screen_height/2 + 100)
				for rect in in_game_menu_rects:
					square = pygame.draw.rect(screen, BLACK, rect)
					if square.collidepoint(float(mouse[0]), float(mouse[1])) and mouse is not None:
						square = pygame.draw.rect(screen, BLUE, rect)
				quit_game_text = fonts.font_size50.render(lang[ch_lang][5], 0, RED)
				screen.blit(quit_game_text, quit_game_text_place)
				screen.blit(explainer_text, explainer_text_place)
				draw_left_top_texts()
				pygame.display.update()

			draw_left_top_texts()
			screen.blit(tile[0], tile[1])
			
	def draw_broken_blocks(self):
		for bloc in self.blocks:
			bloc.update()
			bloc.draw(screen)

	def get_player(self):
		return self.player_place




class Fireball(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(os.path.join("kepek", "tuzgolyo.png"))
		self.image = pygame.transform.scale(image, (25, 25))
		self.rect = self.image.get_rect()
		self.rect.x = x + 15
		self.rect.y = y
		self.start_x = x
		self.start_y = y
		self.initial_y = y
		self.vertical_velocity = -4

	def update(self):
		self.rect.y += self.vertical_velocity
		distance_revealed = abs(self.initial_y - self.rect.y)

		if self.vertical_velocity < 0:
			if distance_revealed >= 200:
				self.vertical_velocity *= -1
		elif self.vertical_velocity > 0:
			if self.rect.y >= self.initial_y:
				self.vertical_velocity = -4
				self.rect.y = self.initial_y
		



class Stalactite(pygame.sprite.Sprite):
	def __init__(self, x, y, tile):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(os.path.join("kepek", "tuzgolyo.png"))
		self.image = pygame.transform.scale(image, (25, 25))
		self.rect = self.image.get_rect()
		self.rect.x = x + 15
		self.rect.y = y + 30
		self.start_x = x
		self.start_y = y
		self.initial_y = y
		self.starting_tile = tile[1]
		self.fall = 0
		self.vertical_velocity = 7

	def update(self, player : Player, tile_list : list):
		if player.rect.y - 250 <= self.rect.y and player.rect.x + 15 >= self.rect.x:
			self.fall = 1

		if self.fall:
			self.rect.y += self.vertical_velocity
			for tile in tile_list:
				if self.rect.colliderect(tile[1]) and not self.rect.colliderect(self.starting_tile):
					self.kill()

		if self.rect.colliderect(player):
			player.died = 1





class Block(pygame.sprite.Sprite):
	def __init__(self, x, y, image, second):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.visible = 1
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



def make_block(image, col_count, row_count, seconds):
	img = pygame.transform.scale(image, (tile_size, tile_size))
	img_rect = img.get_rect()
	img_rect.x = col_count * tile_size
	img_rect.y = row_count * tile_size
	block = Block(img_rect.x, img_rect.y, img, seconds)
	return block


def make_tile(image, tile_size, col_count, row_count, number):
	img = pygame.transform.scale(image, (tile_size, tile_size))
	img_rect = img.get_rect()
	img_rect.x = col_count * tile_size
	img_rect.y = row_count * tile_size
	tile = (img, img_rect, number)
	return tile


def saving_game(points, level, chosen_lang):
	with open("saves.csv", "w") as file:
		file.write(f"{str(points)} {str(level)} {chosen_lang}")
		file.close()

		
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


		
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(languages[choosen_language][0])
tile_size = 50
bg_img = pygame.image.load(os.path.join("kepek", "hatter.png")).convert()
bg_img = pygame.transform.scale(bg_img, (1000, 1000))
bg2_img = pygame.image.load(os.path.join("kepek", "hatter2.png")).convert()
bg2_img = pygame.transform.scale(bg2_img, (1000, 1000))
bg3_img = pygame.image.load(os.path.join("kepek", "hatter3.png")).convert()
bg3_img = pygame.transform.scale(bg3_img, (1000, 1000))
bg4_img = pygame.image.load(os.path.join("kepek", "hatter4.png")).convert()
bg4_img = pygame.transform.scale(bg4_img, (1000, 1000))

level_name = languages[choosen_language]["in game"][0]

world = World(worlds.world_data, 1, f"{level_name}: 1")
world2 = World(worlds.world2_data, 2, f"{level_name}: 2")
world3 = World(worlds.world3_data, 3, f"{level_name}: 3")
world4 = World(worlds.world4_data, 4, f"{level_name}: 4")
world5 = World(worlds.world5_data, 5, f"{level_name}: 5")
world6 = World(worlds.world6_data, 6, f"{level_name}: 6")
world7 = World(worlds.world7_data, 7, f"{level_name}: 7")
world8 = World(worlds.world8_data, 8, f"{level_name}: 8")
world9 = World(worlds.world9_data, 9, f"{level_name}: 9")
world10 = World(worlds.world10_data, 10, f"{level_name}: 10")
worlds_list = [world, world2, world3, world4, world5, world6, world7, world8, world9, world10]

in_game_menu_rects = [
	pygame.rect.Rect(screen_width*0.27, screen_height/2-50, screen_width*0.5, screen_width*0.1)
]

async def main(level):
	run = 1
	completed = 0
	clock = pygame.time.Clock()
	FPS = 60
	pause = 0
	while run and not pause:
		current_world = worlds_list[level - 1]
		clock.tick(FPS)
		if level < 4:
			screen.blit(bg_img, (0, 0))
		elif level >= 4 and level <= 5:
			screen.blit(bg2_img, (0, 0))
		elif level >= 6 and level <= 8:
			screen.blit(bg3_img, (0, 0))
		elif level >= 9:
			screen.blit(bg4_img, (0, 0))

		current_world.draw(pause, run, languages, choosen_language)
		current_world.draw_broken_blocks()
		player = current_world.get_player()
		current_world.world_enemy_group.update()
		current_world.world_enemy_group.draw(screen)
		current_world.fireballs_group.update()
		current_world.fireballs_group.draw(screen)
		current_world.stalactite_group.draw(screen)
		current_world.stalactite_group.update(player, current_world.tile_list)
		completed = player.update()


		if completed == 1:
			level += 1
			completed = 0
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

	if not run and not pause:
		with open("saves.csv", "w") as file:
			file.write(f"{points} {level} {choosen_language}")
			file.close()
		pygame.quit()

asyncio.run(main(level))
