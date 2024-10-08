import pygame as py
from uti import Vec
from sys import exit

class Animation:

    def __init__(self, textures : list[py.Surface], delay : int = 0, pos : Vec = None) -> None:
        """
        textures: frames of the animation
        delay: delay in game tick between each frames
        """
        if not self.textures:
            print("ERROR in Animation no frames")
            exit(1)

        self.textures = textures
        self.delay = delay
        self.delay_count = 0
        self.current = 0
        self.pos = pos.copy() if pos else Vec(0,0)

    def get_current_frame(self):
        return self.textures[self.current]

    def next_frame(self):
        self.delay_count += 1
        if self.delay_count > self.delay:
            self.current += 1
            self.delay_count = 0

        if self.current >= len(self.textures):
            self.current = 0            