from pokemons import *
from pk_types import *
from random import uniform
from uti import *
import items

ROWLET_ID = 1
ROWLET_BASE_STAT = [68, 55, 55, 50, 50, 42]
ROWLET_BASE_XP = 64

class PK_Rowlet(Pokemon):
	def __init__(self, level : int, surname : str, gender : int, shiny : bool, item: items.Item):
		if gender == -1:
			gender = 0
			if uniform(0, 100) <= 12.5:
				gender = 1
		super().__init__(
			ROWLET_ID,
			surname,
			level,
			(PK_T_GRASS, None),
			random_nature(),
			ROWLET_BASE_STAT.copy(),
			gender,
			(Textures["pokemon"]["rowlet"], Textures["pokemon"]["rowlet_shiny"]),
			shiny,
			item,
			ROWLET_BASE_XP
			)
		

register_pokemon(ROWLET_ID, "Rowlet", PK_Rowlet)