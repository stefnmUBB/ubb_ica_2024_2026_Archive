from src.actions import (
    PlayerAction,
    ForwardAction,
    TurnLeftAction,
    TurnRightAction,
)
from src.constants import PLAYER_ROTATE_DEGREES, VERBOSE
from src.geometry import Vector2D

from ..dummy_player import DummyPlayerAgent


class TacticalPlayerAgent(DummyPlayerAgent):
    timeout_counter: int = 0

    def _check_repetition(self):
        if len(self.last_actions) < 4:
            return

        if (
            type(self.last_actions[-1]) == TurnLeftAction
            and type(self.last_actions[-2]) == TurnRightAction
            and type(self.last_actions[-3]) == TurnLeftAction
            and type(self.last_actions[-4]) == TurnRightAction
        ):
            self.timeout_counter = 50
            if VERBOSE:
                print(
                    f"[{self.player_id}]: Detected repeated actions, resetting timeout."
                )
            return

    def _pursue_enemy(self):
        if not isinstance(self.current_message, Vector2D):
            return None

        angle = self.current_message.base_angle()
        angle_threshold = PLAYER_ROTATE_DEGREES * 1.5

        if abs(angle) <= angle_threshold:
            return ForwardAction()
        elif angle < 0:
            return TurnLeftAction()
        else:
            return TurnRightAction()

    def _select_raw_action(self) -> PlayerAction:
        if self.timeout_counter > 0:
            self.timeout_counter -= 1
            return super()._select_raw_action()

        self._check_repetition()

        if action := self._check_enemy():
            return action

        if action := self._check_wall():
            return action

        if action := self._pursue_enemy():
            return action

        return ForwardAction()
