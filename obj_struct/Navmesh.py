class NavMesh:
    def __init__(self):
        self.places = dict()  # dict with place id as key, containing place objects
        self.areas = dict()  # dict with area id as key, containing area objects
        self.ladders = dict()  # dict with ladder id as key, containing ladder objects
        self.major_version = int()
        self.minor_version = int()
        self.bsp_size = int()
        self.is_mesh_analyzed = bool()
