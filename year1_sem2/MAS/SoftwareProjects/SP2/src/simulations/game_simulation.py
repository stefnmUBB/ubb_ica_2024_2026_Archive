from .base_simulation import BaseSimulation
from src.environment import GameEnvironment


class GameSimulation(BaseSimulation):
    env: GameEnvironment
    max_simulations: int = 500

    def is_complete(self) -> bool:
        if self.env.state.tick >= self.max_simulations:
            return True

        alive_teams = set()
        for agent_stats in self.env.state.agent_stats.values():
            if not agent_stats.is_alive or agent_stats.map_data.team in alive_teams:
                continue
            if len(alive_teams) >= 1:
                return False
            alive_teams.add(agent_stats.map_data.team)
        return True
