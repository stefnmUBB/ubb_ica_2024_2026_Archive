import multiprocessing

from src.agents.dummy_player.dummy_player import DummyPlayerAgent
from src.agents.moderator.agent import ModeratorAgent
from src.agents.player import PlayerAgent
from src.agents.random_player import RandomPlayerAgent
from src.agents.tactical_player.tactical_player import TacticalPlayerAgent
from src.blackboard import Blackboard
from src.environment import GameEnvironment
from src.map import GameMap
from src.render_engines import PygameRenderEngine
from src.simulations.game_simulation import GameSimulation
from src.state import GameState


def run_simulation():
    render_engine = PygameRenderEngine(clock_tick=200, sleep_between_simulations=0.001)
    blackboard = Blackboard()
    game_map = GameMap.from_file("maps/level_tactical.txt")
    agents = [
        *[
            (
                RandomPlayerAgent(player_id=player_id, blackboard=blackboard)
                if data.team == "R"
                else (
                    DummyPlayerAgent(player_id=player_id, blackboard=blackboard)
                    if data.team == "Y"
                    else (
                        TacticalPlayerAgent(player_id=player_id, blackboard=blackboard)
                        if data.team == "B"
                        else PlayerAgent(player_id=player_id, blackboard=blackboard)
                    )
                )
            )
            for player_id, data in game_map.players.items()
        ],
        ModeratorAgent(blackboard=blackboard, probability=0.5),
    ]
    initial_state = GameState(map=game_map)
    simulation = GameSimulation(
        agents=agents,
        env=GameEnvironment(state=initial_state),
        render_engine=render_engine,
        max_simulations=750,
    )
    simulation.start()


if __name__ == "__main__":
    processes = []
    for _ in range(1):
        p = multiprocessing.Process(target=run_simulation)
        p.start()
        processes.append(p)
