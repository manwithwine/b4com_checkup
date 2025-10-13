import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class L3SVIMetric(BaseMetric):
    """Метрика количества L3 SVI"""

    def __init__(self):
        super().__init__(
            name="l3_svi_count",
            description="L3 SVI Count",
            display_name="L3 SVI"
        )
        self.threshold = get_threshold("l3_svi")

    def extract_value(self, content: str) -> int:
        cmd12_match = re.search(r'Command 12:.*?(vlan\d+\.\d+.*?)(?=Command|\Z)', content, re.DOTALL)
        if cmd12_match:
            cmd12_lines = cmd12_match.group(1).strip().split('\n')
            return len([line for line in cmd12_lines if line.strip() and 'vlan' in line and '.' in line])
        return 0

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