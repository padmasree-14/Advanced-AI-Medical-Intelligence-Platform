import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.database.mongo import db_manager
from backend.database.repositories.base import BaseRepository

_in_memory_audit_logs: List[Dict[str, Any]] = []

class AuditRepository(BaseRepository):
    def __init__(self):
        self.collection_name = "audit_logs"

    async def create(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        if "_id" not in audit_data:
            audit_data["_id"] = str(uuid.uuid4())
        if "timestamp" not in audit_data:
            audit_data["timestamp"] = datetime.utcnow()

        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].insert_one(audit_data)
            return audit_data
        else:
            _in_memory_audit_logs.append(audit_data)
            return audit_data

    async def get_by_id(self, audit_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"_id": audit_id})
        for item in _in_memory_audit_logs:
            if item.get("_id") == audit_id:
                return item
        return None

    async def find_all(self, query: Dict[str, Any] = None, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        query = query or {}
        if db_manager.is_connected and db_manager.db is not None:
            cursor = db_manager.db[self.collection_name].find(query).sort("timestamp", -1).skip(skip).limit(limit)
            return await cursor.to_list(length=limit)
        sorted_logs = sorted(_in_memory_audit_logs, key=lambda x: str(x.get("timestamp", "")), reverse=True)
        return sorted_logs[skip:skip+limit]

    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return None  # Audit logs are append-only immutable records

    async def delete(self, entity_id: str) -> bool:
        return False  # Audit logs cannot be deleted

audit_repository = AuditRepository()
