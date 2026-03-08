from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from firebase_admin import auth, credentials, initialize_app
from .db import DB
from .models import UploadPhoto, UploadVideo, UploadLocation, UploadQuestion
from .dbcollections import LocationCollection, VideoCollection, PhotoCollection, AIQuestion
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import os

load_dotenv()

app = FastAPI()
db = DB()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cred = credentials.Certificate("service.json")
initialize_app(cred)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    
    token = authorization.split(" ")[1]
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/get_questions")
async def root(user=Depends(get_current_user)):
    questions = list(db.query_collection(AIQuestion, filter={"user_id": 0}))
    return {"questions": questions}

@app.post("/ask_question")
async def upload_question(question: UploadQuestion, user=Depends(get_current_user)):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=question.data
    )
    db.write_collection(AIQuestion(0, question.data, response.text))
    return response.text
    
@app.post("/upload_photo")
async def upload_photo(photo: UploadPhoto, user=Depends(get_current_user)):
    photo_collection = PhotoCollection(0, photo.data)
    db.write_collection(photo_collection)
    

@app.post("/upload_video")
async def upload_video(video: UploadVideo, user=Depends(get_current_user)):
    video_collection = VideoCollection(0 , video.data)
    db.write_collection(video_collection)
    
@app.get("/gallery")
async def get_gallery(user=Depends(get_current_user)):
    videos = list(db.query_collection(VideoCollection, filter={"user_id": 0}))
    photos = list(db.query_collection(PhotoCollection, filter={"user_id": 0}))
    
    for item in videos + photos:
        item["_id"] = ""
    
    return {
        "videos": videos,
        "photos": photos
    }
    
    
@app.get("/get_last_location")
async def get_last_location(user=Depends(get_current_user)):
    # we are querying multiple locations here but we should expect to only obtain one location
    locations = list(db.query_collection(LocationCollection, filter={"user_id": 0}))
    location = locations[0]
    location["_id"] = ""
    return {"location": location}

@app.post("/upload_location")
async def upload_last_location(location: UploadLocation, user=Depends(get_current_user)):
    location_collection = LocationCollection(user["uid"], location.lat, location.long)
    db.upsert_last_location(location_collection)
