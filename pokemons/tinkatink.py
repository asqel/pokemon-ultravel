from pk_types import *
from random import getrandbits
from pokemons import *
from uti import *


TINKATINK_BASE_STAT = [50, 45, 45, 35, 64, 58]
TINKATINK_ID = 58
TINKATINK_SPR_N = Textures["pokemon"]["golemastoc"]
TINKATINK_SPR_S  = Textures["pokemon"]["golemastoc_shiny"]

class PK_Tinkatink(Pokemon):
	def __init__(self, level : int, surname : str, gender : int, shiny : bool) -> None:
		super().__init__(
			TINKATINK_ID,
			surname,
			level,
			(PK_T_FAIRY, PK_T_STELL),
			"NATURE",
			TINKATINK_BASE_STAT.copy(),
			1,
			(TINKATINK_SPR_N, TINKATINK_SPR_S),
			shiny
		)