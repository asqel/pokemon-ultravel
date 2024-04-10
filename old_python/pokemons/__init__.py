from uti.hitbox import HITBOX_50X50
from uti.vector import *
from uti.hitbox import *
import pygame as py
import os 
import importlib as imp

class Pokemon:
    def __init__(self, name : str, surname : str, level : int) -> None:
        self.name = name # species name
        self.surname = surname # custom user name
        self.level = level
        

Pokemons = {}
Pokemons_id : dict[str, tuple[int, str]]= {} # name : (dex_num, dex_type, class)


def registerObj(pok : type, name : str, dex_num : int, dex_type : str):
    Pokemons[pok.__name__] = pok
    Pokemons_id[name] = (dex_num, dex_type, pok)

    


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
    imp.import_module(f".{i}", __package__)



