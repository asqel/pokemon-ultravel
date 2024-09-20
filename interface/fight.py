from pygame.event import Event
from interface import *
import pygame as py
from uti import *
import entities as en
import pokemons as PK
import items
from langs import *
import key_map as km

class fight_gui(Gui):
	def __init__(self, player) -> None:
		super().__init__("fight_gui", None, player)
		self.main_cursor_x = 0
		self.main_cursor_y = 0
		self.enemy : list[PK.Pokemon] = None
		self.player_pk_idx = 0
		self.enemy_pk_idx = 0
		self.player_pk_sprite_resize = None
		self.player_pk_sprite = None
		self.player_pk_transparency = 255.0
		self.black_fade = 255
		# 0 : choose action, 1: choose attack, 2: choose item, 3: choose pokemon
		self.state = 0

	def tick(self, events: list[py.event.Event]):
		keys = km.get_pressed(events)
		if self.state == 0:
			if keys[km.t_mov_up] == 1:
				self.main_cursor_y -= 1
			if keys[km.t_mov_down] == 1:
				self.main_cursor_y += 1
			if keys[km.t_mov_left] == 1:
				self.main_cursor_x -= 1
			if keys[km.t_mov_right] == 1:
				self.main_cursor_x += 1
			self.main_cursor_x = max(0, min(self.main_cursor_x, 1))
			self.main_cursor_y = max(0, min(self.main_cursor_y, 1))

	def draw_button(self, screen : py.Surface):
		texts = ["attaques", "objets", "pokemons", "fuite"]
		texts_idx = 0
		base_x = 600
		base_y = 400
		for i in range(2):
			for k in range(2):
				if k == self.main_cursor_x and i == self.main_cursor_y:
					col = (106, 181, 91)
					text = main_font_30.render(texts[texts_idx], 0, col)
					screen.blit(
						main_font_30.render(">", 0, col),
						((base_x + k*165 - 20, base_y + i*80))
					)
				else:
					col = (0, 0, 0)
					text = main_font_30.render(texts[texts_idx], 0, col)
				screen.blit(text, (base_x + k*165, base_y + i*80))
				texts_idx += 1
	def draw(self, screen : py.Surface):
		screen.fill(0x00ff00)
		# draw pokemons
		pass
		# draw names
		screen.blit(Textures["pokemon"]["fight_layout"], (0, 0))

		if self.state == 0:
			self.draw_button(screen)
		if self.black_fade > 0:
			s = py.Surface((screen.get_width(), screen.get_height()), py.SRCALPHA).convert_alpha()
			s.fill((0, 0, 0))
			s.set_alpha(self.black_fade)
			screen.blit(s, (0, 0))
			self.black_fade -= 3
		else:
			self.draw_player_pokemon()
	
	def draw_player_pokemon(self):
		pk : PK.Pokemon = self.player.team[self.player_pk_idx]
		if pk.surname == "":
			screen.blit(main_font_30.render(get_text(self.player.lang, "pokemon", PK.Pokemons_id[pk.pk_id][0]), 0, 0x0), (680, 275))
		else:
			screen.blit(main_font_30.render(pk.surname, 0, 0x0), (680, 275))
		screen.blit(main_font_30.render(f"Lv. {pk.level: 4}", 0, 0x0), (890, 275))
		screen.blit(main_font_30.render(f"{pk.hp: 4}/{pk.get_max_hp(): 4}", 0, 0x0), (700, 320))
		if self.player_pk_transparency > 0:
			s = py.transform.flip(pk.get_sprite().copy(), 1, 0)
			s.fill((int(self.player_pk_transparency), int(self.player_pk_transparency), int(self.player_pk_transparency)), special_flags = py.BLEND_RGB_ADD)
			screen.blit(s, (70, 160))
			self.player_pk_transparency -= 8
		else:
			screen.blit(py.transform.flip(pk.get_sprite(), 1, 0), (70, 160))

registerGui(fight_gui)

def new_fight(player : 'en.Character', enemy : list[PK.Pokemon]):
	gui = fight_gui(player)
	player.team[0] = PK.Pokemons_id[1][1](23, "br1 dit booh!", 1, PK.random_is_shiny(), items.items["Air"](1))
	gui.player = player
	gui.enemy = enemy
	player.guis.append(gui)
