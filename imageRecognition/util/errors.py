
class DifferentBlockCountError(Exception):
    def __init__(self, err):
        Exception.__init__(self,"Image blocks count is not the same").format(err)
        self.error = err

class NullImageError(Exception):
    def __init__(self, err):
        Exception.__init__(self, "None image found").format(err)
        self. error = err

class TooSmallImageError(Exception):
    def __init__(self, err):
        Exception.__init__(self, "Image too small to blockify").format(err)
        self.error = err