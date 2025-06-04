from src.map import PlayerID
from src.interfaces.percept import Percept
from src.state import AgentStats


class ModeratorPercept(Percept):
    agent_stats: dict[PlayerID, AgentStats]
