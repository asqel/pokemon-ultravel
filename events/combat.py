from pygame.event import Event
from interface import *
import pygame as py



class combat_gui(Gui):
	def __init__(self, player, pk1 = None, pk2 = None, enemy_trainer = None) -> None:
		super().__init__("combat_gui", {}, player)
		self.pk1 = pk1
		self.pk2 = pk2
		self.enemy_trainer = enemy_trainer

	def tick(self, events: list[Event]):
		...
	def draw(self, screen : py.Surface):
		py.draw.circle(screen, (255,0,255), (0,0), 500)



registerGui(combat_gui)