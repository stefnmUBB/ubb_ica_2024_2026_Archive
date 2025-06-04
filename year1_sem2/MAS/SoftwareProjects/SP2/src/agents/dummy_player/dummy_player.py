import random
from src.actions import (
    PlayerAction,
    WaitAction,
    ForwardAction,
    TurnLeftAction,
    ShootAction,
    TurnRightAction,
)
from src.constants import PLAYER_NUM_RAYS
from src.objects import GameObject

from ..player import PlayerAgent


class DummyPlayerAgent(PlayerAgent):
    def _check_wall(self):
        if random.random() < 0.7 and any(
            [
                ray.obj == GameObject.WALL and ray.distance < 0.2
                for ray in self.current_percept.rays
            ]
        ):
            return TurnLeftAction()
        return None

    def _check_enemy(self):
        for ray_idx, ray in enumerate(self.current_percept.rays):
            if ray.obj != GameObject.ENEMY:
                continue
            elif ray_idx <= PLAYER_NUM_RAYS // 2 - 5:
                return TurnLeftAction()
            elif ray_idx >= PLAYER_NUM_RAYS // 2 + 5:
                return TurnRightAction()
            else:
                return ShootAction(angle=ray.direction.base_angle())
        return None

    def _select_raw_action(self) -> PlayerAction:
        if action := self._check_enemy():
            return action

        if action := self._check_wall():
            return action

        p = random.random()
        if p < 0.85:
            return ForwardAction()
        elif p < 0.95:
            return TurnLeftAction()
        else:
            return WaitAction()
