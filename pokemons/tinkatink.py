from pk_types import get_type_mult3
from random import getrandbits

STAT_t = tuple[float, float, float, float, float, float]


def get_nature_mult(nature : str, stat : int):
	if stat not in range(6):
		return 1
	stat_name = ["HP", "SPEED", "AT", "DEF", "AT_SPE", "DEF_SPE"][stat]
	return 1


def gen_IV():
	n1 = getrandbits(16)
	n2 = getrandbits(16)
	HP = n1 & 31
	ATT = (n1>>5) & 31
	DEF = (n1>>10) & 31
	DEF_SPE = n2 & 31
	ATT_SPE = (n2>>5) & 31
	SPEED = (n2>>10) & 31
	return (HP, SPEED, ATT, DEF, ATT_SPE, DEF_SPE) 
TINKATINK_BASE_STAT = (50, 45, 45, 35, 64, 58)

class PK_tinkatink:
	def __init__(self) -> None:
		self.level = 1
		self.attacks = []
		# [HP, SPEED, AT, DEF, AT_SPE, DEF_SPE]
		self.nature = ""
		self.base_stats : STAT_t= TINKATINK_BASE_STAT
		self.iv = gen_IV()
		self.ev = [0,0,0,0,0,0]
		self.hp = self.get_max_hp()
		self.will_evolve = 0
		self.will_receive_EV = 0
		print(self.__get_STAT_X.__name__)

	def __get_STAT_X(self, stat : int):
		return int((int(((2 * self.base_stats[stat] + self.iv[stat] + int(self.ev[stat]/4)) * self.level) / 100) + 5) * get_nature_mult(self.nature, stat))
			
	def get_max_hp(self):
		return int(((2*self.base_stats[0]+self.iv[0]+int(self.ev[0]/4))*self.level)/100) + self.level + 10
	def get_attack(self):
		return self.__get_STAT_X(2)
	def get_defense(self):
		return self.__get_STAT_X(3)
	def get_attack_spe(self):
		return self.__get_STAT_X(4)
	def get_defense_spe(self):
		return self.__get_STAT_X(5)
	def get_speed(self):
		return self.__get_STAT_X(1)
	def get_evolution(self, player):
		...
	def on_evolve(self, player):
		...
	#self.level will be  the new level
	def on_level(self, player):...


class AT_tackle:
	def __init__(self) -> None:
		self.pp = 35
		self.precision = 100
		self.base_damage = 40
		self.category = "physic"
		self.types = ["normal", None]

	def get_damage(self, player, user, defendant):
		return get_type_mult3('normal', defendant.types[0], defendant.types[1])



def check_EV(EV : STAT_t):
	is_ok = True
	for i in range(6):
		if EV[i] > 252:
			is_ok = False
	return sum(EV) <= 510 and is_ok
