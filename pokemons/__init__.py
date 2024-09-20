from uti import *
import pygame as py
import os 
import importlib as imp
from random import getrandbits, choice, uniform
import items
from pk_types import *
import entities as en

STAT_HP = 0
STAT_ATTACK = 1
STAT_DEFENSE = 2
STAT_SPE_DEFENSE = 3
STAT_SPE_ATTACK = 4
STAT_SPEED = 5

NATURES :dict[str, tuple[float, float, float, float, float, float]] = {
               # HP   AT  DE   SDE  SAT  SP
    "Hardy":   (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), # neutral
    "Lonely":  (1.0, 1.1, 0.9, 1.0, 1.0, 1.0),
    "Brave":   (1.0, 1.1, 1.0, 1.0, 1.0, 0.9),
    "Adamant": (1.0, 1.1, 1.0, 1.0, 0.9, 1.0),
    "Naughty": (1.0, 1.1, 1.0, 0.9, 1.0, 1.0),
    "Bold":    (1.0, 0.9, 1.1, 1.0, 1.0, 1.0),
    "Docile":  (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), # neutral
    "Relaxed": (1.0, 1.0, 1.1, 1.0, 1.0, 0.9),
    "Impish":  (1.0, 1.0, 1.1, 1.0, 0.9, 1.0),
    "Lax":     (1.0, 1.0, 1.1, 0.9, 1.0, 1.0),
    "Timid":   (1.0, 0.9, 1.0, 1.0, 1.0, 1.1),
    "Hasty":   (1.0, 1.0, 0.9, 1.0, 1.0, 1.1),
    "Serious": (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), # neutral
    "Jolly":   (1.0, 1.0, 1.0, 1.0, 0.9, 1.1),
    "Naive":   (1.0, 1.0, 1.0, 0.9, 1.0, 1.1),
    "Modest":  (1.0, 0.9, 1.0, 1.0, 1.1, 1.0),
    "Mild":    (1.0, 1.0, 0.9, 1.0, 1.1, 1.0),
    "Quiet":   (1.0, 1.0, 1.0, 1.0, 1.1, 0.9),
    "Bashful": (1.0, 1.0, 1.0, 1.0, 1.0, 1.0), # neutral
    "Rash":    (1.0, 1.0, 1.0, 0.9, 1.1, 1.0),
    "Calm":    (1.0, 0.9, 1.0, 1.1, 1.1, 1.0),
    "Gentle":  (1.0, 1.0, 0.9, 1.1, 1.0, 1.0),
    "Sassy":   (1.0, 1.0, 1.0, 1.1, 1.0, 0.9),
    "Careful": (1.0, 1.0, 1.0, 1.1, 0.9, 1.0),
    "Quirky":  (1.0, 1.0, 1.0, 1.0, 1.0, 1.0) # neutral
}
STATUS_catch_bonus = {
    "NULL" : 0,
    "SLEEP" : 10,
    "FREEZE" : 10,
}

def get_status_catch_bonus(stat: str) -> int:
    if stat not in STATUS_catch_bonus.keys():
        return 0
    return STATUS_catch_bonus[stat]

def random_nature() -> str:
    return choice(list(NATURES.keys()))

def gen_IV():
    n1 = getrandbits(16)
    n2 = getrandbits(16)
    stats = [0, 0, 0, 0, 0, 0]
    stats[STAT_HP] = n1 & 31
    stats[STAT_ATTACK] = (n1 >> 5) & 31
    stats[STAT_DEFENSE] = (n1 >> 10) & 31
    stats[STAT_SPE_DEFENSE] = n2 & 31
    stats[STAT_SPE_ATTACK] = (n2 >> 5) & 31
    stats[STAT_SPEED] = (n2 >> 10) & 31
    return stats

def xp_gained(player: 'en.Character', pk: 'Pokemon', enemy: 'Pokemon') -> int:
    b = enemy.base_xp
    e = 1 # lucky egg modifier
    f = 1 # affection
    L = enemy.level
    L_p = pk.level
    p = 1 # exp charm
    s = 1 # check if has participated (=2 if not)
    t = 1 if pk.owner == player.save_id else 1.5
    v = 1 # check if past evolv (=4915/4096 if so)
    return (b * L / 5 * 1 / s * ((2 * L + 10) / (L + L_p + 10))**2.5 + 1) * t * e * v *f *p

def get_nature_modifier(nature: str, stat: int) -> float:
    if nature not in NATURES.keys():
        return 1
    return NATURES[nature][stat]

def get_catch_rate(player: 'en.Character', pk_team_idx: int, to_catch : 'Pokemon', ball: items.Item) -> float:
    bonus_ball = 1
    if isinstance(ball, items.Ball_item):
        bonus_ball = ball.catch_bonus(player, pk_team_idx, to_catch)
    HP_max = to_catch.get_max_hp()
    HP_current = to_catch.hp
    return int(((3 * HP_max - 2 * HP_current) / (3 * HP_max)) * 4096 * 1 * to_catch.get_catch_rate() * bonus_ball) * get_status_catch_bonus(to_catch.status)

SHINY_PROBA = 1 / 4096

def random_is_shiny() -> int:
    return uniform(0, 1) <= SHINY_PROBA

class Pokemon:
    def __init__(self,
                    pk_id : int,
                    surname : str,
                    level : int,
                    types:tuple[str, str | None],
                    nature : str,
                    base_stats : list[float],
                    genders : tuple[float, float], # male / female proba (0-1)
                    sprites : tuple[py.Surface, py.Surface], # sprite normal / shiny
                    shiny : bool,
                    item : items.Item,
                    base_xp : int
                ) -> None:
        self.pk_id = pk_id
        self.surname = surname # custom user name
        self.level = level
        self.nature = nature
        self.types = types
        self.base_stats = base_stats
        self.genders = genders
        self.iv = gen_IV()
        self.ev = [0, 0, 0, 0, 0, 0]
        self.sprites = sprites
        self.shiny = shiny
        self.item = item
        self.is_gender_less = 0
        self.hp = 0
        self.base_xp = base_xp
        self.owner = "NULL"
        self.status = "NULL"

    def get_max_hp(self) -> int:
        return int(((2 * self.base_stats[STAT_HP] + self.iv[STAT_HP] + self.ev[STAT_HP] / 4 + 100) * self.level) / 100 + 10)
    
    def get_stat(self, stat : int) -> int:
        return int((((2*self.base_stats[stat] + self.iv[stat] + self.ev[stat]/4) * self.level) / 100 + 5) * self.get_nature_modif(stat))
    
    def get_nature_modif(self, stat : int) -> float:
        return get_nature_modifier(self.nature, stat)

    def get_sprite(self):
        if self.shiny:
            return self.sprites[1]
        return self.sprites[0]
    
    def get_catch_rate(self) -> float:
        """
        return number between 0 and 100
        """
        return 50
    

Pokemons_id : dict[int, tuple[str, Pokemon]]= {} # id:(species_name, class)

# __init__(self, level : int, surname : str, gender : int, shiny : bool, item: Item, base_xp : int)
#   if gender == -1 it has to be randomly choosen
#   0 : male / 1 : female | if gender requested doesnt exist for this species ignore it
def register_pokemon(pk_id : int, species_name : str, pk_class : type):
    Pokemons_id[pk_id] = (species_name, pk_class)



class MISSING_NO(Pokemon):
    def __init__(self, level : int, surname : str, gender : int, shiny : bool) -> None:
        super().__init__(0, surname, level, [PK_T_NORMAL, PK_T_NORMAL], "NONE", [1, 1, 1, 1, 1, 1], 0, NOTHING_TEXTURE, shiny, items.items["Air"], 1)

#import every pokemons
module_names=os.listdir(os.path.dirname(os.path.abspath(__file__)))

for i in range(len(module_names)):
    if module_names[i] == "__init__.py":
        module_names.pop(i)
        break

for i in range(len(module_names)):
    if module_names[i].endswith(".py"):
        module_names[i]=module_names[i][:-3]

for i in module_names:
    if i is not None:
        imp.import_module(f".{i}", __package__)
