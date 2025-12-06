class Collection:
    _name = "base"

class PhotoCollection(Collection):
    _name = "photo"

    def __init__(self, user_id: int, data: str):
        self.user_id = user_id
        self.data = data

class VideoCollection(Collection):
    _name = "video"

    def __init__(self, user_id: int, data: str):
        self.user_id = user_id
        self.data = data

class LocationCollection(Collection):
    _name = "location"

    def __init__(self, user_id: int, long: float, lat: float):
        self.user_id = user_id
        self.long = long
        self.lat = lat
