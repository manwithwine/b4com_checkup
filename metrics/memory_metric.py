import re
from typing import Any, Dict
from .base_metric import RegexMetric
from config.thresholds import get_threshold


class MemoryMetric(RegexMetric):
    """Метрика использования памяти"""

    def __init__(self):
        super().__init__(
            name="memory",
            description="Memory Usage",
            pattern=r'Free\s+:\s+\d+\s+MB\s+\((\d+) %\)',
            value_type=int,
            display_name="MEMORY"
        )
        self.threshold = get_threshold("memory_free")

    def check_threshold(self, value: int) -> Dict[str, Any]:
        if value >= self.threshold:
            status = "OK"
        else:
            status = "WARNING"

        return {
            "status": status,
            "details": f"{value}%<br>Result={status}",
            "raw_data": value
        }