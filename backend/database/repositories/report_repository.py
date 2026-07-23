import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from backend.database.mongo import db_manager
from backend.database.repositories.base import BaseRepository

_in_memory_reports: Dict[str, Dict[str, Any]] = {}

class ReportRepository(BaseRepository):
    def __init__(self):
        self.collection_name = "reports"

    async def create(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        if "_id" not in report_data:
            report_data["_id"] = str(uuid.uuid4())
        if "created_at" not in report_data:
            report_data["created_at"] = datetime.utcnow()

        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].insert_one(report_data)
            return report_data
        else:
            _in_memory_reports[report_data["_id"]] = report_data
            return report_data

    async def get_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"_id": report_id})
        return _in_memory_reports.get(report_id)

    async def get_by_prediction_id(self, prediction_id: str) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            return await db_manager.db[self.collection_name].find_one({"prediction_id": prediction_id})
        for rep in _in_memory_reports.values():
            if rep.get("prediction_id") == prediction_id:
                return rep
        return None

    async def find_all(self, query: Dict[str, Any] = None, limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        query = query or {}
        if db_manager.is_connected and db_manager.db is not None:
            cursor = db_manager.db[self.collection_name].find(query).sort("created_at", -1).skip(skip).limit(limit)
            return await cursor.to_list(length=limit)
        items = list(_in_memory_reports.values())
        return items[skip:skip+limit]

    async def update(self, report_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if db_manager.is_connected and db_manager.db is not None:
            await db_manager.db[self.collection_name].update_one({"_id": report_id}, {"$set": updates})
            return await self.get_by_id(report_id)
        if report_id in _in_memory_reports:
            _in_memory_reports[report_id].update(updates)
            return _in_memory_reports[report_id]
        return None

    async def delete(self, report_id: str) -> bool:
        if db_manager.is_connected and db_manager.db is not None:
            res = await db_manager.db[self.collection_name].delete_one({"_id": report_id})
            return res.deleted_count > 0
        if report_id in _in_memory_reports:
            del _in_memory_reports[report_id]
            return True
        return False

report_repository = ReportRepository()
