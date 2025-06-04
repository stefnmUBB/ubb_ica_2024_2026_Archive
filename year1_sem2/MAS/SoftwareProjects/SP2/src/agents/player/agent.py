from abc import ABC
from collections import deque

from src.actions import PlayerAction, WaitAction
from src.constants import PLAYER_LAST_ACTIONS_LEN, VERBOSE
from src.geometry import Vector2D

from .percept import PlayerPercept
from ..communication_agent import CommunicationAgent


class PlayerAgent(CommunicationAgent, ABC):
    player_id: str
    last_actions: deque[PlayerAction] = deque(maxlen=PLAYER_LAST_ACTIONS_LEN)
    current_percept: PlayerPercept | None = None
    current_message: Vector2D | None = None

    def init(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(PLAYER_LAST_ACTIONS_LEN):
            self.last_actions.append(WaitAction())

    def see(self, percept: PlayerPercept):
        self.current_percept = percept
        message = self.blackboard.read(self.player_id)
        if message is not None:
            if VERBOSE:
                print(f"[AGENT {self.player_id}]: Received message: {message}")
            self.current_message = message

    def _choose_action(self, action: PlayerAction) -> PlayerAction:
        self.current_percept = None
        self.last_actions.append(action)
        return action

    def _select_raw_action(self) -> PlayerAction:
        return WaitAction()

    def select_action(self) -> PlayerAction:
        return self._choose_action(self._select_raw_action())
