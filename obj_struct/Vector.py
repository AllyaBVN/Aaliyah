class Vector:
    def __init__(self, *args):
        if not len(args):
            self.x, self.y, self.z = 0.0, 0.0, 0.0
            return

        if type(args) == tuple:
            args = args[0]

        if len(args) != 3:
            raise Exception('A vector must contains 3 items !')

        if type(args[0]) not in [int, float]:
            raise TypeError('Items must be int or float !')

        self.x = args[0]
        self.y = args[1]
        self.z = args[2]