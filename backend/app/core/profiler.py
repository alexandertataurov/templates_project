"""
Code profiling utilities.
"""

import cProfile
import pstats
import io
from typing import Any, Callable, Optional
from functools import wraps
from .logging import get_logger

logger = get_logger(__name__)


def profile(
    output_file: Optional[str] = None, sort_by: str = "cumulative", lines: int = 50
):
    """
    Decorator for profiling functions.

    Args:
        output_file: Optional file to save profile results
        sort_by: Stats sorting key
        lines: Number of lines to print

    Example:
        >>> @profile(output_file="query_profile.txt")
        ... def complex_query():
        ...     pass
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            profile = cProfile.Profile()
            try:
                return profile.runcall(func, *args, **kwargs)
            finally:
                stats = pstats.Stats(profile)
                stats.sort_stats(sort_by)

                # Print to string
                stream = io.StringIO()
                stats.print_stats(lines)
                profile_data = stream.getvalue()

                # Log results
                logger.info(
                    f"Profile results for {func.__name__}",
                    extra={"profile": profile_data},
                )

                # Save to file if specified
                if output_file:
                    stats.dump_stats(output_file)

        return wrapper

    return decorator
