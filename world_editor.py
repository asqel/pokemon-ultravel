#Hogwarts Legacy en version pétée by Léa et Asqel
import pygame as py
from pygame.locals import *

from uti.textures import *
from uti.sound import play_sound
from entities import *
from events import *
from time import time, sleep
from world import *

from _thread import start_new_thread

py.joystick.init()
py.font.init()

FPS_MAX = 60
TPS_MAX = 150

MOD_ENABLED = True


global g_tps, running_dict 
g_tps = 0

running_dict = {
    "global": True,
    "graphic": True,
    "server": True
}

pygame_events=[]
    
place_type = 0
place_type_str = [
    "background object",
    "object",
    "foreground object",
    "dynamics object",
    "foreground dynamics object"
]

def server_thread():
    global running_dict, g_tps, pygame_events, show_hitbox, obj_idx, place_type

    loop_start = time()
    loop_count = 0
    cooldown=10

    while running_dict["global"]:
        iter_start = time()
        loop_count += 1

        if players[0].guis:
            result = players[0].guis[-1].tick(pygame_events)
            pygame_events = []
            if result == "end_game":
                running_dict["global"] = False
        for i in pygame_events:
            if i.type == py.QUIT:
                running_dict["global"] = False
            if not players[0].guis:
                if i.type == py.KEYDOWN:
                    if i.key == K_SPACE:
                        players[0].chunk_border=not players[0].chunk_border
                    elif i.key == K_ASTERISK:
                        toggle_hitbox()
                    if i.key == K_LEFT:
                        obj_idx-=1
                        if obj_idx==-1:
                            obj_idx=len(Objs.keys())-1
                    if i.key == K_RIGHT:
                        obj_idx+=1
                        if obj_idx == len(Objs.keys()):
                            obj_idx=0
                    if i.key == K_DOWN:
                        place_type +=1
                        if place_type == 5:
                            place_type = 0
                    if i.key == K_UP:
                        place_type -=1
                        if place_type == -1:
                            place_type = 4
                    if i.key == K_p:
                        place_obj(obj_idx, players[0].pos, place_type, starting_world)
                    if i.key == K_o:#delete obj att
                        remove_obj(players[0].pos, place_type, starting_world)
                    if i.key == K_l:
                        for x in range(4):
                            for y in range(4):
                                place_obj(obj_idx, players[0].pos + Vec(x, y) * TILE_SIZE, place_type, starting_world)
                elif i.type ==py.KEYUP:
                    if i.key == py.K_LCTRL:
                        players[0].speed=0.5  
                
        pygame_events=[]
        
        if not players[0].guis:
            pushed_keys=py.key.get_pressed()
            if pushed_keys[py.K_a] and not cooldown:
                players[0].pos.x -= TILE_SIZE
                cooldown=20
                
            if pushed_keys[py.K_d] and not cooldown:
                players[0].pos.x += TILE_SIZE
                cooldown=20
                
            if pushed_keys[py.K_w] and not cooldown:
                players[0].pos.y -= TILE_SIZE
                cooldown=20
                
            if pushed_keys[py.K_s] and not cooldown and not pushed_keys[py.K_LCTRL]:
                players[0].pos.y += TILE_SIZE
                cooldown=20
            if cooldown:
                cooldown-=1
            
            
            if pushed_keys[py.K_LCTRL] and pushed_keys[py.K_s] and not cooldown:
                cooldown = 50
                js.save_world(starting_world)
                print("world have been saved")

        # tps moyenizer
        moy_fps = 1 / (time() - loop_start) * loop_count if loop_count > 10 else TPS_MAX
        to_sleep = (1 / TPS_MAX - (time() - iter_start)) - (1 - (moy_fps / TPS_MAX))
        if to_sleep > 0: sleep(to_sleep)

        g_tps = 1 / (time() - loop_start) * loop_count

    running_dict["server"] = False

def main():
    
    global pygame_events
    for i in events[Event_on_textures_load_t]:
        i.function(Textures)

    players[0].zoom_out = 1
    players[0].render_distance=3

    start_new_thread(server_thread, ())

    arial=py.font.SysFont("Arial",25,False,False)
    fps = 0
    cursor_cooldown=0
    while running_dict["global"] and running_dict["graphic"] and running_dict["server"]:
        start_time = time()
        pygame_events=py.event.get()
        for i in pygame_events:
            if i.type == py.QUIT:
                running_dict["global"]=False
        
                
        players[0].world: World = players[0].world
        players[0].world.show(screen, players[0].zoom_out)
 
        screen.blit(arial.render(f"fps: {int(fps)}", False, (255, 0, 0)), (0, 0))
        screen.blit(arial.render(f"mid tps: {int(g_tps)}", False, (255, 0, 0)), (0, 30))
        screen.blit(arial.render(str(players[0].pos.floor()), False, (255, 0, 0)), (0, 60))
        screen.blit(arial.render(str(players[0].world.get_Chunk_from_pos(players[0].pos).pos), False, (255, 0, 0)), (0, 90))
        screen.blit(arial.render(place_type_str[place_type], False, (255, 0, 0)), (0, 120))

        #draw crusor
        if cursor_cooldown:
            cursor_cooldown-=1
        if 0<cursor_cooldown<=30: # draw obj
            texture=Objs[list(Objs.keys())[obj_idx]]().texture
            s=py.Surface((texture.get_width(), texture.get_height()))
            s.blit(texture,(0,0))
            s.set_alpha(100)
            screen.blit(s,(screen.get_width()//2-TILE_SIZE//2,screen.get_height()//2-TILE_SIZE//2))

        if not cursor_cooldown:
            cursor_cooldown=40

        if players[0].guis:
                players[0].guis[-1].draw(screen)
        display_screen.fill((0,0,0))
        display_screen_width, display_screen_height = display_screen.get_size()

        # Calculer les dimensions ajustées de l'affichage de screen
        scale_factor_width = display_screen_width / screen.get_width()
        scale_factor_height = display_screen_height / screen.get_height()
        scale_factor = min(scale_factor_width, scale_factor_height)

        adjusted_width = int(screen.get_width() * scale_factor)
        adjusted_height = int(screen.get_height() * scale_factor)

        x_offset = (display_screen_width - adjusted_width) // 2
        y_offset = (display_screen_height - adjusted_height) // 2

        # Redimensionner l'écran en conservant le rapport de hauteur/largeur
        scaled_screen = pygame.transform.scale(screen, (adjusted_width, adjusted_height))

        # Dessiner le contenu de scaled_screen sur display_screen
        display_screen.fill((0, 0, 0))  # Remplir display_screen avec du noir
        display_screen.blit(scaled_screen, (x_offset, y_offset))
        py.display.update()
        t=time()
        if  t - start_time <1/60:
            sleep(1/60 -t+start_time)
        fps = 1/(time()-start_time)


import jsonizer as js
import os
if MOD_ENABLED:
        import modloader as md
        md.load_mods()
world_name = input("entrez le nom du monde : ")
if not js.world_exists(world_name, ""):
    print("le monde nexiste pas et vas etre creer")
starting_world = World(world_name, (0,0,0))


starting_world.has_to_collide=True



players.append(Character(0, 0, starting_world))
players[0].is_world_editor = True
obj_idx=0
def place_obj(obj_idx : int, pos : Vec, place_type : int, w : World) -> None:
    match place_type:
        case 0:
            w.add_background_Obj(Objs[list(Objs.keys())[obj_idx]](), pos)
        case 1:
            w.add_Obj(Objs[list(Objs.keys())[obj_idx]](), pos)
        case 2:
            w.add_foreground_Obj(Objs[list(Objs.keys())[obj_idx]](), pos)
        case 3:
            w.add_Dyn_Obj(Objs[list(Objs.keys())[obj_idx]](), pos)
        case 4:
            w.add_foreground_Dyn_Obj(Objs[list(Objs.keys())[obj_idx]](), pos)

def remove_obj(pos : Vec, place_type : int, w : World) -> None:
    match place_type:
        case 0:
            w.remove_background_Obj(pos)
        case 1:
            w.remove_Obj(pos)
        case 2:
            w.remove_foreground_Obj(pos)
        case 3:
            w.remove_Dyn_Obj(pos)
        case 4:
            w.remove_foreground_Dyn_Obj(pos)

main()
"""
au demarrage dans console le nom du monde est demander 
si le monde est deja dans worlds/ alors il sera charger
sinon un nouveau sera creer

ctrl+S pour enregistrer le monde

space pour afficher les bordure de chunk

fleche droite et gauche pour changer d'objet

les objet ajouter sont ajouter la ou vous etes

p pour ajouter un obj
o pour enlver un obj

m pour ajouter un obj au background
l pour enlever un obj au background

i pour faire un carre de 4x4 d'obj
k pour faire un carre de 4x4 d'obj de background
    
"""


