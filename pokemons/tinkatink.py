from pk_types import *
from random import getrandbits
from pokemons import *



TINKATINK_BASE_STAT = [50, 45, 45, 35, 64, 58]
TINKATINK_ID = 58

class PK_Tinkatink(Pokemon):
	def __init__(self, level : int, surname : str, gender : int) -> None:
		super().__init__(
			TINKATINK_ID,
			surname,
			level,
			(PK_T_FAIRY, PK_T_STELL),
			"NATURE",
			TINKATINK_BASE_STAT.copy(),
			1
		)