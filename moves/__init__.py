class Move:
	# precision : 0-100
	def  __init__(self, pp : int, precision : int, damage : int, category : str, type1 : str, type2 : str = None) -> None:
		self.pp = pp
		self.precision = precision
		self.damage = damage
		self.category = category
		self.types = (type1, type2)
		