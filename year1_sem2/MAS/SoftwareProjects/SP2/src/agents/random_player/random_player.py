import random
from src.actions import (
    PlayerAction,
    WaitAction,
    ForwardAction,
    TurnLeftAction,
    TurnRightAction,
    ShootAction,
)
from src.constants import PLAYER_SHOOTING_FOV

from ..player import PlayerAgent


class RandomPlayerAgent(PlayerAgent):
    def _select_raw_action(self) -> PlayerAction:
        possible_actions = [
            WaitAction(),
            ForwardAction(),
            TurnLeftAction(),
            TurnRightAction(),
            ShootAction(
                angle=random.uniform(-PLAYER_SHOOTING_FOV / 2, PLAYER_SHOOTING_FOV / 2)
            ),
        ]

        action = random.choice(possible_actions)
        return action
