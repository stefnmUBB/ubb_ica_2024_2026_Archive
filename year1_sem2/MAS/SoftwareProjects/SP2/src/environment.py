from .actions import PlayerAction
from .agents.moderator import ModeratorAgent, ModeratorPercept
from .agents.player import PlayerAgent, PlayerPercept
from .interfaces import Environment, Agent, Action, Percept
from .state import GameState
from .utils import ActionExecutorFactory


class GameEnvironment(Environment):
    state: GameState

    def get_percept(self, agent: Agent) -> Percept:
        if isinstance(agent, PlayerAgent):
            stats = self.state.agent_stats[agent.player_id]
            return PlayerPercept(rays=stats.rays)
        elif isinstance(agent, ModeratorAgent):
            return ModeratorPercept(agent_stats=self.state.agent_stats)
        raise ValueError("Unsupported agent type")

    def update_state(self, agent: Agent, action: Action) -> None:
        if isinstance(action, PlayerAction):
            executor = ActionExecutorFactory.get_executor(action)
            self.state = executor.execute(agent, self.state)

    def step(self) -> None:
        self.state.step()
