import json
import world as wo
import objs
from uti import *
from events import *
from typing import TypedDict
import os

worlds_path = os.path.join(os.path.abspath("."), "worlds")
template_path = os.path.join(os.path.abspath("."), "templates")
dir_path = os.path.abspath(".")

pk_dict = dict[str, 'pk_dict_value']
pk_dict_value = str | int | float | bool | list | pk_dict


def create_dir_ifn_exist(path: str) -> bool:
    """
    return false if it already exists true if it had to be created
    """
    if os.path.exists(path) and os.path.isdir(path):
        return False
    os.makedirs(path, exist_ok = True)
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

def chunk_to_json(chunk : 'wo.Chunk') -> dict:
    res = {}
    res["pos"] = [chunk.pos.x, chunk.pos.y]
    res["top_left_pos"] = [chunk.top_left_pos.x, chunk.top_left_pos.y]
    res["background_obj"] = [[0 for i in range(wo.CHUNK_LEN)] for k in range(wo.CHUNK_LEN)]
    res["objects"] = [[0 for i in range(wo.CHUNK_LEN)] for k in range(wo.CHUNK_LEN)]
    res["objects_foreground"] = [[0 for i in range(wo.CHUNK_LEN)] for k in range(wo.CHUNK_LEN)]
    res["dyn_objects"] = [[0 for i in range(wo.CHUNK_LEN)] for k in range(wo.CHUNK_LEN)]
    res["dyn_objects_foreground"] = [[0 for i in range(wo.CHUNK_LEN)] for k in range(wo.CHUNK_LEN)]
    for x in range(wo.CHUNK_LEN):
        for y in range(wo.CHUNK_LEN):
            if chunk.background_obj[y][x].id != objs.default_air.id:
                res["background_obj"][y][x] = chunk.background_obj[y][x].to_dict()
            if chunk.objects[y][x].id != objs.default_air.id:
                res["objects"][y][x] = chunk.objects[y][x].to_dict()
            if chunk.objects_foreground[y][x].id != objs.default_air.id:
                res["objects_foreground"][y][x] = chunk.objects_foreground[y][x].to_dict()
            if chunk.dyn_objects[y][x].id != objs.default_air.id:
                res["dyn_objects"][y][x] = chunk.dyn_objects[y][x].to_dict()
            if chunk.dyn_objects_foreground[y][x].id != objs.default_air.id:
                res["dyn_objects_foreground"][y][x] = chunk.dyn_objects_foreground[y][x].to_dict()
    return res
    
def save_world(world : 'wo.World'):
    create_dir_ifn_exist(worlds_path)
    if world.mod != "":
        path = os.path.join("./mods/", world.mod, "worlds", world.name)
    else:
        path = os.path.join(worlds_path, world.name)
    create_dir_ifn_exist(path)
    for i in world.loaded_chunks.keys():
        chunk_path = os.path.join(path, f"c_{i[0]}_{i[1]}.json")
        create_file_ifn_exist(chunk_path)
        with open(chunk_path, "w") as f:
            print(chunk_to_json(world.loaded_chunks[i]))
            json.dump(chunk_to_json(world.loaded_chunks[i]), f, separators=(',', ':'))


def load_chunk(d : dict, w : 'wo.World') -> 'wo.Chunk':
    res = wo.Chunk(Vec(d["pos"][0], d["pos"][1]), w)
    for x in range(wo.CHUNK_LEN):
        for y in range(wo.CHUNK_LEN):
            if d["background_obj"][y][x] != 0 and d["background_obj"][y][x]["id"] in objs.Objs.keys():
                o : objs.Obj = objs.Objs[d["background_obj"][y][x]["id"]]()
                o.from_dict(d["background_obj"][y][x])
                res.background_obj[y][x] = o
            if d["objects"][y][x] != 0 and d["objects"][y][x]["id"] in objs.Objs.keys():
                o : objs.Obj = objs.Objs[d["objects"][y][x]["id"]]()
                o.from_dict(d["objects"][y][x])
                res.objects[y][x] = o
            if d["objects_foreground"][y][x] != 0 and d["objects_foreground"][y][x]["id"] in objs.Objs.keys():
                o : objs.Obj = objs.Objs[d["objects_foreground"][y][x]["id"]]()
                o.from_dict(d["objects_foreground"][y][x])
                res.objects_foreground[y][x] = o
            if d["dyn_objects"][y][x] != 0 and d["dyn_objects"][y][x]["id"] in objs.Objs.keys():
                o : objs.Obj = objs.Objs[d["dyn_objects"][y][x]["id"]]()
                o.from_dict(d["dyn_objects"][y][x])
                res.dyn_objects[y][x] = o
            if d["dyn_objects_foreground"][y][x] != 0 and d["dyn_objects_foreground"][y][x]["id"] in objs.Objs.keys():
                o : objs.Obj = objs.Objs[d["dyn_objects_foreground"][y][x]["id"]]()
                o.from_dict(d["dyn_objects_foreground"][y][x])
                res.dyn_objects_foreground[y][x] = o
    return res


def world_exists(name : str, mod : str = "") -> bool:
    if mod != "":
        path = os.path.join("./mods/", mod, "worlds", name)
    else:
        path = os.path.join(worlds_path, name)
    return os.path.exists(path) and os.path.isdir(path)
"""

while playing chunks loaded are loaded and unloaded

in worldeditor they are never unloaded except when saving

//create a customizable class for world like objkects


"""