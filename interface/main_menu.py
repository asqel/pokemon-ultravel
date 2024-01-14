import pygame as py
from interface import *
from uti import *
from random import randint, choice
from math import cos, sin

class Main_menu(Gui):
	def __init__(self, player) -> None:

		super().__init__("Main_menu", {}, player)
		
	def tick(self, events: list[py.event.Event]):
		for i in events:
			if i.type == py.KEYDOWN:
				self.player.close_gui()
				self.player.open_gui("Choose_name")
			
	def draw(self, screen : py.Surface):
		screen.fill((0,0,0))
		
		text = main_font_40.render("Pokémon ultravel", 0, (116, 44, 156))
		screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 50))

		text = main_font.render("Press any key to start", 0, (116, 44, 156))
		screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 300))
registerGui(Main_menu)
