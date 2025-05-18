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
	"en" : {
		0: "For The Potato!",
		1: "New game",
		2: "Continue game",
		3: "Game language: English",
		4: [ 
			"Music: On",
	  		"Music: Off"
		],
		5: "Save and quit game",
		6: "There is no saves!",
		"in game":{
			0: "Level",
			1: "Paused",
			2: "Open menu and pause the game: ESC",
			3: "To continue again: ESC"
		}
	},

	"hu" :{
		0: "A burgonyáért!",
		1: "Új játék",
		2: "Játék folytatása",
		3: "Játék nyelve: Magyar",
		4: [
			"Zene: Be",
	  		"Zene: Ki"
		],
		5: "Mentés és kilépés a játékból",
		6: "Nincsenek mentések!",
		"in game":{
			0: "Szint",
			1: "Megállítva",
			2: "Menü megnyitása és játék megállítása: ESC",
			3: "Folytatáshoz újra: ESC"
		}
	}
}

class Selected_fonts:
	def __init__(self):
		self.font_size30 = pygame.font.Font(None, 30)
		self.font_size50 = pygame.font.Font(None, 50)
		self.font_size80 = pygame.font.Font(None, 80)
		self.font_size100 = pygame.font.Font(None, 100)
		

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)