from fastapi import FastAPI, HTTPException, Header, Depends
from firebase_admin import auth, credentials, initialize_app
from db import DB
from .models import UploadPhoto, UploadVideo, UploadLocation
from .dbcollections import LocationCollection, VideoCollection, PhotoCollection

app = FastAPI()
db = DB()

cred = credentials.Certificate("service.json")
initialize_app(cred)

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/ai_question")
async def root():
    return {"message": "Hello World"}

@app.post("/upload_question")
async def upload_question():
    ...
    
@app.post("/upload_photo")
async def upload_photo(photo: UploadPhoto, user=Depends(get_current_user)):
    photo_collection = PhotoCollection(user["uid"], photo.data)
    db.write_collection(photo_collection)
    

@app.post("/upload_video")
async def upload_video(video: UploadVideo, user=Depends(get_current_user)):
    video_collection = VideoCollection(user["uid"], video.data)
    db.write_collection(video_collection)
    
@app.get("/gallery")
async def get_gallery(user=Depends(get_current_user)):
    videos = list(db.query_collection(VideoCollection, filter={"user_id": user["uid"]}))
    photos = list(db.query_collection(PhotoCollection, filter={"user_id": user["uid"]}))
    
    return {
        "videos": videos,
        "photos": photos
    }
    
    
@app.get("/get_last_location")
async def get_last_location(user=Depends(get_current_user)):
    # we are querying multiple locations here but we should expect to only obtain one location
    locations = list(db.query_collection(LocationCollection, filter={"user_id": user["uid"]}))
    return {"location": locations[0]}

@app.post("/upload_location")
async def upload_last_location(location: UploadLocation, user=Depends(get_current_user)):
    location_collection = LocationCollection(user["uid"], location.lat, location.long)
    db.upsert_last_location(location_collection)
