from src.agents.player import PlayerAgent
from src.geometry import Vector2D
from src.interfaces import ExecutableAction
from src.state import GameState, PendingShot

from .actions import ShootAction
from ..constants import PLAYER_SHOOTING_DELAY_TICKS
from ..utils import ActionExecutorFactory


class ShootExecutor(ExecutableAction):
    def execute(self, agent: PlayerAgent, state: GameState) -> GameState:
        stats = state.agent_stats[agent.player_id]
        if not stats.is_alive or stats.shooting_delay > 0:
            return state

        origin = stats.map_data.position
        if not stats.map_data.direction:
            return state

        base_angle = stats.map_data.direction.base_angle()
        shot_angle = base_angle + self.action.angle
        direction = Vector2D.from_angle(shot_angle)

        state.pending_shots.append(
            PendingShot(player_id=agent.player_id, origin=origin, direction=direction)
        )
        stats.shooting_delay = PLAYER_SHOOTING_DELAY_TICKS
        return state


ActionExecutorFactory.register(ShootAction, ShootExecutor)
