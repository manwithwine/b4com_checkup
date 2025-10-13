import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class L3NextHopMetric(BaseMetric):
    """Метрика использования next-hop записей"""

    def __init__(self):
        super().__init__(
            name="l3_nexthop",
            description="L3 Next-Hop Usage",
            display_name="NEXTHOP"
        )
        self.threshold = get_threshold("l3_nexthop")

    def extract_value(self, content: str) -> Dict[str, int]:
        nexthop_match = re.search(r'nexthops\s+:\s+(\d+)\s+/\s+(\d+)', content)
        if nexthop_match:
            used = int(nexthop_match.group(1))
            total = int(nexthop_match.group(2))
            return {"used": used, "total": total}
        return None

    def check_threshold(self, value: Dict[str, int]) -> Dict[str, Any]:
        if value["total"] > 0:
            percent = (value["used"] / value["total"]) * 100
            percent_str = f"{percent:.1f}%"

            if percent < self.threshold:
                status = "OK"
            else:
                status = "ALERT"

            return {
                "status": status,
                "details": f"{value['used']}/{value['total']}<br>{percent_str}<br>Result={status}",
                "raw_data": value,
                "percentage": percent
            }

        return {
            "status": "UNKNOWN",
            "details": "N/A",
            "raw_data": value
        }