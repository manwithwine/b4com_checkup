import re
from typing import Any, Dict
from .base_metric import BaseMetric
from config.thresholds import get_threshold

class IPVrfMetric(BaseMetric):
    """Метрика количества IP VRF"""

    def __init__(self):
        super().__init__(
            name="ip_vrf_count",
            description="IP VRF Count",
            display_name="IP VRF"
        )
        self.threshold = get_threshold("ip_vrf")

    def extract_value(self, content: str) -> int:
        cmd13_match = re.search(r'Command 13:.*?(tunvxlan\d+.*?)(?=Command|\Z)', content, re.DOTALL)
        if cmd13_match:
            cmd13_lines = cmd13_match.group(1).strip().split('\n')
            return len([line for line in cmd13_lines if line.strip() and 'tunvxlan' in line])
        return 0

    def check_threshold(self, value: int) -> Dict[str, Any]:
        if value <= 400:
            status = "OK"
        elif value <= 450:
            status = "WARNING"
        else:
            status = "ALERT"

        return {
            "status": status,
            "details": f"{value}<br>Result={status}",
            "raw_data": value
        }