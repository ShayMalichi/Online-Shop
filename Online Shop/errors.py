class ItemNotExistError(Exception):
    def __init__(self, value):
        self.value = value


class ItemAlreadyExistsError(Exception):
    def __init__(self, value):
        self.value = value


class TooManyMatchesError(Exception):
    def __init__(self, value):
        self.value = value
