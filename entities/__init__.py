from uti.vector import *
from uti.hitbox import *
from quests import *
from uti.textures import *
from interface import *
from items import *
import pygame as py

class Character:
    def __init__(self, x : float, y : float, world):
        self.inventaire : list[Item] = [items["Air"](1) for i in range(10)]
        self.is_moving = 0
        self.inventaire_idx = 0 
        self.pv = 100
        self.pvmax = 100
        self.effects = []
        self.hitbox = Hitbox(HITBOX_RECT_t, Vec(0, 0), width = 50, height = 50)
        self.current_texture = MC_FRAMES[2][0]
        self.current_frame = 0
        self.frame_cooldown = 0
        self.frames : list[tuple[py.Surface, py.Surface, py.Surface]] = MC_FRAMES
        self.pos = Vec(x, y)
        self.protection = 0
        self.dir : str = "d" #d -> down  |  u -> up  |  r -> right  |  l -> left  |
        self.level = 0
        self.speed = 2 # px / tick
        self.isvisible=True
        self.render_distance=3
        self.world = world
        self.chunk_border = False
        self.riding : Npc = None # entity wich the player is riding
        self.zoom_out = 1
        self.speed_multiplier : dict[str, int] = {} # name : value
        self.transparent = False # si on peut passer a travers != de invisble
        self.guis : list[Gui] = []
        self.data = {} # str-> str | int | float | list | dict
        self.is_world_editor = False
        self.day_count = 0
        self.tick_count = 0
        self.quests : dict[str, Quest] = {} # incompleted quests
        self.quests_completed : dict[str, Quest] = {}
        self.save_id = "NULL"
    

    def next_frame(self, dir : int):
        if not self.frame_cooldown:
            self.current_frame += 1
            if self.current_frame > 2:
                self.current_frame = 0
            self.current_texture = self.frames[dir][self.current_frame]
            self.frame_cooldown = 5
        else:
            self.frame_cooldown -= 1

    def tick(self):
        if self.is_moving:
            if self.dir == "d":
                self.pos.y += self.speed
                self.next_frame(2)
            elif self.dir == "u":
                self.pos.y -= self.speed
                self.next_frame(0)
            elif self.dir == "l":
                self.pos.x -= self.speed
                self.next_frame(3)
            else:
                self.pos.x += self.speed
                self.next_frame(1)
            if int(self.pos.x) % 50 == int(self.pos.y) % 50 == 0:
                self.is_moving = 0
        else:
            if self.dir == "d":
                self.current_texture = self.frames[2][0]
            elif self.dir == "u":
                self.current_texture = self.frames[0][0]
            elif self.dir == "l":
                self.current_texture = self.frames[3][0]
            else:
                self.current_texture = self.frames[1][0]
    
    def move_dir(self, dir : str):
        if not self.is_moving:
            self.dir = dir
            if self.dir == "d":
                if self.world.can_move_to(self, self.pos + (0, 50)):
                    self.is_moving = 1
            elif self.dir == "u":
                if self.world.can_move_to(self, self.pos - (0, 50)):
                    self.is_moving = 1
            elif self.dir == "l":
                if self.world.can_move_to(self, self.pos - (50, 0)):
                    self.is_moving = 1
            else:
                if self.world.can_move_to(self, self.pos + (50, 0)):
                    self.is_moving = 1
    def on_draw(self,world,has_been_drawn):
        ...
    
    def open_gui(self, gui_name : str):
        self.guis.append(guis[gui_name](self))
        
    def close_gui(self):
        if self.guis:
            self.guis.pop(-1)
    
    def has_quest(self, _id : str):
        return _id in self.quests.keys() or _id in self.quests_completed.keys()
    
    def has_quest_done(self, _id : str):
        return _id in self.quests_completed.keys()

    def has_quest_incompleted(self, _id : str):
        return _id in self.quests.keys()

    def add_quest(self, _id : str, quest : Quest):
        self.quests[_id] = quest

    def add_quest_completed(self, _id : str, quest : Quest):
        self.quests_completed[_id] = quest

    def get_quest(self, _id : str):
        if _id in self.quests.keys():
            return self.quests[_id]
        return None

    def get_quest_completed(self, _id : str):
        if _id in self.quests_completed.keys():
            return self.quests_completed[_id]
        return None

    def complete_quest(self, _id):
        if _id in self.quests.keys():
            self.quests_completed[_id] = self.quests[_id]
            self.quests.pop(_id)
class Npc:
    def __init__(self,name:str,surname:str,texture:py.Surface,spells,pos:Vec,texture_pos:Vec=NULL_VEC,hitbox:Hitbox=HITBOX_50X50,action=None,tick=None) -> None:
        self.name=name
        self.surname=surname
        self.texture=texture
        self.current_texture=self.texture[2]
        self.dir="d"
        self.spells=spells
        self.isvisible=True
        self.pv=100
        self.hitbox=hitbox
        self.pos=pos
        self.texture_pos=texture_pos
        self.speed=0.5
        self.speed_multiplier : dict[str:int] = {} # name : value
        self.transparent=False # si on peut passer a travers != de invisble
        self.collide_player = True
        self.world = None
        self.rider : Character = None
        self.data = {}
        self.rider_offset = Vec(0,0)
    
    def on_draw(self,world,has_been_drawn):
        ...
    def die(self, world):
        return 1
    def tick(self,world):
        ...
    def mov(self,world,rider,dir : str): #dir : u/d/r/l/ur/ul/dr/dl
        ...
    def on_interact(self,world,user):
        ...
players:list[Character]=[]

Npcs : dict[str,type] = {}


def registerNpc(npc:type):
    Npcs[npc.__name__]=npc
    
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


