PK_T_NORMAL = "normal"
PK_T_FIRE = "fire"
PK_T_WATER = "water"
PK_T_ELECTRIC = "electric"
PK_T_GRASS = "grass"
PK_T_ICE = "ice"
PK_T_FIGHTING = "fighting"
PK_T_POISON = "poison"
PK_T_GROUND = "ground"
PK_T_FLYING = "flying"
PK_T_PSYCHIC = "psychic"
PK_T_BUG = "bug"
PK_T_ROCK = "rock"
PK_T_GHOST = "ghost"
PK_T_DRAGON = "dragon"
PK_T_DARK = "dark"
PK_T_STELL = "steel"
PK_T_FAIRY = "fairy"
PK_T_LIGHT = "light"
PK_T_SUGAR = "sugar"
PK_T_PLASTIC = "plastic"

TYPE_TABLE : dict[str, dict[str, int | float]] = {
	"normal": {
		"normal": 1,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 1,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 1,
		"rock": 0.5,
		"ghost": 0,
		"dragon": 1,
		"dark": 1,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 0,
		"sugar" : 0.5,
		"plastic" : 2
	},
	"fire": {
		"normal": 1,
		"fire": 0.5,
		"water": 0.5,
		"electric": 1,
		"grass": 2,
		"ice": 2,
		"fighting": 1,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 2,
		"rock": 0.5,
		"ghost": 1,
		"dragon": 0.5,
		"dark": 1,
		"steel": 2,
		"fairy" : 1,
		"light" : 0,
		"sugar" : 2,
		"plastic" : 2
	},
	"water": {
		"normal": 1,
		"fire": 2,
		"water": 0.5,
		"electric": 1,
		"grass": 0.5,
		"ice": 1,
		"fighting": 1,
		"poison": 1,
		"ground": 2,
		"flying": 1,
		"psychic": 1,
		"bug": 1,
		"rock": 2,
		"ghost": 1,
		"dragon": 0.5,
		"dark": 1,
		"steel": 1,
		"fairy" : 1,
		"light" : 1,
		"sugar" : 0.5,
		"plastic" : 0.5
	},
	"electric": {
		"normal": 1,
		"fire": 1,
		"water": 2,
		"electric": 0.5,
		"grass": 0.5,
		"ice": 1,
		"fighting": 1,
		"poison": 1,
		"ground": 0,
		"flying": 2,
		"psychic": 1,
		"bug": 1,
		"rock": 1,
		"ghost": 1,
		"dragon": 0.5,
		"dark": 1,
		"steel": 1,
		"fairy" : 1,
		"light" : 1,
		"sugar" : 1,
		"plastic" : 0
	},
	"grass": {
		"normal": 1,
		"fire": 0.5,
		"water": 2,
		"electric": 1,
		"grass": 0.5,
		"ice": 1,
		"fighting": 1,
		"poison": 0.5,
		"ground": 2,
		"flying": 0.5,
		"psychic": 1,
		"bug": 0.5,
		"rock": 2,
		"ghost": 1,
		"dragon": 0.5,
		"dark": 1,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 2,
		"sugar" : 1,
		"plastic" : 0.5
	},
	"ice": {
		"normal": 1,
		"fire": 0.5,
		"water": 0.5,
		"electric": 1,
		"grass": 2,
		"ice": 0.5,
		"fighting": 1,
		"poison": 1,
		"ground": 2,
		"flying": 2,
		"psychic": 1,
		"bug": 1,
		"rock": 1,
		"ghost": 1,
		"dragon": 2,
		"dark": 1,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 1
	},
	"fighting": {
		"normal": 2,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 2,
		"fighting": 1,
		"poison": 0.5,
		"ground": 1,
		"flying": 0.5,
		"psychic": 0.5,
		"bug": 0.5,
		"rock": 2,
		"ghost": 0,
		"dragon": 1,
		"dark": 2,
		"steel": 2,
		"fairy" : 0.5,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 1
	},
	"poison": {
		"normal": 1,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 2,
		"ice": 1,
		"fighting": 1,
		"poison": 0.5,
		"ground": 0.5,
		"flying": 1,
		"psychic": 1,
		"bug": 1,
		"rock": 0.5,
		"ghost": 0.5,
		"dragon": 1,
		"dark": 1,
		"steel": 0,
		"fairy" : 2,
		"light" : 1,
		"sugar" : 2,
		"plastic" : 1
	},
	"ground": {
		"normal": 1,
		"fire": 2,
		"water": 1,
		"electric": 2,
		"grass": 0.5,
		"ice": 1,
		"fighting": 1,
		"poison": 2,
		"ground": 1,
		"flying": 0,
		"psychic": 1,
		"bug": 0.5,
		"rock": 2,
		"ghost": 1,
		"dragon": 1,
		"dark": 1,
		"steel": 2,
		"fairy" : 1,
		"light" : 1,
		"sugar" : 2,
		"plastic" : 1
	},
	"flying": {
		"normal": 1,
		"fire": 1,
		"water": 1,
		"electric": 0.5,
		"grass": 2,
		"ice": 1,
		"fighting": 2,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 2,
		"rock": 0.5,
		"ghost": 1,
		"dragon": 1,
		"dark": 1,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 1
	},
	"psychic": {
		"normal": 1,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 2,
		"poison": 2,
		"ground": 1,
		"flying": 1,
		"psychic": 0.5,
		"bug": 1,
		"rock": 1,
		"ghost": 1,
		"dragon": 1,
		"dark": 0,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 0.5,
		"sugar" : 0.5,
		"plastic" : 2
	},
	"bug": {
		"normal": 1,
		"fire": 0.5,
		"water": 1,
		"electric": 1,
		"grass": 2,
		"ice": 1,
		"fighting": 0.5,
		"poison": 0.5,
		"ground": 1,
		"flying": 0.5,
		"psychic": 2,
		"bug": 1,
		"rock": 1,
		"ghost": 0.5,
		"dragon": 1,
		"dark": 2,
		"steel": 0.5,
		"fairy" : 0.5,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 0.5
	},
	"rock": {
		"normal": 1,
		"fire": 2,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 2,
		"fighting": 0.5,
		"poison": 1,
		"ground": 0.5,
		"flying": 2,
		"psychic": 1,
		"bug": 2,
		"rock": 1,
		"ghost": 1,
		"dragon": 1,
		"dark": 1,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 1,
		"sugar" : 1,
		"plastic" : 1
	},
	"ghost": {
		"normal": 0,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 1,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 2,
		"bug": 1,
		"rock": 1,
		"ghost": 2,
		"dragon": 1,
		"dark": 0.5,
		"steel": 1,
		"fairy" : 1,
		"light" : 0,
		"sugar" : 2,
		"plastic" : 1
	},
	"dragon": {
		"normal": 1,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 1,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 1,
		"rock": 1,
		"ghost": 1,
		"dragon": 2,
		"dark": 1,
		"steel": 0.5,
		"fairy" : 0,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 1
	},
	"dark": {
		"normal": 1,
		"fire": 1,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 0.5,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 2,
		"bug": 1,
		"rock": 1,
		"ghost": 2,
		"dragon": 1,
		"dark": 0.5,
		"steel": 1,
		"fairy" : 0.5,
		"light" : 2,
		"sugar" : 1,
		"plastic" : 1
	},
	"steel": {
		"normal": 1,
		"fire": 0.5,
		"water": 0.5,
		"electric": 0.5,
		"grass": 1,
		"ice": 2,
		"fighting": 1,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 1,
		"rock": 2,
		"ghost": 1,
		"dragon": 1,
		"dark": 1,
		"steel": 0.5,
		"fairy": 2,
		"light" : 2,
		"sugar" : 1,
		"plastic" : 2
	},
	"fairy": {
		"normal": 1,
		"fire": 0.5,
		"water": 1,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 2,
		"poison": 0.5,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 1,
		"rock": 2,
		"ghost": 1,
		"dragon": 2,
		"dark": 2,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 1,
		"sugar" : 0.5,
		"plastic" : 0.5
	},
	"sugar": {
		"normal": 2,
		"fire": 0.5,
		"water": 0.5,
		"electric": 1,
		"grass": 1,
		"ice": 1,
		"fighting": 2,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 2,
		"bug": 1,
		"rock": 0.5,
		"ghost": 1,
		"dragon": 2,
		"dark": 2,
		"steel": 0,
		"fairy" : 2,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 0
	},
	"light": {
		"normal": 0.5,
		"fire": 0,
		"water": 1,
		"electric": 0.5,
		"grass": 0.5,
		"ice": 2,
		"fighting": 1,
		"poison": 1,
		"ground": 1,
		"flying": 1,
		"psychic": 1,
		"bug": 0.5,
		"rock": 0.5,
		"ghost": 2,
		"dragon": 1,
		"dark": 2,
		"steel": 1,
		"fairy" : 1,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 1
	},
	"plastic" : {
		"normal": 1,
		"fire": 0.5,
		"water": 2,
		"electric": 2,
		"grass": 2,
		"ice": 0.5,
		"fighting": 1,
		"poison": 0.5,
		"ground": 2,
		"flying": 1,
		"psychic": 1,
		"bug": 2,
		"rock": 0.5,
		"ghost": 1,
		"dragon": 0.5,
		"dark": 0.5,
		"steel": 0.5,
		"fairy" : 1,
		"light" : 0.5,
		"sugar" : 1,
		"plastic" : 0.5
	}
}
TYPES = [
	"normal",
	"fire",
	"water",
	"electric",
	"grass",
	"ice",
	"fighting",
	"poison",
	"ground",
	"flying",
	"psychic",
	"bug",
	"rock",
	"ghost",
	"dragon",
	"dark",
	"steel",
	"fairy",
	"light",
	"sugar",
	"plastic"
]

def get_weakness(type1 : str):
	res = {}
	for i in TYPES:
		res[i] = TYPE_TABLE[i][type1]
	return res

def get_weakness2(type1, type2):
	r1 = get_weakness(type1)
	r2 = get_weakness(type2)
	res = {}
	for i in TYPES:
		res[i] = r1[i] * r2[i]
	return res

def get_type_mult(attack, target):
	return TYPE_TABLE[attack][target]

def get_type_mult2(attack, target1, target2):
	return get_type_mult(attack, target1) * get_type_mult(attack, target2)



if __name__ == "__main__":
	t1 = PK_T_FIRE
	t2 = PK_T_FIGHTING
	print(f"{t1} / {t2}")
	d = get_weakness2(t1, t2)
	for i in d.keys():
		if d[i] != 1:
			print(f"{i}: {d[i]}")