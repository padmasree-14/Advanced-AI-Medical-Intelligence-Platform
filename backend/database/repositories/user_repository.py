import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.database.mongo import db_manager
from backend.database.repositories.base import BaseRepository

_in_memory_users: Dict[str, Dict[str, Any]] = {}

class UserRepository(BaseRepository):
    def __init__(self):
        self.collection_name = "users"

    async def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        if "_id" not in user_data:
            user_data["_id"] = str(uuid.uuid4())
        user_data["created_at"] = user_data.get("created_at", datetime.utcnow())
        user_data["updated_at"] = user_data.get("updated_at", datetime.utcnow())

        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].insert_one(user_data)
            return user_data
        else:
            _in_memory_users[user_data["_id"]] = user_data
            return user_data

    async def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"_id": user_id})
        return _in_memory_users.get(user_id)

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"email": email.lower()})
        for user in _in_memory_users.values():
            if user.get("email", "").lower() == email.lower():
                return user
        return None

    async def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"username": username.lower()})
        for user in _in_memory_users.values():
            if user.get("username", "").lower() == username.lower():
                return user
        return None

    async def find_all(self, query: Dict[str, Any] = None, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        query = query or {}
        if db_manager.is_connected and db_manager.db is not None:
            cursor = db_manager.db[self.collection_name].find(query).skip(skip).limit(limit)
            return await cursor.to_list(length=limit)
        items = list(_in_memory_users.values())
        return items[skip:skip+limit]

    async def update(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        updates["updated_at"] = datetime.utcnow()
        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].update_one({"_id": user_id}, {"$set": updates})
            return await self.get_by_id(user_id)
        if user_id in _in_memory_users:
            _in_memory_users[user_id].update(updates)
            return _in_memory_users[user_id]
        return None

    async def delete(self, user_id: str) -> bool:
        if db_manager.is_connected and db_manager.db is not None:
            res = await db_manager.db[self.collection_name].delete_one({"_id": user_id})
            return res.deleted_count > 0
        if user_id in _in_memory_users:
            del _in_memory_users[user_id]
            return True
        return False

user_repository = UserRepository()
