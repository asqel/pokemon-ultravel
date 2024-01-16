from uti.hitbox import HITBOX_50X50
from uti.vector import *
from uti.hitbox import *
import pygame as py
import os 
import importlib as imp


OBJ_SIZE = 50 # px

class Obj:
    def __init__(self, id: str, istop: bool, texture: py.Surface, hitbox : bool = True, data:dict = None, light = None) -> None:
        self.id = id
        self.texture = texture
        self.toplayer = istop # object is under or above player and entities
        self.hitbox = hitbox
        self.data = ({} if data is None or not isinstance(data, dict) else data)
        self.light = light
    
    def on_interact(self,world,user):
        ...
    def on_walk_in(self,world,user):
        ...
    def on_draw(self,world,has_been_drawn, pos : Vec):
        ...
    def obj_copy(self):
        return Obj(self.id,self.toplayer,self.texture,self.hitbox,self.data)

class Dynamic_Obj:  #Object that can be updated on each tick
    def __init__(self, id: str, istop: bool, texture: py.Surface, hitbox : bool = True, data:dict = None, light = None) -> None:
        self.id = id
        self.texture = texture
        self.toplayer = istop # object is under or above player and entities
        self.hitbox = hitbox
        self.transparent=False #si on peut passer a travvers ou pas
        self.data = ({} if data is None or not isinstance(data, dict) else data)
        self.light = light
    
    def on_interact(self,world,user):
        ...
    def on_walk_in(self,world,user):
        ...
    def tick(self,world):
        ...
    def on_draw(self,world,has_been_drawn, pos : Vec):
        ...
    def dyn_obj_copy(self):
        return Obj(self.id,self.toplayer,self.texture,self.hitbox,self.data)

Objs={}
Dynamic_Objs={}


def registerObj(obj:type):
    Objs[obj.__name__]=obj
    
def registerDynamic_Obj(obj:type):
    Dynamic_Objs[obj.__name__]=obj


#import every objs
module_names=os.listdir(os.path.dirname(os.path.abspath(__file__)))

for i in range(len(module_names)):
    if module_names[i]=="__init__.py":
        module_names.pop(i)
        break
for i in range(len(module_names)):
    if module_names[i].endswith(".py"):
        module_names[i]=module_names[i][:-3]

for i in module_names:
    imp.import_module(f".{i}", __package__)


from uti.textures import *
from random import randint
class Grass(Obj):
    def __init__(self) -> None:
        super().__init__("Grass", 0, Textures["Obj"]["grass"+ str(randint(0, 4))])

class Air(Dynamic_Obj):
    def __init__(self) -> None:
        super().__init__("Air", 0, NOTHING_TEXTURE, False)


class TEST(Obj):
    def __init__(self) -> None:
        super().__init__("TEST", 0, Textures["Obj"]["pc"])
    def on_interact(self, world, user):
        user.open_gui("combat_gui")
registerObj(Grass)
registerObj(Air)
registerObj(TEST)



