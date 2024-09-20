import itertools
import pygame
from objs import *
from entities import *
from objs import *
from events import *
import json
import jsonizer as js
import items

#in pixel (its a square)
CHUNK_SIZE = 20 * TILE_SIZE
show_hitbox = False
# number of object in each direction in each chunk
CHUNK_LEN = CHUNK_SIZE // OBJ_SIZE

class Chunk:
    def __init__(self, chunk_pos : 'Vec', world : 'World') -> None:
        self.pos : Vec = chunk_pos # pos x,y in World:chuncks
        self.top_left_pos : Vec = chunk_pos * CHUNK_SIZE
        self.world :World = world
        self.entities : list[Npc] = []
        # [y][x]
        self.background_obj : list[list[Obj]] = [[default_air for k in range(CHUNK_LEN)] for i in range(CHUNK_LEN)]
        self.objects : list[list[Obj]] = [[default_air for k in range(CHUNK_LEN)] for i in range(CHUNK_LEN)]
        self.objects_foreground : list[list[Obj]] = [[default_air for k in range(CHUNK_LEN)] for i in range(CHUNK_LEN)]
        self.dyn_objects : list[list[Obj]] = [[default_air for k in range(CHUNK_LEN)] for i in range(CHUNK_LEN)]
        self.dyn_objects_foreground : list[list[Obj]] = [[default_air for k in range(CHUNK_LEN)] for i in range(CHUNK_LEN)]

    def get_borders(self)->list['Vec']:
        """
        return corners of the chunk
        (Top-left, Top-right, bottom-left, bottom-right)
        each corner are in the chunk
        if chunk is at 0:
            return ( (0,0), (999,0), (0,999), (999,999) )
        """
        x=self.top_left_pos.x
        y=self.top_left_pos.y
        return (Vec(x, y), Vec(x + CHUNK_SIZE - 1, y), Vec(x, y + CHUNK_SIZE - 1), Vec(x + CHUNK_SIZE - 1, y + CHUNK_SIZE - 1))

    def tick(self):
        """
        check if entities or objects are outside the chunk but still registered in chunk
        if so then they will be moved to the right chunk
        """
        p = 0
        while p < len(self.entities):
            new_pos = self.entities[p].pos// CHUNK_SIZE
            if new_pos != self.pos:
                self.world.get_Chunk_at(new_pos).entities.append(self.entities.pop(p))
                continue
            p += 1
    def to_dict(self) -> dict:
        res = {}
        res["pos"] = [self.pos.x, self.pos.y]
        res["top_left"] = [self.top_left_pos.x, self.top_left_pos.y]
        res["background_obj"] = [[0 for i in range(CHUNK_LEN)] for k in range(CHUNK_LEN)]
        res["objects"] = [[0 for i in range(CHUNK_LEN)] for k in range(CHUNK_LEN)]
        res["objects_foreground"] = [[0 for i in range(CHUNK_LEN)] for k in range(CHUNK_LEN)]
        res["dyn_objects"] = [[0 for i in range(CHUNK_LEN)] for k in range(CHUNK_LEN)]
        res["dyn_objects_foreground"] = [[0 for i in range(CHUNK_LEN)] for k in range(CHUNK_LEN)]
        for y in range(CHUNK_LEN):
            for x in range(CHUNK_LEN):
                if self.background_obj[y][x] != default_air:
                    res["background_obj"] = self.background_obj[y][x].to_dict()

                if self.objects[y][x] != default_air:
                    res["objects"] = self.objects[y][x].to_dict()

                if self.objects_foreground[y][x] != default_air:
                    res["objects_foreground"] = self.objects_foreground[y][x].to_dict()

                if self.dyn_objects[y][x] != default_air:
                    res["dyn_objects"] = self.dyn_objects[y][x].to_dict()

                if self.dyn_objects_foreground[y][x] != default_air:
                    res["dyn_objects_foreground"] = self.dyn_objects_foreground[y][x].to_dict()




class World:
    """
    difference between function called ...at and ...from_pos:
        ...at : pos in the chunks dictionary of the world like chunk.pos
        ...from_pos : pos of an entity or player or an object
    
    """
    def __init__(self, name, background_col : list[int], mod = "", is_outside = False) -> None:
        self.name = name
        self.bg = background_col
        self.mod = mod
        self.loaded_chunks : dict[tuple[int,int],Chunk]= {} #(x,y) : chunk
        self.has_to_collide = False # this check if collisions have to be computed when player moves it is set to True
                                  # will call chunk.tick if true 
        self.is_outside = is_outside

    def activate_collision(self):
        """
        set has_to_collide to true 
        when the world tick and has_to_cliide is true then the collision will be called
        """
        self.has_to_collide = True

    def add_entity(self, n:Npc)->None:
        """
        add an entity to the world
        if the entity is in a chunk that doesn't exists the chunk will be generated 
        """
        self.get_Chunk_from_pos(n.pos).entities.append(n)
        
    def add_background_Obj(self, n:Obj, pos : Vec):
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.background_obj[pos.y][pos.x] = n

    def can_move_to(self, player, pos):
        if self.get_Obj(pos).hitbox:
            return 0
        if self.get_dyn_Obj(pos).hitbox:
            return 0
        if self.get_dyn_Obj_fore(pos).hitbox:
            return 0
        if self.get_Obj_fore(pos).hitbox:
            return 0
        return 1
    def add_Obj(self, n:Obj, pos : Vec)->None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.objects[pos.y][pos.x] = n
    def add_foreground_Obj(self, n:Obj, pos : Vec)->None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.objects_foreground[pos.y][pos.x] = n
    def add_Dyn_Obj(self, n:Obj, pos : Vec)->None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.dyn_objects[pos.y][pos.x] = n
    def add_foreground_Dyn_Obj(self, n:Obj, pos : Vec)->None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.dyn_objects_foreground[pos.y][pos.x] = n   
    def gen_Chunk_at(self, pos:Vec):
        """
        generate a new chunk at {pos} (pos of chunk)
        if chunk already exist it will be erased
        """
        if tuple(pos) not in self.loaded_chunks.keys():
            self.loaded_chunks[tuple(pos)] = newChunk(pos,self)
        for i in events[Event_on_chunk_generate]:
            i.function(players, self.loaded_chunks[pos.x][pos.y])
        
    def gen_Chunk_from_pos(self, pos:Vec):
        """
        generate a new chunk at {pos} (pos of obj/entity)
        if chunk already exist it will be erased
        """
        return self.gen_Chunk_at(pos//CHUNK_SIZE)
        
    def get_Chunk_at(self, pos:Vec)->Chunk:
        """
        return the chunk at {pos} (pos of chunk)
        """
        pos = pos.floor()
        pos_as_tuple = tuple(pos)
        if pos_as_tuple not in self.loaded_chunks:
            if self.mod == "":
                if os.path.exists(f"./worlds/{self.name}/c_{pos.x}_{pos.y}.json"):
                    with open(f"./worlds/{self.name}/c_{pos.x}_{pos.y}.json","r") as f:
                        self.loaded_chunks[pos_as_tuple] = js.load_chunk(json.load(f), self)
                else:
                    self.gen_Chunk_at(pos)
            else:
                if os.path.exists(f"./mods/{self.mod}/worlds/{self.name}/c_{pos.x}_{pos.y}.json"):
                    with open(f"./mods/{self.mod}/worlds/{self.name}/c_{pos.x}_{pos.y}.json","r") as f:
                        self.loaded_chunks[pos_as_tuple] = js.load_chunk(json.load(f), self)
                else:
                    self.gen_Chunk_at(pos)
        return self.loaded_chunks[pos_as_tuple]

    def get_Chunk_from_pos(self, pos:Vec)->Chunk:
        """
        return the chunk at {pos} (pos of obj/entity)
        """
        return self.get_Chunk_at(pos//CHUNK_SIZE)
        
    def chunk_exists_at(self, pos:Vec) -> bool:
        """
        return if the chunk at {pos} exists (pos of chunk)
        """
        if tuple(pos) in self.loaded_chunks.keys():
            return True
        if self.mod == "":
            return os.path.exists(f"./worlds/{self.name}/c_{pos.x}_{pos.y}.json")
        else:
            return os.path.exists(f"./mods/{self.mod}/worlds/{self.name}/c_{pos.x}_{pos.y}.json")
        return False 

    def chunk_exists_from_pos(self, pos:Vec) -> bool:
        """
        return if the chunk at {pos} exists (pos of obj/entity)
        """
        return self.chunk_exists_at(pos // CHUNK_SIZE)
    
    def get_Obj(self, pos:Vec) ->Obj:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        return c.objects[pos.y][pos.x]
    def get_Obj_fore(self, pos:Vec) ->Obj:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        return c.objects_foreground[pos.y][pos.x]
    
    def get_background_Obj(self, pos:Vec) ->Obj:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        return c.background_obj[pos.y][pos.x]

    def remove_entity(self, entity : Npc):
        chunk = self.get_Chunk_from_pos(entity.pos)
        if entity in chunk.entities:
            chunk.entities.remove(entity)

    def remove_obj_at(self, pos: Vec):
        self.get_Chunk_from_pos(pos).objects[pos.y][pos.x] = Objs["Air"]

    def get_dyn_Obj(self, pos:Vec) -> Obj:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        return c.dyn_objects[pos.y][pos.x]
    def get_dyn_Obj_fore(self, pos:Vec) -> Obj:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        return c.dyn_objects_foreground[pos.y][pos.x]

    def on_load(self):
        for i in events[Event_on_world_load]:
            i.function(players, self)

    def spawn_item(self, item : items.Item, pos : Vec):
        i = Npcs["Item_entity"](pos)
        i.item = item
        i.current_texture = item.texture
        self.add_entity(i)

    def get_chunks_to_render(self, pos : Vec) -> list[Chunk]:
        res = [None for i in range(9)]
        res_end = 0
        pos2 = pos // CHUNK_SIZE
        for x in range(-1, 2):
            for y in range(-1, 2):
                res[res_end] = self.get_Chunk_at(pos2 + (x, y))
                res_end += 1
        return res


    def show(self, screen:pygame.Surface, zoom_out: int) -> None:
        """
        display everything that has to be rendered on the screen
        """
        __bg_obj : list[tuple[int, int, Obj]] = []
        __objects : list[tuple[int, int, Obj]] = []
        __fore_objects : list[tuple[int, int, Obj]] = []
        __dyn_obj : list[tuple[int, int, Obj]] = []
        __fore_dyn_obj : list[tuple[int, int, Obj]] = []
        __players : list[Character] = [players[i] for i in range(1,len(players))]#get players except user
        __entities : list[Npc] = []
        __chunks : list[Chunk] = self.get_chunks_to_render(players[0].pos)
        x = (players[0].pos // CHUNK_SIZE).x
        y = (players[0].pos // CHUNK_SIZE).y
        
        scr_w = screen.get_width()
        scr_h = screen.get_height()
        new_texture = get_time_layout(players[0].tick_count, self.is_outside)

        screen.fill(self.bg)


        #get everythings form the chunks
        for c in __chunks:
            __entities.extend(c.entities)
            for i in range(0, CHUNK_SIZE, OBJ_SIZE):
                for k in range(0, CHUNK_SIZE, OBJ_SIZE):
                    __bg_obj.append((i + c.top_left_pos.x, k + c.top_left_pos.y, c.background_obj[k // OBJ_SIZE][i // OBJ_SIZE]))
                    __objects.append((i + c.top_left_pos.x, k + c.top_left_pos.y, c.objects[k // OBJ_SIZE][i // OBJ_SIZE]))
                    __fore_objects.append((i + c.top_left_pos.x, k + c.top_left_pos.y, c.objects_foreground[k // OBJ_SIZE][i // OBJ_SIZE]))
                    __dyn_obj.append((i + c.top_left_pos.x, k + c.top_left_pos.y, c.dyn_objects[k // OBJ_SIZE][i // OBJ_SIZE]))
                    __fore_dyn_obj.append((i + c.top_left_pos.x, k + c.top_left_pos.y, c.dyn_objects_foreground[k // OBJ_SIZE][i // OBJ_SIZE]))

        __offset = Vec(scr_w // 2, scr_h // 2) - players[0].pos - Vec(players[0].current_texture.get_width() // 2, players[0].current_texture.get_height() // 2)

        #draw background objects
        for i in __bg_obj:
            if i[2].id != "Air":
                p = (i[0], i[1]) + __offset
                if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                    screen.blit(i[2].texture,tuple(p))
                    i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                else:
                    i[2].on_draw(self,False, Vec(i[0], i[1]), p)
       #
        #draw objects that are not toplayer
        for i in __objects:
            if i[2].id != "Air":
                if not i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))

        for i in __fore_objects:
            if i[2].id != "Air":
                if not i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))

        for i in __dyn_obj:
            if i[2].id != "Air":
                if not i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))
        for i in __fore_dyn_obj:
            if i[2].id != "Air":
                if not i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))

        #draw user
        if players[0].isvisible and not players[0].is_world_editor:
            if not players[0].riding:
                p = players[0].pos + __offset
                screen.blit(players[0].current_texture, tuple(p))
                players[0].on_draw(self, True)
            else:
                p = players[0].pos + __offset

                screen.blit(players[0].riding.current_texture, tuple(p))
                screen.blit(players[0].current_texture,tuple(p + players[0].riding.rider_offset + (players[0].riding.current_texture.get_width()//2 - players[0].current_texture.get_width()//2 ,-players[0].current_texture.get_height())))

        #draw other players
        for i in __players:
            p = i.pos + __offset
            if -i.current_texture.get_width() <= p.x < scr_w and -i.current_texture.get_height() <= p.y < scr_h:
                screen.blit(i.current_texture, tuple(p))
                i.on_draw(self, True, Vec(i[0], i[1]))
            else:
                i.on_draw(self, False, Vec(i[0], i[1]))

        #draw entities
        for i in __entities:
            p = i.pos + __offset
            if -i.current_texture.get_width() <= p.x < scr_w and -i.current_texture.get_height() <= p.y < scr_h:
                screen.blit(i.current_texture, tuple(p + i.texture_pos))
                i.on_draw(self, True, Vec(i[0], i[1]), p)
            else:
                i.on_draw(self, False, Vec(i[0], i[1]), p)

        #draw objects that are toplayer
        for i in __objects:
            if i[2].id != "Air":
                if i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))

        for i in __fore_objects:
            if i[2].id != "Air":
                if i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))

        for i in __dyn_obj:
            if i[2].id != "Air":
                if i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))
        for i in __fore_dyn_obj:
            if i[2].id != "Air":
                if i[2].toplayer:
                    p = (i[0], i[1]) + __offset
                    if -i[2].texture.get_width() <= p.x < scr_w and -i[2].texture.get_height() <= p.y < scr_h:
                        screen.blit(i[2].texture,tuple(p))
                        i[2].on_draw(self,True, Vec(i[0], i[1]), p)
                    else:
                        i[2].on_draw(self,False, Vec(i[0], i[1]), p)
                    if i[2].light:
                        p = i[2].light.pos + __offset + (i[0], i[1])
                        if -i[2].light.texture.get_width() <= p.x < scr_w and -i[2].light.texture.get_height() <= p.y < scr_h:
                            new_texture.blit(i[2].light.texture,tuple(p))
        
        screen.blit(new_texture, (0,0))

        #draw hitboxes if theyre are visible
        if show_hitbox:
            for i in __chunks:
                for k in i.hitboxes:
                    s=py.Surface((k.width, k.height))
                    s.fill((0, 255, 0))
                    s.set_alpha(50)
                    screen.blit(s, tuple(k.pos + __offset))
        
        #draw chunk borders if the player can see them
        if players[0].chunk_border:
            for i in __chunks:
                corn=i.get_borders()

                py.draw.line(screen, (255, 0, 0), tuple(corn[0] + __offset), tuple(corn[1] + __offset))
                py.draw.line(screen, (255, 0, 0), tuple(corn[2] + __offset), tuple(corn[3] + __offset))
                py.draw.line(screen, (255, 0, 0), tuple(corn[0] + __offset), tuple(corn[2] + __offset))
                py.draw.line(screen, (255, 0, 0), tuple(corn[1] + __offset), tuple(corn[3] + __offset))

    def update(self) -> int :
        """
        called each game tick so ~150 times a second (int theory)
        if world.has_to_collide is set to true the collision will be computed
        and has_to_collide will be set to false
        
        if the player is dead(pv <=0) the function will return 1
        """
        chunks : list[Chunk] = []
        distance =players[0].render_distance // 2 + 1
        chunk_pos = players[0].pos // CHUNK_SIZE
        for i in range(-distance + 1, distance):
            for k in range(-distance + 1, distance):
                chunks.append(self.get_Chunk_at((i, k) + chunk_pos))


        for i in chunks:
            i.tick()
            
        __dyn_objs : list[Obj] = []
        __entities : list[Npc] = []

        for i in chunks:
            __entities.extend(i.entities)
            for a in i.dyn_objects:
                __dyn_objs.extend(a)
            for a in i.dyn_objects_foreground:
                __dyn_objs.extend(a)


        p = 0
        while p < len(__entities):
            if __entities[p].pv <= 0:
                if __entities[p].die(self):
                    self.remove_entity(__entities[p])
                    __entities.pop(p)
                    continue
            p += 1
    
        for i in __entities:
            if i.tick:
                i.tick(self)
        if players[0].riding:
            players[0].riding.tick(self)

        for i in __dyn_objs:
            i.tick(self)
        players[0].tick()

        self.has_to_collide = False
        if players[0].riding:
            players[0].pos = players[0].riding.pos
            players[0].riding.world = players[0].world
        return 0

    def remove_background_Obj(self, pos : Vec) -> None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.background_obj[pos.y][pos.x] = default_air
    def remove_Obj(self, pos : Vec) -> None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.objects[pos.y][pos.x] = default_air
    def remove_foreground_Obj(self, pos : Vec) -> None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.objects_foreground[pos.y][pos.x] = default_air
    def remove_Dyn_Obj(self, pos : Vec) -> None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.dyn_objects[pos.y][pos.x] = default_air
    def remove_foreground_Dyn_Obj(self, pos : Vec) -> None:
        c = self.get_Chunk_from_pos(pos)
        pos = (pos - c.top_left_pos)// OBJ_SIZE
        c.dyn_objects_foreground[pos.y][pos.x] = default_air
    
    def walk_in_at(self, player, pos: Vec):
        self.get_background_Obj(pos).on_walk_in(self, player, pos)
        self.get_Obj(pos).on_walk_in(self, player, pos)
        self.get_Obj_fore(pos).on_walk_in(self, player, pos)
        self.get_dyn_Obj(pos).on_walk_in(self, player, pos)
        self.get_dyn_Obj_fore(pos).on_walk_in(self, player, pos)

def newChunk(pos:Vec,world:World) -> Chunk:
    return Chunk(pos,world)

def newWorld(name:str,background_color:list[int]=(0,0,0)):
    return World(name,background_color)

def toggle_hitbox():
    global show_hitbox
    show_hitbox = not show_hitbox
    
def get_time_layout(tick : int, outside : bool):
    if not outside or tick <= 54000 or tick >= 108000:
        return NOTHING_TEXTURE_1024_576.copy()
    if tick > 54000 and tick < 64000:
        new_texture = Textures["other"]["night_layout"].copy()
        new_texture.set_alpha(int(25.5 * tick / 1000 - 1377))
    elif tick >= 64000 and tick <= 98000:
        new_texture = Textures["other"]["night_layout"].copy()
    elif tick > 98000:
        new_texture = Textures["other"]["night_layout"].copy()
        new_texture.set_alpha(int(-25.5 * tick / 1000 + 2754))
    else:
        new_texture = NOTHING_TEXTURE_1024_576.copy()
    return new_texture
