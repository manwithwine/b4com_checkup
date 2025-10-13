import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class EVPNRouteCountMetric(BaseMetric):
    """Метрика использования MAC таблицы"""

    def __init__(self):
        super().__init__(
            name="evpn_route_count",
            description="EVPN Route Count which includes MAC-only, MAC-IPv4, MAC-IPv6",
            display_name="EVPN ROUTE COUNT"
        )
        self.threshold = get_threshold("evpn_route_count")

    def extract_value(self, content: str) -> Dict[str, int]:
        cmd14_match = re.search(
            r'Command 14:.*?Max supported route count\s+:\s+(\d+).*?Active route count:\s+(\d+)',
            content, re.DOTALL
        )
        if cmd14_match:
            max_count = int(cmd14_match.group(1))
            active_count = int(cmd14_match.group(2))
            return {"max": max_count, "active": active_count}
        return None

    def check_threshold(self, value: Dict[str, int]) -> Dict[str, Any]:
        if value["max"] > 0:
            percent = (value["active"] / value["max"]) * 100
            percent_str = f"{percent:.1f}%"

            if percent < self.threshold:
                status = "OK"
            else:
                status = "ALERT"

            return {
                "status": status,
                "details": f"{value['active']}/{value['max']}<br>{percent_str}<br>Result={status}",
                "raw_data": value,
                "percentage": percent
            }

        return {
            "status": "UNKNOWN",
            "details": "N/A",
            "raw_data": value
        }