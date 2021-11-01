from .Area import Area


class Connection:
    def __init__(self):
        self.source_area = Area()
        self.target_area_id = int()
        self.target_area = Area()
        self.nav_direction = int()
