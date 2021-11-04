import struct
from file_handler import FileHandler
from obj_struct import Area, EncounterPath, EncounterSpot, HidingSpot, Ladder, LadderConnection, Place, VisibleArea, Connection, NavMesh, Vector
from vars_size import VarsSize


class Parser:
    def __init__(self):
        self.raw_files = self._get_raw_files()

        self.offset = int()
        self.current_file = bytes()

    def initialize_parser(self, map_name):
        file = self.raw_files.get(map_name)
        if not file:
            raise KeyError("{} doesn't exist".format(map_name))

        self.current_file = file
        self.offset = 0

    def parse(self, map_name):
        self.initialize_parser(map_name)

        magic = self.read("I", VarsSize.uint32)
        if magic != 4277009102:
            raise Exception("Wrong magic number, it is not a nav file")

        navmesh = NavMesh()

        navmesh.major_version = self.read("I", VarsSize.uint32)
        if navmesh.major_version < 6 or navmesh.major_version > 16:
            raise Exception('Version is too old')

        if navmesh.major_version >= 10:
            navmesh.minor_version = self.read("I", VarsSize.uint32)

        navmesh.bsp_size = self.read("I", VarsSize.uint32)

        if navmesh.major_version >= 14:
            navmesh.is_mesh_analyzed = self.read("B", VarsSize.uint8)

        place_count = self.read("H", VarsSize.uint16)

        for i in range(place_count):
            cur_place = Place()
            cur_place.id = i + 1

            name_len = self.read("H", VarsSize.uint16)
            cur_place.name = self.read("{}s".format(name_len-1), name_len)

            navmesh.places[i + 1] = cur_place

        if navmesh.major_version > 11:
            has_unnamed_areas = self.read("B", VarsSize.uint8)

        area_count = self.read("I", VarsSize.uint32)
        for i in range(area_count):
            area = Area()

            area.id = self.read("I", VarsSize.uint32)
            if navmesh.major_version <= 8:
                area.flags = self.read("B", VarsSize.uint8)
            elif navmesh.major_version < 13:
                area.flags = self.read("H", VarsSize.uint16)
            else:
                area.flags = self.read("I", VarsSize.uint32)

            area.north_west = self.read("3f", VarsSize.Vector)
            area.south_east = self.read("3f", VarsSize.Vector)
            area.north_east_z = self.read("f", VarsSize.float)
            area.south_west_z = self.read("f", VarsSize.float)

            for direction in range(4):

                connection_count = self.read("I", VarsSize.uint32)
                for j in range(connection_count):
                    cur_connection = Connection()
                    cur_connection.source_area = area
                    cur_connection.nav_direction = direction

                    cur_connection.target_area_id = self.read("I", VarsSize.uint32)
                    area.connections.append(cur_connection)

            hiding_spot_count = self.read("B", VarsSize.uint8)
            for j in range(hiding_spot_count):
                cur_hiding_spot = HidingSpot()
                cur_hiding_spot.id = self.read("I", VarsSize.uint32)
                cur_hiding_spot.position = self.read("3f", VarsSize.Vector)
                cur_hiding_spot.flags = self.read("B", VarsSize.uint8)

                area.hiding_spots.append(cur_hiding_spot)

            if navmesh.major_version < 15:
                approch_area_count = self.read("B", VarsSize.uint8)
                self.increase_offset((4*3 + 2) * int(approch_area_count))

            encounter_paths_count = self.read("I", VarsSize.uint32)
            for j in range(encounter_paths_count):
                cur_path = EncounterPath()

                cur_path.from_area_id = self.read("I", VarsSize.uint32)
                cur_path.from_direction = self.read("B", VarsSize.uint8)
                cur_path.to_area_id = self.read("I", VarsSize.uint32)
                cur_path.to_direction = self.read("B", VarsSize.uint8)

                spot_count = self.read("B", VarsSize.uint8)
                for s in range(spot_count):
                    cur_spot = EncounterSpot()

                    cur_spot.order_id = self.read("I", VarsSize.uint32)
                    distance = self.read("B", VarsSize.uint8)

                    cur_spot.distance = distance / 255

                    cur_path.spots.append(cur_spot)

            place_id = self.read("H", VarsSize.uint16)
            place = navmesh.places.get(place_id)
            if place:
                area.place = place
                place.areas.append(area)

            for direction in range(2):
                ladder_connection_count = self.read("I", VarsSize.uint32)

                for j in range(ladder_connection_count):
                    cur_ladder_connection = LadderConnection()
                    cur_ladder_connection.source_area = area
                    cur_ladder_connection.nav_ladder_direction = direction
                    cur_ladder_connection.target_id = self.read("I", VarsSize.uint32)

                    area.ladder_connections.append(cur_ladder_connection)

            area.earliest_occupy_time_first_team = self.read("f", VarsSize.float)
            area.earliest_occupy_time_second_team = self.read("f", VarsSize.float)

            if navmesh.major_version >= 11:
                area.north_west_light_intensity = self.read("f", VarsSize.float)
                area.north_east_light_intensity = self.read("f", VarsSize.float)
                area.south_east_light_intensity = self.read("f", VarsSize.float)
                area.south_west_light_intensity = self.read("f", VarsSize.float)

            if navmesh.major_version >= 16:
                visible_area_count = self.read("I", VarsSize.uint32)
                for j in range(visible_area_count):
                    cur_visible_area = VisibleArea()

                    cur_visible_area.visible_area_id = self.read("I", VarsSize.uint32)
                    cur_visible_area.attributes = self.read("b", VarsSize.uint8)

                    area.visible_areas.append(cur_visible_area)

            area.inherit_visibility_from = self.read("I", VarsSize.uint32)

            garbage_count = self.read("b", VarsSize.uint8)

            self.increase_offset(garbage_count * 14)

            navmesh.areas[area.id] = area

        ladder_count = self.read('I', VarsSize.uint32)
        for i in range(ladder_count):
            cur_ladder = Ladder()
            cur_ladder.id = self.read('I', VarsSize.uint32)
            cur_ladder.width = self.read("f", VarsSize.float)
            cur_ladder.top = self.read("3f", VarsSize.Vector)
            cur_ladder.bottom = self.read("3f", VarsSize.Vector)
            cur_ladder.length = self.read("f", VarsSize.float)
            cur_ladder.direction = self.read('I', VarsSize.uint32)

            cur_ladder.top_forward_area_id = self.read('I', VarsSize.uint32)
            cur_ladder.top_forward_area = navmesh.areas.get(cur_ladder.top_forward_area_id)
            cur_ladder.top_left_area_id = self.read('I', VarsSize.uint32)
            cur_ladder.top_left_area = navmesh.areas.get(cur_ladder.top_left_area_id)
            cur_ladder.top_right_area_id = self.read('I', VarsSize.uint32)
            cur_ladder.top_right_area = navmesh.areas.get(cur_ladder.top_right_area_id)
            cur_ladder.top_behind_area_id = self.read('I', VarsSize.uint32)
            cur_ladder.top_behind_area = navmesh.areas.get(cur_ladder.top_behind_area_id)
            cur_ladder.bottom_area_id = self.read('I', VarsSize.uint32)
            cur_ladder.bottom_area = navmesh.areas.get(cur_ladder.bottom_area_id)

            navmesh.ladders[cur_ladder.id] = cur_ladder

        return navmesh

    def read(self, format_string, byte_size):
        output = struct.unpack_from(format_string, self.current_file, self.offset)
        self.increase_offset(byte_size)
        if byte_size == VarsSize.Vector and format_string in ['fff', '3f']:
            return Vector(output)
        return output[0]

    def increase_offset(self, value):
        self.offset += value

    @staticmethod
    def _get_raw_files():
        handler = FileHandler()
        return handler.get_nav_files()