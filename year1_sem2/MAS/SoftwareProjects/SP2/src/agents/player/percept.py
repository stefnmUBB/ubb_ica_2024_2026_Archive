from src.objects import Ray
from src.interfaces.percept import Percept


class PlayerPercept(Percept):
    rays: list[Ray]
