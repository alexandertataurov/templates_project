"""
Performance metrics and monitoring.
"""

import time
from typing import Any, Dict, Optional
from contextlib import contextmanager
from statistics import mean, median
from app.core.logging import get_logger

logger = get_logger(__name__)


class Metrics:
    """Performance metrics collector."""

    def __init__(self):
        self.metrics: Dict[str, list[float]] = {}
        self.counters: Dict[str, int] = {}

    def record_time(self, metric_name: str, value: float) -> None:
        """Record a timing metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)

    def increment_counter(self, name: str, value: int = 1) -> None:
        """Increment a counter metric."""
        self.counters[name] = self.counters.get(name, 0) + value

    def get_stats(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        if metric_name not in self.metrics:
            return {}
        values = self.metrics[metric_name]
        return {
            "count": len(values),
            "mean": mean(values),
            "median": median(values),
            "min": min(values),
            "max": max(values),
        }

    def get_counter(self, name: str) -> int:
        """Get counter value."""
        return self.counters.get(name, 0)

    def reset(self) -> None:
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()


metrics = Metrics()


@contextmanager
def timing(name: str, extra: Optional[Dict[str, Any]] = None):
    """
    Context manager for timing code blocks.

    Example:
        with timing("db_query", {"table": "documents"}):
            result = db.execute(query)
    """
    start_time = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        metrics.record_time(name, elapsed)
        log_data = {"duration": elapsed}
        if extra:
            log_data.update(extra)
        logger.info(f"Operation timing: {name}", extra={"metrics": log_data})
