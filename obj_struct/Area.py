from .Vector import Vector
from .Place import Place


class Area:
    def __init__(self):
        self.id = int()
        self.north_west = Vector()
        self.south_east = Vector()
        self.flags = int()
        self.north_east_z = float()
        self.south_west_z = float()
        self.north_west_light_intensity = float()
        self.north_east_light_intensity = float()
        self.south_west_light_intensity = float()
        self.south_east_light_intensity = float()
        self.place = Place()
        self.connections = list()  # list of connection id meaning the area id of the connection
        self.hiding_spots = list()  # list containing hiding spot objects
        self.encounter_paths = list()  # list containing encounter path objects
        self.ladder_connections = list()  # list containing ladder connection objects
        self.visible_areas = list()  # list containing visible area objects
        self.earliest_occupy_time_first_team = float()
        self.earliest_occupy_time_second_team = float()
        self.inherit_visibility_from_area_id = int()
