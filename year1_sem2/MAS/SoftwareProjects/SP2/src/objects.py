from enum import IntEnum

from pydantic import BaseModel

from src.geometry import Vector2D


class GameObject(IntEnum):
    NONE = 0
    WALL = 1
    TEAMMATE = 2
    ENEMY = 3


WALL_SIZE = 1
PLAYER_DIAMETER = 0.8


class CollisionDetector:
    @classmethod
    def check_collision_point_wall(cls, point: Vector2D, wall: Vector2D) -> bool:
        return (
            wall.x - WALL_SIZE / 2 < point.x < wall.x + WALL_SIZE / 2
            and wall.y - WALL_SIZE / 2 < point.y < wall.y + WALL_SIZE / 2
        )

    @classmethod
    def check_collision_point_player(cls, point: Vector2D, player: Vector2D) -> bool:
        return (player - point).length() < PLAYER_DIAMETER / 2

    @classmethod
    def check_collision_player_wall(cls, player: Vector2D, wall: Vector2D) -> bool:
        dx = max(wall.x - WALL_SIZE / 2, min(player.x, wall.x + WALL_SIZE / 2))
        dy = max(wall.y - WALL_SIZE / 2, min(player.y, wall.y + WALL_SIZE / 2))

        closest_point = Vector2D(x=dx, y=dy)
        return (player - closest_point).length() < PLAYER_DIAMETER / 2


class Ray(BaseModel):
    distance: float  # [0, 1]
    obj: GameObject
    direction: Vector2D
