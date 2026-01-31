class Collection:
    _name = "base"
    
class PhotoCollection(Collection):
    _name = "photo"

    def __init__(self, user_id: str, file_name: str, data: str):
        self.user_id = user_id
        self.file_name = file_name
        self.data = data

class VideoCollection(Collection):
    _name = "video"

    def __init__(self, user_id: str, file_name: str, data: str):
        self.user_id = user_id
        self.file_name = file_name
        self.data = data

class LocationCollection(Collection):
    _name = "location"

    def __init__(self, user_id: str, long: float, lat: float):
        self.user_id = user_id
        self.long = long
        self.lat = lat
