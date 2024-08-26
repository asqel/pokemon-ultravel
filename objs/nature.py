from pygame import Surface
from objs import *
from random import randint
import interface.fight as fight
import pokemons as pk
import items

from uti import Vec

class Grass(Obj):
    def __init__(self) -> None:
        super().__init__("Grass", 0, Textures["Obj"]["grass"+ str(randint(0, 4))])
        
registerObj(Grass)

class Campfire(Obj):
    def __init__(self) -> None:
        self.current_frame = 0
        self.cooldown = 50
        super().__init__("Campfire", 1, Textures["Obj"]["campfire0"])
    
    def on_draw(self, world, has_been_drawn, pos: Vec, screen_pos: Vec):
        self.cooldown -= 1
        if self.cooldown == 0:
            self.current_frame += 1
            self.cooldown = 10
        if self.current_frame >= 5:
            self.current_frame = 0
        self.texture = Textures["Obj"][f"campfire{self.current_frame}"]

    def on_interact(self, world, user):
        fight.new_fight(user, [pk.Pokemons_id[1][1](23, "huit", -1, 1, items.items["Air"](1))])


registerObj(Campfire)
register_simple_obj("Pumpkin", Textures["Obj"]["pumpkin"])

register_simple_obj("Ruin_wall0", Textures["Obj"]["ruin_wall0"])
register_simple_obj("Ruin_wall1", Textures["Obj"]["ruin_wall1"])
register_simple_obj("Ruin_wall2", Textures["Obj"]["ruin_wall2"])
register_simple_obj("Ruin_wall3", Textures["Obj"]["ruin_wall3"])
register_simple_obj("Ruin_wall4", Textures["Obj"]["ruin_wall4"])
