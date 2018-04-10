
class DifferentBlockCountError(Exception):
    def __init__(self, err):
        Exception.__init__(self,"Image blocks count is not the same")
        self.error = err

class NullImageError(Exception):
    def __init__(self, err):
        Exception.__init__(self, "None type  image found")
        self. error = err

class TooSmallImageError(Exception):
    def __init__(self, err):
        Exception.__init__(self, "Image too small to blockify")
        self.error = err
