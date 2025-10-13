import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold


class L2VNIMetric(BaseMetric):
    """Метрика количества L2 VNI"""

    def __init__(self):
        super().__init__(
            name="l2vni_count",
            description="L2 VNI Count",
            display_name="L2VNI"
        )
        self.threshold = get_threshold("l2vni")

    def extract_value(self, content: str) -> int:
        cmd11_match = re.search(r'Command 11:.*?(nvo vxlan id \d+.*?)(?=Command|\Z)', content, re.DOTALL)
        if cmd11_match:
            cmd11_lines = cmd11_match.group(1).strip().split('\n')
            return len([line for line in cmd11_lines if line.strip() and 'nvo vxlan id' in line])
        return 0

    def check_threshold(self, value: int) -> Dict[str, Any]:
        if value <= 3000:
            status = "OK"
        elif value <= 3500:
            status = "WARNING"
        else:
            status = "ALERT"

        return {
            "status": status,
            "details": f"{value}<br>Result={status}",
            "raw_data": value
        }