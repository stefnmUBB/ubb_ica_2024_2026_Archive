from src.agents.player import PlayerAgent
from src.constants import PLAYER_ROTATE_DEGREES
from src.geometry import Vector2D, closest_vec_multiple_angle
from src.interfaces import ExecutableAction
from src.state import GameState
from src.utils import ActionExecutorFactory

from .actions import TurnLeftAction, TurnRightAction


class TurnLeftExecutor(ExecutableAction):
    def execute(self, agent: PlayerAgent, state: GameState) -> GameState:
        return self._rotate(agent, state, -PLAYER_ROTATE_DEGREES)

    def _rotate(self, agent: PlayerAgent, state: GameState, angle: float):
        player_stats = state.agent_stats[agent.player_id]
        if player_stats.map_data.direction:
            current_angle = player_stats.map_data.direction.base_angle()
            new_angle = current_angle + angle
            player_stats.map_data.direction = closest_vec_multiple_angle(
                Vector2D.from_angle(new_angle), PLAYER_ROTATE_DEGREES
            )
        return state


class TurnRightExecutor(TurnLeftExecutor):
    def execute(self, agent: PlayerAgent, state: GameState) -> GameState:
        return self._rotate(agent, state, PLAYER_ROTATE_DEGREES)


ActionExecutorFactory.register(TurnLeftAction, TurnLeftExecutor)
ActionExecutorFactory.register(TurnRightAction, TurnRightExecutor)
