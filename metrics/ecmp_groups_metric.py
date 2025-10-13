import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class ECMPMetric(BaseMetric):
    """Метрика использования ECMP групп"""

    def __init__(self):
        super().__init__(
            name="ecmp_groups",
            description="ECMP Groups Usage",
            display_name="ECMP"
        )
        self.threshold = get_threshold("ecmp_groups")

    def extract_value(self, content: str) -> Dict[str, int]:
        ecmp_match = re.search(r'ecmp_groups\s+:\s+(\d+)\s+/\s+(\d+)', content)
        if ecmp_match:
            used = int(ecmp_match.group(1))
            total = int(ecmp_match.group(2))
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