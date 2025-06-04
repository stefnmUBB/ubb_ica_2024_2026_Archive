import time

import pygame
import math

from src.interfaces.render_engine import RenderEngine
from src.objects import WALL_SIZE, PLAYER_DIAMETER
from src.simulations.exceptions import StopSimulationException
from src.state import GameState
from src.constants import (
    PLAYER_VIEW_FOV,
    PLAYER_NUM_RAYS,
    PLAYER_RAY_LENGTH,
    PLAYER_SHOOTING_LENGTH_PER_TICK,
)
from src.geometry import Vector2D


class PygameRenderEngine(RenderEngine):
    CELL_SIZE = 40
    COLORS = {
        "background": (200, 255, 200),
        "wall": (0, 0, 0),
        "empty": (255, 255, 255),
        "dead": (100, 100, 100),
        "team_r": (255, 0, 0),
        "team_y": (255, 200, 0),
        "team_g": (0, 255, 120),
        "team_b": (0, 120, 255),
        "ray_wall": (0, 0, 255),
        "ray_agent": (255, 0, 255),
        "ray_none": (0, 255, 0),
        "shoot_ray": (255, 50, 50),
    }

    def __init__(self, clock_tick: int = 50, sleep_between_simulations: float = 0.05):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.paused = False
        self.clock_tick = clock_tick
        self.sleep_between_simulations = sleep_between_simulations

    def display(self, state: GameState):
        self._setup_screen(state)
        self._draw_grid(state)
        self._draw_walls(state)
        self._draw_agents(state)
        self._draw_rays(state)
        self._draw_tick(state)
        self._draw_shots(state)
        pygame.display.flip()
        self.clock.tick(self.clock_tick)
        self._listen_events()

        while self.paused:
            self._listen_events()
            self.clock.tick(5)

        time.sleep(self.sleep_between_simulations)

    def _setup_screen(self, state: GameState):
        width = state.map.width * self.CELL_SIZE
        height = state.map.height * self.CELL_SIZE + 30
        if self.screen is None:
            self.screen = pygame.display.set_mode((width, height))
        self.screen.fill(self.COLORS["background"])

    def _coord_to_px(self, x: float | int, y: float | int):
        return int(x * self.CELL_SIZE + self.CELL_SIZE / 2), int(
            y * self.CELL_SIZE + self.CELL_SIZE / 2
        )

    def _draw_grid(self, state: GameState):
        for x in range(state.map.width):
            for y in range(state.map.height):
                rect = pygame.Rect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE,
                    self.CELL_SIZE * WALL_SIZE,
                    self.CELL_SIZE * WALL_SIZE,
                )
                pygame.draw.rect(self.screen, self.COLORS["empty"], rect)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def _draw_walls(self, state: GameState):
        for wall in state.map.walls:
            rect = pygame.Rect(
                int(wall.x * self.CELL_SIZE),
                int(wall.y * self.CELL_SIZE),
                self.CELL_SIZE,
                self.CELL_SIZE,
            )
            pygame.draw.rect(self.screen, self.COLORS["wall"], rect)

    def _draw_agents(self, state: GameState):
        for player_id in state.agent_stats.keys():
            agent_stats = state.agent_stats[player_id]

            if not agent_stats.is_alive:
                color = self.COLORS["dead"]
            else:
                color = self.COLORS.get(
                    f"team_{agent_stats.map_data.team.lower()}", (255, 0, 0)
                )

            pygame.draw.circle(
                self.screen,
                color,
                self._coord_to_px(
                    agent_stats.map_data.position.x, agent_stats.map_data.position.y
                ),
                (self.CELL_SIZE * PLAYER_DIAMETER) // 2,
            )

    def _draw_rays(self, state: GameState):
        for player_id, agent_stats in state.agent_stats.items():
            if not agent_stats.is_alive or len(agent_stats.rays) == 0:
                continue

            origin = agent_stats.map_data.position
            direction = agent_stats.map_data.direction
            if direction is None:
                continue

            base_angle = direction.base_angle()
            start_angle = base_angle - (PLAYER_VIEW_FOV / 2)
            angle_step = PLAYER_VIEW_FOV / (PLAYER_NUM_RAYS - 1)

            for i, ray in enumerate(agent_stats.rays):
                angle = start_angle + i * angle_step
                dx = math.cos(math.radians(angle))
                dy = math.sin(math.radians(angle))
                ray_direction = Vector2D(x=dx, y=dy)

                hit_pos = origin + ray_direction * (ray.distance * PLAYER_RAY_LENGTH)

                if ray.obj.name == "WALL":
                    color = self.COLORS["ray_wall"]
                elif ray.obj.name in ("ENEMY", "TEAMMATE"):
                    color = self.COLORS["ray_agent"]
                else:
                    color = self.COLORS["ray_none"]

                pygame.draw.line(
                    self.screen,
                    color,
                    self._coord_to_px(origin.x, origin.y),
                    self._coord_to_px(hit_pos.x, hit_pos.y),
                    2,
                )

    def _draw_shots(self, state: GameState):
        for shot in state.pending_shots:
            origin = shot.origin
            direction = shot.direction
            end = origin + direction * PLAYER_SHOOTING_LENGTH_PER_TICK

            pygame.draw.line(
                self.screen,
                self.COLORS["shoot_ray"],
                self._coord_to_px(origin.x, origin.y),
                self._coord_to_px(end.x, end.y),
                4,  # thickness
            )

    def _draw_tick(self, state: GameState):
        tick_text = self.font.render(f"Tick: {state.tick}", True, (0, 0, 0))
        self.screen.blit(tick_text, (5, state.map.height * self.CELL_SIZE + 5))

    def _listen_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise StopSimulationException()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

    def stop(self):
        self.paused = True
        while self.paused:
            self._listen_events()
            self.clock.tick(50)
        pygame.display.quit()
        pygame.quit()
