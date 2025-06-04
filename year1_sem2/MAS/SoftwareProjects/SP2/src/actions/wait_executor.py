from src.agents.player import PlayerAgent
from src.interfaces import ExecutableAction
from src.state import GameState
from src.utils import ActionExecutorFactory

from .actions import WaitAction


class WaitExecutor(ExecutableAction):
    def execute(self, agent: PlayerAgent, state: GameState) -> GameState:
        return state


ActionExecutorFactory.register(WaitAction, WaitExecutor)
