import re
from typing import Any, Dict
from .base_metric import RegexMetric
from config.thresholds import get_threshold


class IPv4RoutesMetric(RegexMetric):
    """Метрика количества IPv4 маршрутов"""

    def __init__(self):
        super().__init__(
            name="ipv4_routes",
            description="IPv4 Routes Count",
            pattern=r'routes\s+:\s+(\d+)\s+/\s+\d+',
            value_type=int,
            display_name="IPv4 ROUTES"
        )
        self.threshold = get_threshold("ipv4_routes")

    def check_threshold(self, value: int) -> Dict[str, Any]:
        if value <= self.threshold:
            status = "OK"
        else:
            status = "ALERT"

        return {
            "status": status,
            "details": f"{value}<br>Result={status}",
            "raw_data": value
        }