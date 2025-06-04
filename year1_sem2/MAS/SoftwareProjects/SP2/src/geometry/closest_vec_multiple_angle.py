import math

from .vector2d import Vector2D


def closest_vec_multiple_angle(unit_vec: Vector2D, target_angle: float) -> Vector2D:
    angle_rad = math.atan2(unit_vec.y, unit_vec.x)
    angle_deg = math.degrees(angle_rad)
    rounded_deg = round(angle_deg / target_angle) * target_angle
    angle_rad = math.radians(rounded_deg)
    dir_x = math.cos(angle_rad)
    dir_y = math.sin(angle_rad)
    return Vector2D(x=dir_x, y=dir_y)
