

# TODO do something with the error
class InvalidBlockSizeError(Exception):
    def __init__(self, errors):
        super().__init__("Image blocks number not the same")

        self.errors = errors

class