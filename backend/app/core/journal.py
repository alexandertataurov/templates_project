"""
Audit logging and journaling functionality.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.journal import JournalEntry
from .logging import get_logger

logger = get_logger(__name__)


class Journal:
    """Audit journal for tracking system events."""

    @staticmethod
    async def log_event(
        db: AsyncSession,
        event_type: str,
        user_id: Optional[int],
        entity_type: str,
        entity_id: Optional[int],
        details: Dict[str, Any],
        ip_address: Optional[str] = None,
    ) -> JournalEntry:
        """
        Log an event to the audit journal.

        Args:
            db: Database session
            event_type: Type of event (create, update, delete, etc.)
            user_id: ID of user performing action
            entity_type: Type of entity being modified
            entity_id: ID of entity being modified
            details: Additional event details
            ip_address: IP address of request

        Returns:
            Created journal entry
        """
        entry = JournalEntry(
            event_type=event_type,
            user_id=user_id,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details,
            ip_address=ip_address,
            timestamp=datetime.utcnow(),
        )

        try:
            db.add(entry)
            await db.commit()
            await db.refresh(entry)

            logger.info(
                "Audit event logged",
                extra={
                    "event_type": event_type,
                    "user_id": user_id,
                    "entity_type": entity_type,
                    "entity_id": entity_id,
                },
            )

            return entry
        except Exception as e:
            logger.error(
                "Failed to log audit event",
                exc_info=e,
                extra={
                    "event_type": event_type,
                    "user_id": user_id,
                    "entity_type": entity_type,
                    "entity_id": entity_id,
                },
            )
            raise

    @staticmethod
    async def get_entity_history(
        db: AsyncSession, entity_type: str, entity_id: int
    ) -> list[JournalEntry]:
        """Get audit history for an entity."""
        result = await db.execute(
            select(JournalEntry)
            .where(
                JournalEntry.entity_type == entity_type,
                JournalEntry.entity_id == entity_id,
            )
            .order_by(JournalEntry.timestamp.desc())
        )
        return result.scalars().all()
