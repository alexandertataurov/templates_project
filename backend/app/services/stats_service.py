"""
Service for generating document statistics.
"""

from datetime import date, datetime
from typing import List, Dict, Any
import logging
from sqlalchemy import func, extract, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document

logger = logging.getLogger(__name__)


class StatsService:
    """Service for handling document statistics operations."""

    @staticmethod
    async def get_total_amount_by_type(db: AsyncSession, document_type: str) -> float:
        """Get total amount for a specific document type from dynamic_fields."""
        result = await db.execute(
            select(
                func.sum(
                    func.cast(
                        Document.dynamic_fields["total_price"].astext, func.Numeric
                    )
                )
            ).where(Document.document_type == document_type)
        )
        total = result.scalar() or 0
        logger.info("Total amount for %s: %f", document_type, total)
        return float(total)

    @staticmethod
    async def get_monthly_stats(
        db: AsyncSession, year: int, month: int
    ) -> Dict[str, Any]:
        """
        Get monthly statistics for all documents.

        Args:
            db: Database session
            year: Year to get stats for
            month: Month to get stats for

        Returns:
            Dictionary with monthly statistics
        """
        logger.debug("Fetching monthly stats for %d-%d", year, month)
        # Count documents by type
        query = (
            select(Document.document_type, func.count(Document.id).label("count"))
            .where(
                extract("year", Document.created_date) == year,
                extract("month", Document.created_date) == month,
            )
            .group_by(Document.document_type)
        )
        result = await db.execute(query)
        doc_counts = {row[0]: row[1] for row in result.fetchall()}

        # Total amount from dynamic_fields (assuming 'total_price' exists)
        total_query = select(
            func.sum(
                func.cast(Document.dynamic_fields["total_price"].astext, func.Numeric)
            )
        ).where(
            extract("year", Document.created_date) == year,
            extract("month", Document.created_date) == month,
        )
        total_result = await db.execute(total_query)
        total_amount = float(total_result.scalar() or 0)

        stats = {
            "year": year,
            "month": month,
            "document_counts": doc_counts,
            "total_amount": total_amount,
        }
        logger.info("Monthly stats retrieved: %s", stats)
        return stats


# Create service instance
stats_service = StatsService()


# Export individual functions for backward compatibility
async def get_monthly_stats(db: AsyncSession, year: int, month: int) -> Dict[str, Any]:
    return await stats_service.get_monthly_stats(db, year, month)


async def get_total_amount_by_type(db: AsyncSession, document_type: str) -> float:
    return await stats_service.get_total_amount_by_type(db, document_type)
