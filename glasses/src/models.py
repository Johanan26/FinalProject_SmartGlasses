from dataclasses import dataclass

@dataclass
class FileData:
    name: str
    data: str
    
@dataclass
class Location:
    long: float
    lat: float