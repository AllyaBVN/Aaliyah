from .Area import Area
from .Ladder import Ladder


class LadderConnection:
    def __init__(self):
        self.source_area = Area()
        self.target_id = int()
        self.target_ladder = Ladder()
        self.nav_ladder_direction = int()