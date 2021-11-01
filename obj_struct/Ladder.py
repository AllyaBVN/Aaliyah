from .Vector import Vector
from .Area import Area


class Ladder:
    def __init__(self):
        self.id = int()
        self.width = float()
        self.length = float()
        self.top = Vector()
        self.bottom = Vector()
        self.direction = int()
        self.top_forward_area_id = int()
        self.top_forward_area = Area()
        self.top_left_area_id = int()
        self.top_left_area = Area()
        self.top_right_area_id = int()
        self.top_right_area = Area()
        self.top_behind_area_id = int()
        self.top_behind_area = Area()
        self.bottom_area_id = int()
        self.bottom_area = Area()