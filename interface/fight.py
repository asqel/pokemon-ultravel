from pygame.event import Event
from interface import *
import pygame as py
from uti import *

class fight_gui(Gui):
	def __init__(self, player) -> None:
		super().__init__("fight_gui", None, player)
		self.main_cursor_x = 0
		self.main_cursor_y = 0

	def tick(self, events: list[py.event.Event]):
		for i in events:
			if i.type == py.KEYDOWN:
				if i.key == py.K_LEFT:
					self.main_cursor_x -= 1
					if self.main_cursor_x < 0:
						self.main_cursor_x = 1
				if i.key == py.K_RIGHT:
					self.main_cursor_x += 1
					if self.main_cursor_x > 1:
						self.main_cursor_x = 0
				if i.key == py.K_UP:
					self.main_cursor_y -= 1
					if self.main_cursor_y < 0:
						self.main_cursor_y = 1
				if i.key == py.K_DOWN:
					self.main_cursor_y += 1
					if self.main_cursor_y > 1:
						self.main_cursor_y = 0
	
	def draw(self, screen : py.Surface):
		screen.fill(0x00ff00)
		# draw pokemons
		pass
		# draw names
		screen.blit(Textures["pokemon"]["combat_names"], (0, 0))
		# draw 4 action
		texts = ["attaques", "objets", "pokemons", "fuite"]
		texts_idx = 0
		base_x = 600
		base_y = 400
		for i in range(2):
			for k in range(2):
				col = (0, 0, 0)
				if k == self.main_cursor_x and i == self.main_cursor_y:
					col = (106, 181, 91)
				text = main_font.render(texts[texts_idx], 0, col)
				screen.blit(text, (base_x + k*165, base_y + i*80))
				texts_idx += 1

registerGui(fight_gui)