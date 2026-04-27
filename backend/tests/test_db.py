import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import MagicMock, patch
from src.dbcollections import PhotoCollection, LocationCollection, AIQuestion


def _make_db():
    with patch("pymongo.mongo_client.MongoClient") as MockClient:
        mock_mongo = MagicMock()
        MockClient.return_value = mock_mongo
        mock_mongo.admin.command.return_value = True

        with patch.dict(os.environ, {"DB_URI": "mongodb://mock"}):
            from src.db import DB
            db = DB()
    return db


def test_write_collection_calls_insert_one():
    db = _make_db()
    photo = PhotoCollection(1, "img.png", "data")
    mock_col = MagicMock()
    db.db.__getitem__.return_value = mock_col

    db.write_collection(photo)

    mock_col.insert_one.assert_called_once_with(photo.__dict__)


def test_query_collection_applies_filter():
    db = _make_db()
    mock_col = MagicMock()
    db.db.__getitem__.return_value = mock_col
    mock_col.find.return_value = iter([{"user_id": 0, "question": "Q", "answer": "A"}])

    results = list(db.query_collection(AIQuestion, filter={"user_id": 0}))

    mock_col.find.assert_called_once_with({"user_id": 0})
    assert len(results) == 1


def test_clear_collection_calls_delete_many():
    db = _make_db()
    mock_col = MagicMock()
    db.db.__getitem__.return_value = mock_col

    db.clear_collection("photo")

    mock_col.delete_many.assert_called_once_with({})


def test_upsert_last_location_calls_update_one():
    db = _make_db()
    mock_col = MagicMock()
    db.db.__getitem__.return_value = mock_col

    loc = LocationCollection(0, -8.24, 53.27)
    db.upsert_last_location(loc)

    mock_col.update_one.assert_called_once_with(
        {"user_id": 0},
        {"$set": {"lat": 53.27, "long": -8.24}},
        upsert=True,
    )
