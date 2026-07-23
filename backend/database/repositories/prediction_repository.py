import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.database.mongo import db_manager
from backend.database.repositories.base import BaseRepository

_in_memory_predictions: Dict[str, Dict[str, Any]] = {}

class PredictionRepository(BaseRepository):
    def __init__(self):
        self.collection_name = "predictions"

    async def create(self, prediction_data: Dict[str, Any]) -> Dict[str, Any]:
        if "_id" not in prediction_data:
            prediction_data["_id"] = str(uuid.uuid4())
        if "created_at" not in prediction_data:
            prediction_data["created_at"] = datetime.utcnow()

        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].insert_one(prediction_data)
            return prediction_data
        else:
            _in_memory_predictions[prediction_data["_id"]] = prediction_data
            return prediction_data

    async def get_by_id(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"_id": prediction_id})
        return _in_memory_predictions.get(prediction_id)

    async def get_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            cursor = db_manager.db[self.collection_name].find({"user_id": user_id}).sort("created_at", -1).skip(skip).limit(limit)
            return await cursor.to_list(length=limit)
        user_scans = [p for p in _in_memory_predictions.values() if p.get("user_id") == user_id]
        user_scans.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        return user_scans[skip:skip+limit]

    async def find_all(self, query: Dict[str, Any] = None, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        query = query or {}
        if db_manager.is_connected and db_manager.db is not None:
            cursor = db_manager.db[self.collection_name].find(query).sort("created_at", -1).skip(skip).limit(limit)
            return await cursor.to_list(length=limit)
        filtered = list(_in_memory_predictions.values())
        filtered.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        return filtered[skip:skip+limit]

    async def update(self, prediction_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].update_one({"_id": prediction_id}, {"$set": updates})
            return await self.get_by_id(prediction_id)
        if prediction_id in _in_memory_predictions:
            _in_memory_predictions[prediction_id].update(updates)
            return _in_memory_predictions[prediction_id]
        return None

    async def delete(self, prediction_id: str) -> bool:
        if db_manager.is_connected and db_manager.db is not None:
            res = await db_manager.db[self.collection_name].delete_one({"_id": prediction_id})
            return res.deleted_count > 0
        if prediction_id in _in_memory_predictions:
            del _in_memory_predictions[prediction_id]
            return True
        return False

    async def count_by_user(self, user_id: str) -> int:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].count_documents({"user_id": user_id})
        return len([p for p in _in_memory_predictions.values() if p.get("user_id") == user_id])

prediction_repository = PredictionRepository()
