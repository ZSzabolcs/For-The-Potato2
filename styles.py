import pygame

def set_language():
	try:
		with open("saves.csv", "r") as file:
			sor = file.readline().split(" ")
			text = str(sor[2])
			language = text
			if language == "en" or language == "hu":
				return language

	except IndexError:
		language = "en"
		return language
	
	except FileNotFoundError:
		print("Nem létezik a fájl!")

languages = {
	"en" : [
		"For The Potato!",
		"New game",
		"Continue game",
		"Game language: English",
		"Quit game",
		"There is no saves!",
		[
			"Level",
			"Paused"
		]
	],

	"hu" :[
		"A burgonyáért!",
		"Új játék",
		"Játék folytatása",
		"Játék nyelve: Magyar",
		"Kilépés a játékból",
		"Nincsenek mentések!",
		[
			"Szint",
			"Megállítva"
		]
	]
}

class Selected_fonts:
	def __init__(self):
		self.font_size50 = pygame.font.Font(None, 50)
		self.font_size80 = pygame.font.Font(None, 80)
		self.font_size100 = pygame.font.Font(None, 100)
		

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)