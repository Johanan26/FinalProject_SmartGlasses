from fastapi import FastAPI
from pydantic import BaseModel

class UploadPhoto(BaseModel):
    data: str
    name: str

class UploadVideo(BaseModel):
    data: str
    name: str
    
class UploadLocation(BaseModel):
    long: float
    lat: float