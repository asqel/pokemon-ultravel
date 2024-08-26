from items import *
from uti import *


class Air(Item):
    def __init__(self, quantity) -> None:
        super().__init__(self.__class__.__name__, 3, NOTHING_TEXTURE, quantity)

    def get_display_name(self) -> str:
        return "Air"



registerItem(Air)