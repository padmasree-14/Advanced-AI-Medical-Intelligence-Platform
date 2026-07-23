from typing import Optional, Dict, Any
from backend.database.repositories.audit_repository import audit_repository

class AuditService:
    async def log_action(
        self,
        action: str,
        resource: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        audit_record = {
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "ip_address": ip_address,
            "details": details or {}
        }
        await audit_repository.create(audit_record)

audit_service = AuditService()
