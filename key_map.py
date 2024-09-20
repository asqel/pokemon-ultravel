import pygame as py
import json

key_map = {}

"""
keys.json
{
    trigger: keyname # str: str
}
trigger:
"""
t_mov_up = "mov up"
t_mov_down = "mov down"
t_mov_left = "mov left"
t_mov_right = "mov right"
t_use_object = "use object"
t_sprint = "sprint"
t_stay = "stay"

key_entries = [
    t_mov_up,
    t_mov_down,
    t_mov_left,
    t_mov_right,
    t_use_object,
    t_sprint,
    t_stay
]
"""
key names:
    a-z
    0-9
    lctrl
    rctrl
    lshift
    rshift
    tab
    space
    enter
    M1 (lclick)
    M2 (midclick)
    M3 (rclick)
"""
def str_to_code(key : str):
    key = key.lower()
    if key in "abcdefghijklmnopqrstuvwxyz":
        return py.key.key_code(key)
    if key in "1234567890":
        return py.key.key_code(key)
    if key == "lctrl":
        return py.K_LCTRL
    if key == "rctrl":
        return py.K_RCTRL
    if key == "lshift":
        return py.K_LSHIFT
    if key == "rshift":
        return py.K_RSHIFT
    if key == "tab":
        return py.K_TAB
    if key == "space":
        return py.K_SPACE
    if key == "enter":
        return py.K_RETURN
    if key == "m1":
        return (1, 1)
    if key == "m2":
        return (1, 2)
    if key == "m3":
        return (1, 3)
def load_keys():
    global key_map
    le_json = {}
    with open("./key_map.json","r") as f:
        le_json = json.load(f)
    for i in le_json.keys():
        key_map[i]= le_json[i]
    for i in key_map.keys():
        key_map[i]= str_to_code(key_map[i])
    for i in key_entries:
        if i not in key_map.keys():
            key_map[i] = None
    return key_map

def register_key_entry(key_entry : str):
    key_entries.append(key_entry)


def get_pressed(events: list[py.event.Event]) -> dict[str, int]:
    """
    key: state (0: nothing, 1: pressed, 2: released)
    """
    res = {i : 0 for i in key_entries}
    for i in events:
        if i.type == py.KEYDOWN:
            for k in key_map.keys():
                if i.key == key_map[k]:
                    res[k] = 1
                    break
        elif i.type == py.KEYUP:
            for k in key_map.keys():
                if i.key == key_map[k]:
                    res[k] = 2
                    break
        if i.type == py.MOUSEBUTTONDOWN:
            for k in key_map.keys():
                if (1, i.button) == key_map[k]:
                    res[k] = 1
                    break
        elif i.type == py.MOUSEBUTTONUP:
            for k in key_map.keys():
                if (1, i.button) == key_map[k]:
                    res[k] = 2
                    break
    return res

