import jsonizer as js
from uti import *
import pygame as py
import os 
import importlib as imp


OBJ_SIZE = TILE_SIZE # px

class Obj:
    def __init__(self, id: str, istop: bool, texture: py.Surface, hitbox : bool = True, data:dict = None, light = None) -> None:
        self.id = id
        self.texture = texture
        self.toplayer = istop # object is under or above player and entities
        self.hitbox = hitbox
        self.data = ({} if data is None or not isinstance(data, dict) else data)
        self.light = light
    
    def on_interact(self, world, user):
        ...
    def on_walk_in(self, world, user):
        ...
    def on_draw(self, world, has_been_drawn, pos : Vec, screen_pos :Vec):
        ...
    def tick(self, world):
        ...
    def obj_copy(self):
        return Obj(self.id,self.toplayer,self.texture,self.hitbox,self.data)

    def data_to_json(self) -> js.pk_dict:
        keys = self.data.keys()
        assert len(keys) == 0 or any(str != type(i) for i in keys)
        return self.data
    
    def to_dict(self) -> js.pk_dict:
        return {"id": self.id, "data": self.data_to_json()}

    def from_dict(self, d : js.pk_dict) -> None:
        self.data = d["data"]




Objs : dict[str, Obj] = {}

def register_simple_obj(id_ : str, texture : py.Surface):
    registerObj(
        type(
            id_,
            (Obj, ),
            {
                "__init__" : lambda self : super(self.__class__, self).__init__(id_, 0, texture)
            }
        )
    )

def registerObj(obj:type):
    Objs[obj.__name__] = obj

class Air(Obj):
    def __init__(self) -> None:
        super().__init__("Air", 0, NOTHING_TEXTURE, False)


default_air = Air()

registerObj(Air)

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







