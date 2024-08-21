from objs import *
from random import randint

class Grass(Obj):
    def __init__(self) -> None:
        super().__init__("Grass", 0, Textures["Obj"]["grass"+ str(randint(0, 4))])
        
registerObj(Grass)