import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.dbcollections import (
    PhotoCollection, VideoCollection, LocationCollection, AIQuestion
)


def test_photo_collection_attributes():
    p = PhotoCollection(1, "img.png", "base64data")
    assert p.user_id == 1
    assert p.file_name == "img.png"
    assert p.data == "base64data"
    assert PhotoCollection._name == "photo"


def test_video_collection_attributes():
    v = VideoCollection(2, "clip.mp4", "videodata")
    assert v.user_id == 2
    assert v.file_name == "clip.mp4"
    assert v.data == "videodata"
    assert VideoCollection._name == "video"


def test_location_collection_attributes():
    loc = LocationCollection(3, -8.24, 53.27)
    assert loc.user_id == 3
    assert loc.long == -8.24
    assert loc.lat == 53.27
    assert LocationCollection._name == "location"


def test_ai_question_attributes():
    q = AIQuestion(0, "What is AI?", "AI is...")
    assert q.user_id == 0
    assert q.question == "What is AI?"
    assert q.answer == "AI is..."
    assert AIQuestion._name == "questions"


def test_collection_dict_serialisation():
    p = PhotoCollection(1, "img.png", "data")
    assert p.__dict__ == {"user_id": 1, "file_name": "img.png", "data": "data"}
