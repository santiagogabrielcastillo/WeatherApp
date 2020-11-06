class CityError(Exception):
    def __init__(self, message):
        self.message = message


class CityErrorNotFound(CityError):
    pass
