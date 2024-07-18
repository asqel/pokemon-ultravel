import json
from world import *
from objs import *
from uti import *
from events import *
from typing import TypedDict
import os

worlds_path = os.path.join(os.path.abspath("."), "worlds")
template_path = os.path.join(os.path.abspath("."), "templates")
dir_path = os.path.abspath(".")

pk_dict = dict[str, 'pk_dict_value']
pk_dict_value = str | int | float | bool | list | pk_dict

DO_TEMPLATE = False

def create_dir_ifn_exist(path: str) -> bool:
    """
    return false if it already exists true if it had to be created
    """
    if os.path.exists(path) and os.path.isdir(path):
        return False
    os.mkdir(path, exist_ok = True)
    return True

def create_file_ifn_exist(path: str) -> bool:
    """
    return false if it already exists true if it had to be created
    """
    if os.path.exists(path) and os.path.isfile(path):
        return False
    open(path, "x").close()
    return True

def write_and_create_ifn_exist(path: str, text: str):
    if not(os.path.exists(path) and os.path.isfile(path)):
        f = open(path, "x")
    else:
        f = open(path, "w")
    f.write(text)
    f.close()
    
    

def create_world_save(world: World) -> None:
    fullname = world.mod + '_SEP_' + world.name
    path = os.path.join(worlds_path, fullname)
    create_dir_ifn_exist(path)
    create_file_ifn_exist(os.path.join(path, "info.json"))
    create_file_ifn_exist(os.path.join(path, "data.json"))
    create_dir_ifn_exist(os.path.join(path, "chunks"))

def save_chunk(world: World, chunk: Chunk):
    fullname = world.mod + '_SEP_' + world.name
    path = os.path.join(worlds_path, fullname, "chunks", f"c_{str(chunk.pos.x)}_{str(chunk.pos.y)}.json")
    write_and_create_ifn_exist(path, json.dumps(chunk.to_dict()))
 
def load_chunk(world: World, pos: Vec):
    fullname = world.mod + '_SEP_' + world.name
    path = os.path.join(worlds_path, fullname, "chunks", f"c_{str(pos.x)}_{str(pos.y)}.json")
    return Chunk(pos, world)
    
    

"""

while playing chunks loaded are loaded and unloaded

in worldeditor they are never unloaded except when saving

//create a customizable class for world like objkects

"""