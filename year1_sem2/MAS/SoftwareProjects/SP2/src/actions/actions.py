from abc import ABC

from src.interfaces import Action


class PlayerAction(Action, ABC):
    pass


class ForwardAction(PlayerAction):
    pass


class TurnLeftAction(PlayerAction):
    pass


class TurnRightAction(PlayerAction):
    pass


class ShootAction(PlayerAction):
    angle: float = 0


class WaitAction(PlayerAction):
    pass
