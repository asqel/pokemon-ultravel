from random import randint
class Move:
	# precision : 0-100 (0 always fails, 100 never fails)
	def  __init__(self, pp : int, precision : int, damage : int, category : str, type1 : str, type2 : str = None) -> None:
		self.pp = pp
		self.precision = precision
		self.damage = damage
		self.category = category
		self.types = (type1, type2)

	def will_attack(self, user, player, target):
		return 1
	def on_attack(self, user, player, target):
		...
	def precision_succeed(self):
		return randint(0,100) <= self.precision
		