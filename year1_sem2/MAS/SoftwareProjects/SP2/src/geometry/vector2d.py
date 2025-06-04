import math

from pydantic import BaseModel


class Vector2D(BaseModel):
    x: float
    y: float

    def __add__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        return Vector2D(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        return Vector2D(x=self.x * scalar, y=self.y * scalar)

    def __truediv__(self, scalar: float) -> "Vector2D":
        return Vector2D(x=self.x / scalar, y=self.y / scalar)

    def length(self):
        return (self.x**2 + self.y**2) ** 0.5

    def versor(self) -> "Vector2D":
        length = self.length()
        if length == 0:
            return Vector2D(x=0, y=0)
        return self / length

    @classmethod
    def from_angle(cls, angle_degrees: float) -> "Vector2D":
        radians = math.radians(angle_degrees)
        return Vector2D(x=math.cos(radians), y=math.sin(radians))

    def base_angle(self) -> float:
        return math.degrees(math.atan2(self.y, self.x))

    def rotate(self, angle_deg: float) -> "Vector2D":
        radians = math.radians(angle_deg)
        cos_a = math.cos(radians)
        sin_a = math.sin(radians)
        return Vector2D(
            x=self.x * cos_a + self.y * sin_a,
            y=-self.x * sin_a + self.y * cos_a,
        )
