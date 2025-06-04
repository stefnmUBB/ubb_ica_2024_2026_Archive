import uuid

from pydantic import BaseModel

from src.geometry import Vector2D, closest_vec_multiple_angle

from .constants import PLAYER_ROTATE_DEGREES


PlayerID = str


class PlayerMapData(BaseModel):
    player_id: PlayerID
    team: str
    position: Vector2D
    direction: Vector2D | None = None

    def _compute_default_direction(self, target: Vector2D):
        dir_vec = (target - self.position).versor()
        dir_vec = closest_vec_multiple_angle(dir_vec, PLAYER_ROTATE_DEGREES)
        self.direction = dir_vec


class GameMap(BaseModel):
    grid: list[list[str]]
    width: int
    height: int
    walls: list[Vector2D]
    players: dict[PlayerID, PlayerMapData]

    def __init__(self, grid: list[list[str]]):
        grid = self._pad_with_walls(grid)
        super().__init__(
            grid=grid,
            width=len(grid[0]),
            height=len(grid),
            walls=set(),
            players={},
        )
        self._process_grid()

    @classmethod
    def from_file(cls, path: str) -> "GameMap":
        with open(path, "r") as f:
            lines = [line.rstrip() for line in f if line.strip()]
            max_width = max(len(line) for line in lines)
            grid = [list(line.ljust(max_width, ".")) for line in lines]
        return cls(grid)

    @classmethod
    def _pad_with_walls(cls, grid: list[list[str]]) -> list[list[str]]:
        padded = []

        width = len(grid[0])
        wall_row = ["#"] * (width + 2)

        padded.append(wall_row)
        for row in grid:
            padded.append(["#", *row, "#"])
        padded.append(wall_row)

        return padded

    def _process_grid(self):
        center = Vector2D(x=self.width, y=self.height) / 2
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == ".":
                    continue
                elif cell == "#":
                    self.walls.append(Vector2D(x=x, y=y))
                else:
                    player_id = str(uuid.uuid4())
                    team = cell
                    player = PlayerMapData(
                        position=Vector2D(x=x, y=y), team=team, player_id=player_id
                    )
                    player._compute_default_direction(center)
                    self.players[player_id] = player
                    self.grid[y][x] = "."

    def _point_inside_grid(self, x: int | float, y: int | float) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def nearest_walls(self, point: Vector2D) -> list[Vector2D]:
        point_x, point_y = int(point.x), int(point.y)
        walls = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                other_x = point_x + dx
                other_y = point_y + dy
                if not self._point_inside_grid(other_x, other_y):
                    continue
                other = self.grid[other_y][other_x]
                if other == "#":
                    walls.append(Vector2D(x=other_x, y=other_y))
        return walls
