from pk_types import get_type_mult3


class PK_tinkatink:
	def __init__(self) -> None:
		self.level = 0
		self.attacks = []

class AT_tackle:
	def __init__(self) -> None:
		self.pp = 35
		self.precision = 100
		self.base_damage = 40
		self.category = "physic"
		self.types = ["normal", None]

	def get_damage(self, user, defendant):
		return get_type_mult3('normal', defendant.types[0], defendant.types[1])




