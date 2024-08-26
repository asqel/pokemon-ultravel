from items import Item
from uti import *
import pygame as py
import os 
import importlib as imp
from random import getrandbits
from random import choice
from items import *
from pk_types import *

STAT_HP = 0
STAT_ATTACK = 1
STAT_DEFENSE = 2
STAT_SPE_DEFENSE = 3
STAT_SPE_ATTACK = 4
STAT_SPEED = 5

NATURES = [
    "Hardy",
    "Lonely",
    "Brave",
    "Adamant",
    "Naughty",
    "Bold",
    "Docile",
    "Relaxed",
    "Impish",
    "Lax",
    "Timid",
    "Hasty",
    "Serious",
    "Jolly",
    "Naive",
    "Modest",
    "Mild",
    "Quiet",
    "Bashful",
    "Rash",
    "Calm",
    "Gentle",
    "Sassy",
    "Careful",
    "Quirky"
]

def random_nature() -> str:
    return choice(NATURES)

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
                    item : Item,
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

    def get_max_hp(self) -> int:
        return int(((2 * self.base_stats[STAT_HP] + self.iv[STAT_HP] + self.ev[STAT_HP] / 4 + 100) * self.level) / 100 + 10)
    
    def get_stat(self, stat : int) -> int:
        return int((((2*self.base_stats[stat] + self.iv[stat] + self.ev[stat]/4) * self.level) / 100 + 5) * self.get_nature_modif(stat))
    
    def get_nature_modif(self, stat : int) -> float:
        return 1

    def get_sprite(self):
        if self.shiny:
            return self.sprites[1]
        return self.sprites[0]
    

Pokemons_id : dict[int, tuple[str, Pokemon]]= {} # id:(species_name, class)

# __init__(self, level : int, surname : str, gender : int, shiny : bool, item: Item)
#   if gender == -1 it has to be randomly choosen
#   0 : male / 1 : female | if gender requested doesnt exist for this species ignore it
def register_pokemon(pk_id : int, species_name : str, pk_class : type):
    Pokemons_id[pk_id] = (species_name, pk_class)



class MISSING_NO(Pokemon):
    def __init__(self, level : int, surname : str, gender : int, shiny : bool) -> None:
        super().__init__(0, surname, level, [PK_T_NORMAL, PK_T_NORMAL], "NONE", [1, 1, 1, 1, 1, 1], 0, NOTHING_TEXTURE, shiny, items["Air"])

#import every objs
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



