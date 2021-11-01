from .Area import Area


class EncounterPath:
    def __init__(self):
        self.from_area_id = int()
        self.from_area = Area()
        self.from_direction = int()
        self.to_area_id = int()
        self.to_area = Area()
        self.to_direction = int()
        self.spots = list()  # list containing EncounterSpot objects
